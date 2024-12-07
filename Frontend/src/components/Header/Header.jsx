// src/components/Header/Header.jsx
import React, { useState } from 'react';
import './Header.css';
import SearchBar from '../SearchBar/SearchBar';

function Header({ onSearch }) {
    const [query, setQuery] = useState('');

    const handleSearch = () => {
        if (query.trim() !== '') {
            onSearch(query);
        }
    }

    return (
        <header className="header">
            <h1 className="header-title">Найди свою следующую книгу...</h1>
            <SearchBar
                onSearch={handleSearch}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
            />
        </header>
    );
}

export default Header;
