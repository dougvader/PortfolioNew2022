"use client"; // Ensure this is the first line

import React, { useState, useEffect } from 'react';
import { signIn, useSession } from 'next-auth/react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import { loadStripe } from '@stripe/stripe-js';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!);

const Bookings: React.FC = () => {
    const [bookings, setBookings] = useState<{ date: Date, type: string }[]>([]);
    const { data: session } = useSession();
    const [selectedDate, setSelectedDate] = useState<Date | null>(null);
    const [selectedService, setSelectedService] = useState<string | null>(null);
    const [availableServices, setAvailableServices] = useState({
        mixdownWithFeedback: false,
        mixdownNoFeedback: false,
        masteringWithFeedback: false,
        masteringNoFeedback: false
    });

    useEffect(() => {
        const fetchBookings = async () => {
            try {
                const response = await fetch('/api/bookings');
                if (!response.ok) throw new Error('Network response was not ok');
                const data = await response.json();
                setBookings(data.bookings);
            } catch (error) {
                console.error('Failed to fetch bookings:', error);
            }
        };

        fetchBookings();
    }, []);

    useEffect(() => {
        if (selectedDate) {
            const checkAvailability = () => {
                const bookingsForDate = bookings.filter(
                    (booking) => new Date(booking.date).toDateString() === selectedDate.toDateString()
                );

                const mixdownBookings = bookingsForDate.filter((booking) => booking.type.includes('Mixdown'));
                const masteringBookings = bookingsForDate.filter((booking) => booking.type.includes('Mastering'));

                const mixdownAvailable = mixdownBookings.length === 0;
                const masteringAvailable = masteringBookings.length < 4 && mixdownAvailable;

                setAvailableServices({
                    mixdownWithFeedback: mixdownAvailable,
                    mixdownNoFeedback: mixdownAvailable,
                    masteringWithFeedback: masteringAvailable,
                    masteringNoFeedback: masteringAvailable
                });
            };

            checkAvailability();
        }
    }, [selectedDate, bookings]);

    const handleServiceSelection = (service: string) => {
        setSelectedService(service);
        if (!session) {
            signIn(undefined, { callbackUrl: '/checkout' });
        }
    };

    const isDateAvailable = (date: Date) => {
        const today = new Date();
        today.setHours(0, 0, 0, 0); // Set to midnight to compare only the date part

        if (date < today) return false; // Only allow future dates

        const day = date.getDay();
        if (day === 0 || day === 6) return false;

        const bookingsForDate = bookings.filter(
            (booking) => new Date(booking.date).toDateString() === date.toDateString()
        );

        const mixdownBookings = bookingsForDate.filter((booking) => booking.type.includes('Mixdown'));
        const masteringBookings = bookingsForDate.filter((booking) => booking.type.includes('Mastering'));

        if (mixdownBookings.length >= 1) return false;
        if (masteringBookings.length >= 4) return false;

        return true;
    };

    const handleCheckout = async () => {
        if (!selectedDate || !selectedService) return;

        const stripe = await stripePromise;
        const response = await fetch('/api/checkout_sessions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                date: selectedDate,
                service: selectedService,
            }),
        });

        const session = await response.json();
        if (stripe) {
            await stripe.redirectToCheckout({ sessionId: session.id });
        } else {
            console.error('Stripe initialization failed.');
        }
    };

    return (
        <div className="p-4">
            <h2 className="text-3xl font-bold mb-4">Book a Session</h2>
            <p>Select a date for your session:</p>
            <Calendar
                onChange={(value) => setSelectedDate(value as Date)}
                value={selectedDate}
                tileDisabled={({ date }) => !isDateAvailable(date)}
            />
            {selectedDate && (
                <>
                    <p>Select a service type:</p>
                    <div className="flex flex-col mb-4 space-y-2">
                        <button
                            className={`p-2 border ${selectedService === 'Stems Mixdown (with detailed feedback)' ? 'bg-blue-500 text-white' : 'bg-white text-black'}`}
                            onClick={() => handleServiceSelection('Stems Mixdown (with detailed feedback)')}
                            disabled={!availableServices.mixdownWithFeedback}
                        >
                            Stems Mixdown (with detailed feedback): $250AUD
                        </button>
                        <button
                            className={`p-2 border ${selectedService === 'Stems Mixdown (no feedback)' ? 'bg-blue-500 text-white' : 'bg-white text-black'}`}
                            onClick={() => handleServiceSelection('Stems Mixdown (no feedback)')}
                            disabled={!availableServices.mixdownNoFeedback}
                        >
                            Stems Mixdown (no feedback): $200AUD
                        </button>
                        <button
                            className={`p-2 border ${selectedService === 'Mastering (with detailed feedback)' ? 'bg-blue-500 text-white' : 'bg-white text-black'}`}
                            onClick={() => handleServiceSelection('Mastering (with detailed feedback)')}
                            disabled={!availableServices.masteringWithFeedback}
                        >
                            Mastering (with detailed feedback): $40AUD
                        </button>
                        <button
                            className={`p-2 border ${selectedService === 'Mastering (no feedback)' ? 'bg-blue-500 text-white' : 'bg-white text-black'}`}
                            onClick={() => handleServiceSelection('Mastering (no feedback)')}
                            disabled={!availableServices.masteringNoFeedback}
                        >
                            Mastering (no feedback): $30AUD
                        </button>
                    </div>
                </>
            )}
            {selectedService && (
                !session ? (
                    <div className="flex space-x-4">
                        <button
                            onClick={() => signIn(undefined, { callbackUrl: '/checkout' })}
                            className="bg-blue-500 text-white px-4 py-2 mt-2"
                        >
                            Sign In
                        </button>
                    </div>
                ) : (
                    <button
                        onClick={() => handleCheckout()}
                        className="bg-blue-500 text-white px-4 py-2 mt-2"
                    >
                        Proceed to Checkout
                    </button>
                )
            )}
        </div>
    );
};

export default Bookings;