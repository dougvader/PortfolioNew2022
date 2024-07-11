"use client";

import { SessionProvider } from "next-auth/react";
import { GuestCheckoutProvider } from './GuestCheckoutContext';

const SessionWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    return (
        <SessionProvider>
            <GuestCheckoutProvider>
                {children}
            </GuestCheckoutProvider>
        </SessionProvider>
    );
};

export default SessionWrapper;
