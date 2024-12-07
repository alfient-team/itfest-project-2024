import React, { useState } from 'react';
import './SearchBar.css';

function SearchBar({ onSearch }) {
    const [value, setValue] = useState('');

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            onSearch(value);
        }
    };

    const handleClick = () => {
        onSearch(value);
    };

    return (
        <div className="searchbar-wrapper">
            <input
                className="searchbar-input"
                type="text"
                placeholder="Что бы почитать..."
                value={value}
                onChange={(e) => setValue(e.target.value)}
                onKeyPress={handleKeyPress}
            />
            <span className="searchbar-icon" onClick={handleClick}>🔍</span>
        </div>
    );
}

export default SearchBar;
