"use client";

import React, { useState } from 'react';

const FileUpload: React.FC = () => {
    const [files, setFiles] = useState<FileList | null>(null);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFiles(e.target.files);
    };

    const handleUpload = async () => {
        if (!files) return;

        const formData = new FormData();
        Array.from(files).forEach((file) => {
            formData.append('files', file);
        });

        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            alert('Files uploaded successfully!');
        } else {
            alert('Failed to upload files.');
        }
    };

    return (
        <div className="container mx-auto px-4 py-10">
            <h2 className="text-3xl font-bold mb-4">Upload Your Tracks/Files</h2>
            <input type="file" multiple onChange={handleFileChange} className="mb-4" />
            <button onClick={handleUpload} className="bg-blue-500 text-white px-4 py-2 rounded">
                Upload
            </button>
        </div>
    );
};

export default FileUpload;
