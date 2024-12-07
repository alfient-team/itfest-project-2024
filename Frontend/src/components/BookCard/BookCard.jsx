import React from 'react';
import './BookCard.css';

function BookCard({ data, style }) {
    const { book, generated_summary, generated_reason } = data;
    const { title, author, image_link } = book;

    return (
        <div className="bookcard" style={style}>
            <img src={image_link} alt={`${title} cover`} className="bookcard-image" />
            <div className="bookcard-overlay">
                {generated_reason && <span className="bookcard-reason">{generated_reason}</span>}
                <h2 className="bookcard-title">{title}</h2>
                <p className="bookcard-author">{author}</p>
                <p className="bookcard-summary">{generated_summary}</p>
            </div>
        </div>
    );
}

export default BookCard;
