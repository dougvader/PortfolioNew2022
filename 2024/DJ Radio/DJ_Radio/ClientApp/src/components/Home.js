import Player from './Player';
import React from 'react';

// Assuming you have a URL for your Icecast server stream
    const streamUrl = 'http://localhost:8000/stream';

const Home = () => {
    return (
            <div className="home-page">
                <h1>Welcome to Our Internet Radio Station!</h1>
                <Player url={streamUrl} />
                <p>More content for your home page...</p>
            </div>
        );
    };

export default Home;