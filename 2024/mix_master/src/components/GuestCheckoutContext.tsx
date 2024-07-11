"use client";

import React, { createContext, useContext, useState } from 'react';

const GuestCheckoutContext = createContext(null);

export const useGuestCheckout = () => {
    return useContext(GuestCheckoutContext);
};

export const GuestCheckoutProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [guestInfo, setGuestInfo] = useState(null);

    return (
        <GuestCheckoutContext.Provider value={{ guestInfo, setGuestInfo }}>
            {children}
        </GuestCheckoutContext.Provider>
    );
};
