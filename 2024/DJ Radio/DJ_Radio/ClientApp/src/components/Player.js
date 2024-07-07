import React from 'react';
import ReactPlayer from './react-player';

const Player = ({ url }) => {
    return (
        <div className="player">
            <ReactPlayer url={url} playing controls />
        </div>
    );
}

export default Player;