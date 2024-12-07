import React, { useState } from 'react';
import './App.css';
import Header from './components/Header/Header';
import BookCardList from './components/BookCardList/BookCardList';

function transformBookList(data) {
    // Проверяем, что входные данные содержат ключ `book_list` и это массив
    if (!data.book_list || !Array.isArray(data.book_list)) {
        throw new Error("Неверный формат данных: ожидается ключ `book_list` с массивом.");
    }

    // Используем метод `map` для преобразования каждого элемента массива
    return data.book_list.map(item => {
        // Проверяем наличие необходимых полей
        if (!item.book || !item.book.title || !item.book.author || !item.book.image_link) {
            throw new Error("Неверный формат книги: отсутствуют необходимые поля.");
        }

        return {
            title: item.book.title, // Название книги
            author: item.book.author, // Автор книги
            photo_link: item.book.image_link, // Ссылка на изображение книги
            summary: item.generated_summary, // Сгенерированное резюме
            reason: item.generated_reason // Сгенерированная причина
        };
    });
}

// Пример использования:

const inputData = {
    "book_list": [
        {
            "id": 4,
            "book": {
                "title": "Soft Skills: The software developer's life manual",
                "author": "Gayle Laakmann McDowell",
                "image_link": "https://vk-cloud-prod.hb.kz-ast.bizmrg.com/book_images/5.jpg"
            },
            "generated_summary": "This book covers the often-overlooked non-technical skills required for career advancement in IT. It addresses personal branding, productivity, career development, and interviewing skills. The insights offered help in personal development and in building the soft skills necessary for leadership roles. For those looking to become a Tech Lead or Head of Backend, it provides guidance on improving communication, leadership, and other interpersonal skills that are crucial in managing teams and projects.",
            "generated_reason": "It provides comprehensive coverage of essential soft skills needed for leadership roles in IT."
        }
    ]
};

function App() {
    const [books, setBooks] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');

    const handleSearch = async (query) => {
        setSearchTerm(query);
        if (!query.trim()) {
            setBooks([]);
            return;
        }
        setLoading(true);
        setError(null);
        try {
            // Замените URL на ваш реальный бэкенд-эндпоинт
            const response = await fetch(`http://localhost:8000/books/recommends/${encodeURIComponent(query)}`);
            if (!response.ok) {
                throw new Error('Ошибка сети');
            }
            const json_data = await response.json()
            console.log(json_data)
            console.log(transformBookList(json_data))
            const data = transformBookList(json_data);
            setBooks(data);
        } catch (err) {
            setError(err.message || 'Что-то пошло не так');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="App">
            <Header onSearch={handleSearch} />
            {loading && <p>Загрузка...</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {!loading && !error && books.length > 0 && <BookCardList books={books} />}
            {!loading && !error && searchTerm && books.length === 0 && (
                <p>Книги не найдены</p>
            )}
        </div>
    );
}

export default App;
