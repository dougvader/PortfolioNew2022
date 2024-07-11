import React from 'react';

const Footer: React.FC = () => {
    return (
        <footer className="text-center py-4 bg-gray-800 text-white">
            <p>&copy; {new Date().getFullYear()} Mixing & Mastering Services. All rights reserved.</p>
            <ul className="flex justify-center space-x-4 mt-2">
                <li>
                    <a href="#privacy" className="hover:underline">Privacy Policy</a>
                </li>
                <li>
                    <a href="#terms" className="hover:underline">Terms of Service</a>
                </li>
            </ul>
        </footer>
    );
};

export default Footer;
