// src/components/SearchBar/SearchBar.jsx
import React from 'react';
import './SearchBar.css';

function SearchBar({ onSearch, value, onChange }) {
    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            onSearch();
        }
    }

    return (
        <div className="searchbar-wrapper">
            <input
                className="searchbar-input"
                type="text"
                placeholder="Что бы почитать..."
                value={value}
                onChange={onChange}
                onKeyPress={handleKeyPress}
            />
            <span className="searchbar-icon" onClick={onSearch}>🔍</span>
        </div>
    );
}

export default SearchBar;
