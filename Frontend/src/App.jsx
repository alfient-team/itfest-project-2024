import React, { useState } from 'react'
import './App.css'
import Header from './components/Header/Header'
import BookCardList from './components/BookCardList/BookCardList'

function App() {
    const [searchActive, setSearchActive] = useState(false)

    const handleSearch = () => {
        setSearchActive(true)
    }

    return (
        <div className="App">
            <Header onSearch={handleSearch}/>
            {searchActive && <BookCardList />}
        </div>
    )
}

export default App
