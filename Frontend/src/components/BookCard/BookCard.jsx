import React from 'react';
import './BookCard.css';

function BookCard({ data, style }) {
    const { title, author, photo_link, summary, reason } = data;

    return (
        <div className="bookcard" style={style}>
            <div className="bookcard-image-container">
                <img src={photo_link} alt={`${title} cover`} className="bookcard-image" />
            </div>
            <div className="bookcard-content">
                {reason && <span className="bookcard-reason">{reason}</span>}
                <h2 className="bookcard-title">{title}</h2>
                <p className="bookcard-author">{author}</p>
                <p className="bookcard-summary">{summary}</p>
            </div>
        </div>
    );
}

export default BookCard;
