"use client";

import React, { useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import { useSession, signIn, signOut } from 'next-auth/react';
import { loadStripe } from '@stripe/stripe-js';
import { useGuestCheckout } from './GuestCheckoutContext';

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY);

const Bookings: React.FC = () => {
    const [date, setDate] = useState<Date | null>(null);
    const [service, setService] = useState<{ name: string, price: number, feedback: boolean } | null>(null);
    const { data: session } = useSession();
    const { guestInfo, setGuestInfo } = useGuestCheckout();

    const handleDateChange = (date: Date) => {
        setDate(date);
    };

    const handleServiceSelect = (name: string, price: number, feedback: boolean) => {
        setService({ name, price, feedback });
    };

    const handleCheckout = async () => {
        const stripe = await stripePromise;
        const response = await fetch('/api/checkout_sessions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                items: [{ name: service.name, price: service.price * 100, quantity: 1 }],
            }),
        });

        const { sessionId } = await response.json();

        const { error } = await stripe.redirectToCheckout({ sessionId });
        if (error) {
            console.error('Stripe checkout error:', error);
        }
    };

    const handleGuestCheckout = () => {
        const guestEmail = prompt("Please enter your email for guest checkout:");
        if (guestEmail) {
            setGuestInfo({ email: guestEmail });
            handleCheckout();
        }
    };

    return (
        <div>
            <h2 className="text-3xl font-bold mb-4">Book a Session</h2>
            <p>Select a date for your session:</p>
            <Calendar onChange={handleDateChange} value={date} />
            {date && (
                <div>
                    <p className="mt-4">Selected Date: {date.toDateString()}</p>
                    <p>Select a service:</p>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                        <button onClick={() => handleServiceSelect('Stems Mixdown (with detailed feedback)', 250, true)} className="bg-blue-500 text-white px-4 py-2 rounded">
                            Stems Mixdown (with detailed feedback): $250AUD
                        </button>
                        <button onClick={() => handleServiceSelect('Stems Mixdown (no feedback)', 200, false)} className="bg-blue-500 text-white px-4 py-2 rounded">
                            Stems Mixdown (no feedback): $200AUD
                        </button>
                        <button onClick={() => handleServiceSelect('Mastering (with detailed feedback)', 40, true)} className="bg-blue-500 text-white px-4 py-2 rounded">
                            Mastering (with detailed feedback): $40AUD
                        </button>
                        <button onClick={() => handleServiceSelect('Mastering (no feedback)', 30, false)} className="bg-blue-500 text-white px-4 py-2 rounded">
                            Mastering (no feedback): $30AUD
                        </button>
                    </div>
                    {service && (
                        <div className="mt-4">
                            <p>Selected Service: {service.name} - ${service.price}AUD</p>
                            {!session ? (
                                <div className="mt-4">
                                    <button onClick={() => signIn('google')} className="mr-4 bg-blue-500 text-white px-4 py-2 rounded">
                                        Log In with Google
                                    </button>
                                    <button onClick={handleGuestCheckout} className="bg-gray-500 text-white px-4 py-2 rounded">
                                        Continue as Guest
                                    </button>
                                </div>
                            ) : (
                                <div className="mt-4">
                                    <button onClick={handleCheckout} className="bg-green-500 text-white px-4 py-2 rounded">
                                        Proceed to Checkout
                                    </button>
                                    <button onClick={() => signOut()} className="bg-red-500 text-white px-4 py-2 rounded ml-4">
                                        Sign Out
                                    </button>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default Bookings;
