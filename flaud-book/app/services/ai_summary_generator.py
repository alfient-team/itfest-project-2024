from json import JSONDecodeError

import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()

# Константы
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
PROMPT = f"""You are a helpful assistant that returns answers strictly in JSON format. The user will provide a request describing the kind of books they want. Given the user’s request, you must:

1. Identify the language of the user’s request.  
2. Recommend exactly 5 real, existing books that match the user’s description AND have been published or translated into the same language as the user’s request.  
3. Rank them in ascending order of suitability (1 is the best match, 5 is the least good match).

Your response must be a strictly valid JSON object. The JSON object must have numeric keys "1", "2", "3", "4", "5" (as strings). Each of these keys must map to a JSON object representing a book. That object must have the following fields:

- "title": The exact title of the real book.
- "author": The real author of the book.
- "summary": A friendly, easy-to-understand summary of the book’s relevance to the user’s request, between 100 and 200 words. It should help the user understand why this book suits their needs.
- "reason": A short explanation (1-2 sentences) of why this book matches the user’s request criteria.

If there are no real books meeting these criteria (either thematically or in terms of translation availability), return an empty JSON object .

Do not include any text outside of the JSON object. Do not provide non-existent or fabricated books. If uncertain about a book's availability in the request’s language, do not include it.

Your entire response must be in English.
"""

def get_books_from_openai(prompt: str) -> str:
    """
    Отправляет запрос к OpenAI, используя заданный промпт, и возвращает ответ в JSON-формате.
    Предполагается, что промпт заставит модель вернуть уже структурированный JSON.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    response.raise_for_status()

    completion_data = response.json()
    # Обычно content находится в completion_data['choices'][0]['message']['content']
    content = completion_data['choices'][0]['message']['content']

    return content


if __name__ == "__main__":
    # Вызываем функцию с нашим PROMPT
    #user_prompt = """
    #Нужны книги от авторов, получивших Нобелевскую премию, рассматривающие экологические проблемы и взаимоотношения человека и природы, с научными аргументами и примерами.
    #"""
    
    #user_prompt = """
    #We need books from Nobel Prize-winning authors addressing environmental issues and human-nature relations, with scientific arguments and examples.
    #"""

    user_prompt = """
    I want to find a book for my professional carrer development in IT or specially in Backend side of web development, I want to became a Senior, Tech lead, Head of Backend and in the end of all Solution Architect. Give me a technical and also development in soft skill books. Also additional with books that provides how to sell yourself, how to pass an interview, road to FAANG and algorithms with data structures, system design questions and tasks.
    """
    
    books_text = get_books_from_openai(user_prompt)

    # Печатаем полученный JSON
    try:
        if books_text.startswith("```json"):
            books_text = books_text[7:]
        if books_text.endswith("```"):
            books_text = books_text[:-3]
        books_json = json.loads(books_text)
        print(json.dumps(books_json, indent=2, ensure_ascii=False))
    except JSONDecodeError:
        print("JSONERROR:\n", books_text)