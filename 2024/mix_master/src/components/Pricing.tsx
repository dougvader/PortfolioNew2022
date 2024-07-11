import React from 'react';

const Pricing: React.FC = () => {
    return (
        <div>
            <h2 className="text-3xl font-bold mb-4">Pricing</h2>
            <ul>
                <li>Stems Mixdown (with detailed feedback): $250AUD</li>
                <li>Stems Mixdown (no feedback): $200AUD</li>
                <li>Mastering (with detailed feedback): $40AUD</li>
                <li>Mastering (no feedback): $30AUD</li>
            </ul>
        </div>
    );
};

export default Pricing;