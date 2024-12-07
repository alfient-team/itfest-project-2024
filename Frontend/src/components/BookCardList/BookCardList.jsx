// src/components/BookCardList/BookCardList.jsx
import React, { useEffect, useState } from 'react';
import './BookCardList.css';
import BookCard from '../BookCard/BookCard';
import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';

function BookCardList({ query }) {
    const [loading, setLoading] = useState(false);
    const [books, setBooks] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (query) {
            setLoading(true);
            setError(null);

            // Создаем AbortController для отмены запроса при необходимости
            const controller = new AbortController();
            const signal = controller.signal;

            // Устанавливаем таймаут для задержки в 30 секунд
            const timeoutId = setTimeout(() => {
                controller.abort(); // Отменяем запрос после 30 секунд
                setError('Запрос превысил время ожидания. Попробуйте позже.');
                setLoading(false);
            }, 30000); // 30000 миллисекунд = 30 секунд

            // Выполняем GET-запрос
            fetch(`https://your-api-endpoint.com/books?search=${encodeURIComponent(query)}`, { signal })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Сетевая ошибка');
                    }
                    return response.json();
                })
                .then(data => {
                    clearTimeout(timeoutId); // Очищаем таймаут, если запрос завершился вовремя
                    setBooks(data);
                    setLoading(false);
                })
                .catch(error => {
                    if (error.name === 'AbortError') {
                        console.log('Запрос был отменен из-за превышения времени ожидания.');
                    } else {
                        console.error('Ошибка при загрузке данных:', error);
                        setError('Ошибка при загрузке данных. Попробуйте позже.');
                        setLoading(false);
                    }
                });

            // Очистка таймаута и отмена запроса при размонтировании компонента или изменении запроса
            return () => {
                clearTimeout(timeoutId);
                controller.abort();
            };
        }
    }, [query]);

    return (
        <div className="bookcard-list">
            {loading ? (
                // Отображаем скелетоны
                Array(1).fill().map((_, idx) => (
                    <div className="bookcard-skeleton" key={idx}>
                        <Skeleton height={200} />
                        <Skeleton height={30} style={{ marginTop: '10px' }} />
                        <Skeleton height={20} width="60%" />
                        <Skeleton height={15} count={2} style={{ marginTop: '10px' }} />
                        <Skeleton height={25} width="30%" style={{ marginTop: '10px' }} />
                    </div>
                ))
            ) : error ? (
                // Отображаем сообщение об ошибке
                <p style={{ color: '#fff', marginTop: '20px' }}>{error}</p>
            ) : (
                books.length > 0 ? books.map((book, idx) => (
                    <BookCard key={idx} data={book} style={{ '--i': idx }} />
                )) : <p style={{ color: '#fff', marginTop: '20px' }}>Книги не найдены</p>
            )}
        </div>
    );
}

export default BookCardList;
