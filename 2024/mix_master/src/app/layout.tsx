import React from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import '../app/globals.css';
import SessionWrapper from '../components/SessionWrapper';

const RootLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    return (
        <html lang="en">
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <title>Mixing & Mastering Services</title>
            </head>
            <body className="flex flex-col min-h-screen">
                <SessionWrapper>
                    <Navbar />
                    <main className="flex-grow">{children}</main>
                    <Footer />
                </SessionWrapper>
            </body>
        </html>
    );
};

export default RootLayout;
