// src/mockData.js

export const USE_MOCK = true; // Установи true для использования мока, false для реального запроса

export const mockResponse = {
    book_list: [
        {
            id: 1,
            book: {
                title: "Cracking the Coding Interview",
                author: "Gayle Laakmann McDowell",
                image_link: "https://via.placeholder.com/600x400?text=Book+1"
            },
            generated_summary: "This book is a comprehensive guide for anyone preparing for programming interviews.",
            generated_reason: "Ideal for"
        },
        {
            id: 2,
            book: {
                title: "You Don’t Know JS",
                author: "Kyle Simpson",
                image_link: "https://via.placeholder.com/600x400?text=Book+2"
            },
            generated_summary: "A deep dive into JavaScript fundamentals, explaining core concepts in detail.",
            generated_reason: "Essential for"
        }
    ]
};
