import React from 'react'
import './BookCardList.css'
import BookCard from '../BookCard/BookCard'

const mockData = [
    {
        title: "Унесенные ветром",
        author: "Маргарет Митчелл",
        photo_link: "https://simg.marwin.kz/media/catalog/product/cache/41deb699a7fea062a8915debbbb0442c/c/o/mitchell_m_unesennye_vetrom_t_1.jpg",
        summary: "История любви и выживания во времена Гражданской войны в США.",
        reason: "Рекомендовано"
    },
    {
        title: "Мастер и Маргарита",
        author: "Михаил Булгаков",
        photo_link: "https://simg.marwin.kz/media/catalog/product/c/o/cover1_38_215.jpg",
        summary: "Сатирический роман о дьяволе в Москве, любви и свободе.",
        reason: "Выбрано для вас"
    },
    // Добавь больше книг по необходимости
]
function BookCardList() {
    return (
        <div className="bookcard-list">
            {mockData.map((book, idx) => (
                <BookCard key={idx} data={book} style={{ '--i': idx }} />
            ))}
        </div>
    );
}

export default BookCardList
