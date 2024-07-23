"use client";

import { SessionProvider } from 'next-auth/react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import '../app/globals.css';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <html lang="en">
      <head>
        <title>Mixing & Mastering Services</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body className="flex flex-col min-h-screen">
        <SessionProvider session={null}>
          <Navbar session={null} />
          <main className="flex-grow">{children}</main>
          <Footer />
        </SessionProvider>
      </body>
    </html>
  );
};

export default Layout;