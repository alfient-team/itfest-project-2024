import React from 'react';
import './BookCard.css';

function BookCard({ data, style }) {
    const { title, author, photo_link, summary, reason } = data;

    return (
        <div className="bookcard" style={style}>
            <img src={photo_link} alt={`${title} cover`} className="bookcard-image" />
            <div className="bookcard-overlay">
                {reason && <span className="bookcard-reason">{reason}</span>}
                <h2 className="bookcard-title">{title}</h2>
                <p className="bookcard-author">{author}</p>
                <p className="bookcard-summary">{summary}</p>
            </div>
        </div>
    );
}

export default BookCard;
