import React from 'react'
import './Header.css'
import SearchBar from '../SearchBar/SearchBar'

function Header({ onSearch }) {
    return (
        <header className="header">
            <h1 className="header-title">Найди свою следующую книгу...</h1>
            <SearchBar onSearch={onSearch} />
        </header>
    )
}

export default Header
