"use client";

import React from 'react';
import Link from 'next/link';
import { signIn, signOut } from 'next-auth/react';
import { Session } from 'next-auth';

const Navbar: React.FC<{ session: Session | null }> = ({ session }) => {
    const handleSignIn = () => signIn();
    const handleSignOut = () => signOut();

    console.log('Navbar session:', session); // Debugging

    return (
        <nav className="bg-gray-800 p-4 text-white flex justify-between">
            <div className="flex space-x-4">
                <Link href="/" legacyBehavior>
                    <a className="hover:underline">Home</a>
                </Link>
                <Link href="#services" legacyBehavior>
                    <a className="hover:underline">Services</a>
                </Link>
                <Link href="#bookings" legacyBehavior>
                    <a className="hover:underline">Bookings</a>
                </Link>
                <Link href="#testimonials" legacyBehavior>
                    <a className="hover:underline">Testimonials</a>
                </Link>
            </div>
            <div className="flex space-x-4">
                {session ? (
                    <>
                        <Link href="/profile" legacyBehavior>
                            <a className="hover:underline">Profile</a>
                        </Link>
                        <button onClick={handleSignOut} className="hover:underline">
                            Sign Out
                        </button>
                    </>
                ) : (
                    <button onClick={handleSignIn} className="hover:underline">
                        Sign In
                    </button>
                )}
            </div>
        </nav>
    );
};

export default Navbar;