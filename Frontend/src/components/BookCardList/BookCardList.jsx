import React from 'react';
import './BookCardList.css';
import BookCard from '../BookCard/BookCard';

function BookCardList({ books }) {
    return (
        <div className="bookcard-list">
            {books.map((book, idx) => (
                <BookCard key={idx} data={book} style={{ '--i': idx }} />
            ))}
        </div>
    );
}

export default BookCardList;
