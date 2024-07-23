"use client";

import React, { useEffect, useState } from 'react';
import { useSession, signIn, signOut } from 'next-auth/react';

const Profile: React.FC = () => {
    const { data: session, status } = useSession();
    const [bookings, setBookings] = useState([]);
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const [receivedFiles, setReceivedFiles] = useState([]);

    useEffect(() => {
        if (session) {
            fetchBookings();
            fetchFiles();
        }
    }, [session]);

    useEffect(() => {
        console.log('Session data:', session);
        console.log('Session status:', status);
    }, [session, status]);

    const fetchBookings = async () => {
        try {
            const response = await fetch('/api/bookings');
            const data = await response.json();
            setBookings(data.bookings);
        } catch (error) {
            console.error('Failed to fetch bookings:', error);
        }
    };

    const fetchFiles = async () => {
        try {
            const response = await fetch('/api/files');
            const data = await response.json();
            setUploadedFiles(data.uploadedFiles);
            setReceivedFiles(data.receivedFiles);
        } catch (error) {
            console.error('Failed to fetch files:', error);
        }
    };

    if (!session) {
        return (
            <div>
                <p>You need to be signed in to view this page.</p>
                <button onClick={() => signIn()}>Sign In</button>
            </div>
        );
    }

    return (
        <div>
            <h2 className="text-3xl font-bold mb-4">User Profile</h2>
            <button onClick={() => signOut()}>Sign Out</button>

            <h3 className="text-2xl font-bold mt-4">Your Orders</h3>
            <ul>
                {bookings.map((booking: { id: string; service: string; date: string }) => (
                    <li key={booking.id}>{booking.service} - {new Date(booking.date).toLocaleDateString()}</li>
                ))}
            </ul>

            <h3 className="text-2xl font-bold mt-4">Uploaded Files</h3>
            <ul>
                {uploadedFiles.map((file: { id: string; url: string; name: string }) => (
                    <li key={file.id}>
                        <a href={file.url} download>{file.name}</a>
                    </li>
                ))}
            </ul>

            <h3 className="text-2xl font-bold mt-4">Received Files</h3>
            <ul>
                {receivedFiles.map((file: { id: string; url: string; name: string }) => (
                    <li key={file.id}>
                        <a href={file.url} download>{file.name}</a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Profile;