"use client";

import React from 'react';

const Confirmed: React.FC = () => {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold">Email Confirmed</h1>
      <p>Your email address has been successfully confirmed. You can now sign in.</p>
      <a href="/auth/signin" className="text-blue-500">Sign In</a>
    </div>
  );
};

export default Confirmed;
