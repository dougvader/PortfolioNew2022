import React from 'react';
import Link from 'next/link';

const Navbar: React.FC = () => {
    return (
        <nav className="flex justify-between items-center p-4 bg-gray-800 text-white">
            <div className="text-xl">
                <Link href="/">MixMaster</Link>
            </div>
            <ul className="flex space-x-4">
                <li>
                    <Link href="#services">Services</Link>
                </li>
                <li>
                    <Link href="#portfolio">Testimonials</Link>
                </li>
                <li>
                    <Link href="#contact">Contact</Link>
                </li>
            </ul>
        </nav>
    );
};

export default Navbar;