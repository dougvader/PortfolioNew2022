import React from 'react';
import Image from 'next/image';

const Services: React.FC = () => {
    return (
        <div>
            <h3 className="text-3xl font-bold mt-4 py-5">Services</h3>
            <div className="flex justify-center items-center space-x-8">
                <div className="text-center">
                    <Image src="/images/mixing.jpg" alt="Mixing" width={500} height={300} className="w-full h-auto" />
                    <h3 className="text-xl font-bold mt-4">Mixing</h3>
                </div>
                <div className="text-center">
                    <Image src="/images/mastering.jpg" alt="Mastering" width={500} height={300} className="w-full h-auto" />
                    <h3 className="text-xl font-bold mt-4">Mastering</h3>
                </div>
            </div>
        </div>
    );
};

export default Services;
