import React from 'react';

const Header: React.FC = () => {
    return (
        <header className="text-center py-5 bg-gray-100">
            <h1 className="text-4xl font-bold text-gray-800 py-5">Welcome to MixMaster</h1>
            <div className="flex justify-center">
                <img src="/images/logo.png" alt="Mixing" className="w-1/4 h-auto" />
            </div>
            <p className="text-lg text-gray-600 mt-4">Your music, professionally mixed and mastered to perfection.</p>
        </header>
    );
};

export default Header;
