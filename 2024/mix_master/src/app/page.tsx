"use client";

import React from 'react';
import Header from '../components/Header';
import Services from '../components/Services';
import Testimonials from '../components/Testimonials';
import Bookings from '../components/Bookings';
import Pricing from '../components/Pricing';

const HomePage: React.FC = () => {
    return (
        <div>
            <Header />
            <section id="services" className="py-5 bg-white">
                <div className="container mx-auto px-4">
                    <Services />
                </div>
            </section>
            <section id="testimonials" className="py-5 bg-gray-100">
                <div className="container mx-auto px-4">
                    <Testimonials />
                </div>
            </section>
            <section id="pricing" className="py-5 bg-gray-100">
                <div className="container mx-auto px-4">
                    <Pricing />
                </div>
            </section>
            <section id="bookings" className="py-5 bg-white">
                <div className="container mx-auto px-4">
                    <Bookings />
                </div>
            </section>
        </div>
    );
};

export default HomePage;
