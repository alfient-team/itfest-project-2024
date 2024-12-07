// src/App.jsx
import React, { useState } from 'react';
import './App.css';
import Header from './components/Header/Header';
import BookCardList from './components/BookCardList/BookCardList';

function App() {
    const [query, setQuery] = useState('');

    const handleSearch = (searchQuery) => {
        setQuery(searchQuery);
    }

    return (
        <div className="App">
            <Header onSearch={handleSearch} />
            {query && <BookCardList query={query} />}
        </div>
    );
}

export default App;
