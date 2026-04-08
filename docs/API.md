# API эндпоинты

## Базовый URL

## Список эндпоинтов

| Метод | URL | Описание |
| ------|-----|----------|
| GET | '/courses' | Список всех курсов |

## GET /courses/

### Параметры
- `?page=1` - номер страницы
- ...

### Пример ответа (200 OK)

``` json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Test Course 1",
            "description": "Test Course 1. Description.",
            "price": "100.00",
            "lessons_count": 2,
            "created_at": "2026-04-07T21:27:14.382578Z",
            "author": "author"
        },
    ]
}
```
