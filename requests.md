Руководство по тестированию Django API в Postman
Предварительная настройка
1. Создание коллекции в Postman
Откройте Postman
Создайте новую коллекцию: Django News API
В настройках коллекции создайте переменные:
baseUrl: http://localhost:8000 (или ваш домен)
access_token: (будет заполняться автоматически)
refresh_token: (будет заполняться автоматически)
test_user_id: (будет заполняться автоматически)
2. Запуск Django сервера
bash
python manage.py runserver
ЧАСТЬ 1: ТЕСТИРОВАНИЕ АУТЕНТИФИКАЦИИ (ACCOUNTS APP)
1. Регистрация пользователя
Метод: POST
URL: {{baseUrl}}/api/v1/auth/register/
Headers:

Content-Type: application/json
Body (JSON):

json
{
    "email": "test@example.com",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "password": "TestPassword123!",
    "password_confirm": "TestPassword123!"
}
Ожидаемый ответ (201 Created):

json
{
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "full_name": "Test User",
        "avatar": null,
        "bio": "",
        "created_at": "2025-08-27T12:00:00Z",
        "updated_at": "2025-08-27T12:00:00Z",
        "posts_count": 0,
        "comments_count": 0
    },
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "message": "User registered successfully"
}
Test Script (Tests tab):

javascript
pm.test("Registration successful", function () {
    pm.response.to.have.status(201);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('access');
    pm.expect(responseJson).to.have.property('refresh');
    pm.expect(responseJson.user).to.have.property('id');
    
    // Сохраняем токены и ID пользователя
    pm.collectionVariables.set("access_token", responseJson.access);
    pm.collectionVariables.set("refresh_token", responseJson.refresh);
    pm.collectionVariables.set("test_user_id", responseJson.user.id);
});
2. Вход в систему
Метод: POST
URL: {{baseUrl}}/api/v1/auth/login/
Headers:

Content-Type: application/json
Body (JSON):

json
{
    "email": "test@example.com",
    "password": "TestPassword123!"
}
Test Script:

javascript
pm.test("Login successful", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('access');
    pm.expect(responseJson).to.have.property('refresh');
    
    // Обновляем токены
    pm.collectionVariables.set("access_token", responseJson.access);
    pm.collectionVariables.set("refresh_token", responseJson.refresh);
});
3. Просмотр профиля
Метод: GET
URL: {{baseUrl}}/api/v1/auth/profile/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
4. Обновление профиля
Метод: PATCH
URL: {{baseUrl}}/api/v1/auth/profile/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "first_name": "UpdatedTest",
    "bio": "This is my updated bio"
}
5. Смена пароля
Метод: PUT
URL: {{baseUrl}}/api/v1/auth/change-password/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "old_password": "TestPassword123!",
    "new_password": "NewPassword123!",
    "new_password_confirm": "NewPassword123!"
}
ЧАСТЬ 2: ТЕСТИРОВАНИЕ ОСНОВНОГО ФУНКЦИОНАЛА (MAIN APP)
6. Создание категории
Метод: POST
URL: {{baseUrl}}/api/v1/posts/categories/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "name": "Technology",
    "description": "Posts about technology and innovations"
}
Ожидаемый ответ (201 Created):

json
{
    "id": 1,
    "name": "Technology",
    "slug": "technology",
    "description": "Posts about technology and innovations",
    "posts_count": 0,
    "created_at": "2025-08-29T12:00:00Z"
}
Test Script:

javascript
pm.test("Category created successfully", function () {
    pm.response.to.have.status(201);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('id');
    pm.expect(responseJson.slug).to.eql('technology');
    
    // Сохраняем ID категории
    pm.collectionVariables.set("category_id", responseJson.id);
    pm.collectionVariables.set("category_slug", responseJson.slug);
});
7. Получение списка категорий
Метод: GET
URL: {{baseUrl}}/api/v1/posts/categories/
Headers:

Content-Type: application/json
Test Script:

javascript
pm.test("Categories list retrieved", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson.results).to.be.an('array');
});
8. Получение конкретной категории
Метод: GET
URL: {{baseUrl}}/api/v1/posts/categories/{{category_slug}}/
Headers:

Content-Type: application/json
9. Создание поста
Метод: POST
URL: {{baseUrl}}/api/v1/posts/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "title": "My First Tech Post",
    "content": "This is a comprehensive article about the latest technology trends. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
    "category": {{category_id}},
    "status": "published"
}
Ожидаемый ответ (201 Created):

json
{
    "id": 1,
    "title": "My First Tech Post",
    "slug": "my-first-tech-post",
    "content": "This is a comprehensive article about...",
    "image": null,
    "category": 1,
    "author": 1,
    "status": "published",
    "created_at": "2025-08-29T12:05:00Z",
    "updated_at": "2025-08-29T12:05:00Z",
    "views_count": 0
}
Test Script:

javascript
pm.test("Post created successfully", function () {
    pm.response.to.have.status(201);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('id');
    pm.expect(responseJson.slug).to.eql('my-first-tech-post');
    
    // Сохраняем данные поста
    pm.collectionVariables.set("post_id", responseJson.id);
    pm.collectionVariables.set("post_slug", responseJson.slug);
});
10. Получение списка постов
Метод: GET
URL: {{baseUrl}}/api/v1/posts/
Headers:

Content-Type: application/json
Query Parameters (опционально):

page: 1
search: technology
category: {{category_id}}
ordering: -created_at
Test Script:

javascript
pm.test("Posts list retrieved", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('results');
    pm.expect(responseJson.results).to.be.an('array');
    pm.expect(responseJson).to.have.property('count');
});
11. Получение конкретного поста
Метод: GET
URL: {{baseUrl}}/api/v1/posts/{{post_slug}}/
Headers:

Content-Type: application/json
Test Script:

javascript
pm.test("Post detail retrieved", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('id');
    pm.expect(responseJson).to.have.property('title');
    pm.expect(responseJson).to.have.property('author_info');
    pm.expect(responseJson).to.have.property('category_info');
    pm.expect(responseJson.views_count).to.be.a('number');
});
12. Обновление поста
Метод: PATCH
URL: {{baseUrl}}/api/v1/posts/{{post_slug}}/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "title": "Updated Tech Post Title",
    "content": "This is the updated content of my technology post. Now with more detailed information about current trends."
}
Test Script:

javascript
pm.test("Post updated successfully", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson.title).to.eql('Updated Tech Post Title');
    
    // Обновляем slug если изменился
    if (responseJson.slug) {
        pm.collectionVariables.set("post_slug", responseJson.slug);
    }
});
13. Получение постов пользователя
Метод: GET
URL: {{baseUrl}}/api/v1/posts/my-posts/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Test Script:

javascript
pm.test("My posts retrieved", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson.results).to.be.an('array');
    // Проверяем, что все посты принадлежат текущему пользователю
    responseJson.results.forEach(function(post) {
        pm.expect(post.author).to.eql(parseInt(pm.collectionVariables.get("test_user_id")));
    });
});
14. Получение постов по категории
Метод: GET
URL: {{baseUrl}}/api/v1/posts/categories/{{category_slug}}/posts/
Headers:

Content-Type: application/json
Test Script:

javascript
pm.test("Posts by category retrieved", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('category');
    pm.expect(responseJson).to.have.property('posts');
    pm.expect(responseJson.posts).to.be.an('array');
    pm.expect(responseJson).to.have.property('pinned_posts_count');
});
15. Получение популярных постов
Метод: GET
URL: {{baseUrl}}/api/v1/posts/popular/
Headers:

Content-Type: application/json
Test Script:

javascript
pm.test("Popular posts retrieved", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.be.an('array');
    pm.expect(responseJson.length).to.be.at.most(10);
});
16. Получение недавних постов
Метод: GET
URL: {{baseUrl}}/api/v1/posts/recent/
Headers:

Content-Type: application/json
Test Script:

javascript
pm.test("Recent posts retrieved", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.be.an('array');
    pm.expect(responseJson.length).to.be.at.most(10);
});
17. Создание дополнительных постов для тестирования
Метод: POST
URL: {{baseUrl}}/api/v1/posts/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON) - Пост 2:

json
{
    "title": "AI and Machine Learning Trends",
    "content": "Artificial Intelligence is rapidly evolving. This post covers the latest trends in machine learning, deep learning, and their applications in various industries.",
    "category": {{category_id}},
    "status": "published"
}
Body (JSON) - Пост 3:

json
{
    "title": "Draft Post About Programming",
    "content": "This is a draft post about programming best practices that I'm still working on.",
    "category": {{category_id}},
    "status": "draft"
}
18. Создание второй категории
Метод: POST
URL: {{baseUrl}}/api/v1/posts/categories/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "name": "Science",
    "description": "Scientific discoveries and research"
}
19. Тестирование поиска постов
Метод: GET
URL: {{baseUrl}}/api/v1/posts/?search=technology
Headers:

Content-Type: application/json
Test Script:

javascript
pm.test("Search works correctly", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson.results).to.be.an('array');
    
    // Проверяем, что результаты содержат поисковый термин
    responseJson.results.forEach(function(post) {
        const searchTerm = post.title.toLowerCase().includes('tech') || 
                          post.content.toLowerCase().includes('tech');
        pm.expect(searchTerm).to.be.true;
    });
});
20. Тестирование фильтрации по категории
Метод: GET
URL: {{baseUrl}}/api/v1/posts/?category={{category_id}}
Headers:

Content-Type: application/json
21. Тестирование сортировки
Метод: GET
URL: {{baseUrl}}/api/v1/posts/?ordering=-views_count
Headers:

Content-Type: application/json
22. Удаление поста
Метод: DELETE
URL: {{baseUrl}}/api/v1/posts/{{post_slug}}/
Headers:

Authorization: Bearer {{access_token}}
Test Script:

javascript
pm.test("Post deleted successfully", function () {
    pm.response.to.have.status(204);
});
23. Обновление категории
Метод: PATCH
URL: {{baseUrl}}/api/v1/posts/categories/{{category_slug}}/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "name": "Advanced Technology",
    "description": "Updated description for advanced technology topics"
}
24. Удаление категории
Метод: DELETE
URL: {{baseUrl}}/api/v1/posts/categories/{{category_slug}}/
Headers:

Authorization: Bearer {{access_token}}
25. Выход из системы
Метод: POST
URL: {{baseUrl}}/api/v1/auth/logout/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "refresh_token": "{{refresh_token}}"
}
ТЕСТИРОВАНИЕ ОШИБОК И ГРАНИЧНЫХ СЛУЧАЕВ
Тестирование прав доступа
26. Попытка создания поста без авторизации
Метод: POST
URL: {{baseUrl}}/api/v1/posts/
Headers:

Content-Type: application/json
Body (JSON):

json
{
    "title": "Unauthorized Post",
    "content": "This should fail"
}
Ожидаемый ответ (401 Unauthorized):

json
{
    "detail": "Authentication credentials were not provided."
}
27. Попытка редактирования чужого поста
Создайте второго пользователя и попробуйте отредактировать пост первого пользователя.

Тестирование валидации
28. Создание поста с пустым заголовком
Метод: POST
URL: {{baseUrl}}/api/v1/posts/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "title": "",
    "content": "Post without title"
}
29. Создание категории с дублирующимся именем
Метод: POST
URL: {{baseUrl}}/api/v1/posts/categories/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "name": "Technology"
}
Ожидаемый ответ (400 Bad Request):

json
{
    "name": ["Category with this Name already exists."]
}
Тестирование пагинации
30. Тестирование пагинации постов
Метод: GET
URL: {{baseUrl}}/api/v1/posts/?page=1&page_size=5
Headers:

Content-Type: application/json
Test Script:

javascript
pm.test("Pagination works correctly", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('count');
    pm.expect(responseJson).to.have.property('next');
    pm.expect(responseJson).to.have.property('previous');
    pm.expect(responseJson.results.length).to.be.at.most(5);
});
РАСШИРЕННОЕ ТЕСТИРОВАНИЕ
Создание тестовых данных
31. Создание множественных постов для тестирования
Создайте скрипт для массового создания постов:

Pre-request Script:

javascript
const posts = [
    { title: "JavaScript Frameworks in 2025", content: "Exploring the latest JavaScript frameworks..." },
    { title: "Python for Data Science", content: "How Python is revolutionizing data analysis..." },
    { title: "Cloud Computing Trends", content: "The future of cloud infrastructure..." },
    { title: "Cybersecurity Best Practices", content: "Protecting your applications from threats..." },
    { title: "Mobile App Development", content: "Native vs Cross-platform development..." }
];

pm.globals.set("test_posts", JSON.stringify(posts));
pm.globals.set("current_post_index", "0");
Тестирование производительности
32. Тест загрузки множественных постов
Метод: GET
URL: {{baseUrl}}/api/v1/posts/?page_size=50

Test Script:

javascript
pm.test("Response time is acceptable", function () {
    pm.expect(pm.response.responseTime).to.be.below(2000);
});

pm.test("Large dataset loads correctly", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson.results).to.be.an('array');
});
Тестирование загрузки файлов
33. Загрузка изображения для поста
Метод: PATCH
URL: {{baseUrl}}/api/v1/posts/{{post_slug}}/
Headers:

Authorization: Bearer {{access_token}}
Body: form-data

image: [выберите файл изображения]
title: "Post with Image"
Тестирование специальных эндпоинтов
34. Тестирование счетчика просмотров
Сделайте несколько GET запросов к одному посту и проверьте увеличение счетчика:

Метод: GET
URL: {{baseUrl}}/api/v1/posts/{{post_slug}}/

Test Script:

javascript
pm.test("Views counter increments", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    
    // Сохраняем текущее количество просмотров
    const currentViews = responseJson.views_count;
    pm.globals.set("previous_views", currentViews);
    
    // При повторном вызове проверим увеличение
});
АВТОМАТИЗАЦИЯ ТЕСТИРОВАНИЯ
Collection-level Pre-request Script
javascript
// Проверяем наличие токена
const token = pm.collectionVariables.get("access_token");
if (!token && pm.info.requestName !== "Register" && pm.info.requestName !== "Login") {
    console.log("Warning: No access token found for authenticated request");
}

// Логирование для отладки
console.log(`Making request to: ${pm.request.url}`);
console.log(`Method: ${pm.request.method}`);
Collection-level Test Script
javascript
// Общие тесты для всех запросов
pm.test("Response has valid JSON structure", function () {
    pm.response.to.be.json;
});

pm.test("No server errors", function () {
    pm.response.to.not.have.status(500);
});

// Логирование ошибок
if (pm.response.code >= 400) {
    console.log("Error response:", pm.response.json());
}
ПОСЛЕДОВАТЕЛЬНОСТЬ ПОЛНОГО ТЕСТИРОВАНИЯ
Настройка пользователя:
Регистрация → сохранить токены
Просмотр профиля → проверить данные
Создание контента:
Создание категории → сохранить ID и slug
Создание нескольких постов
Создание черновика
Чтение контента:
Получение всех постов
Получение постов по категории
Популярные посты
Недавние посты
Мои посты
Обновление контента:
Редактирование поста
Обновление категории
Тестирование функций:
Поиск по постам
Фильтрация
Сортировка
Пагинация
Тестирование ошибок:
Неавторизованный доступ
Редактирование чужого контента
Невалидные данные
Очистка:
Удаление постов
Удаление категорий
Выход из системы
ДОПОЛНИТЕЛЬНЫЕ СОВЕТЫ
Переменные среды
Создайте разные среды:

Development: http://localhost:8000
Testing: http://localhost:8001
Production: https://yourdomain.com
Тестирование загрузки файлов
Для загрузки аватара или изображений постов:

Используйте Content-Type: multipart/form-data
Добавьте файл в соответствующее поле
Массовое тестирование
Используйте Newman (CLI для Postman) для автоматического запуска тестов:

bash
newman run collection.json -e environment.json
Мониторинг API
Настройте мониторы в Postman Cloud для автоматической проверки доступности API.

ИСПРАВЛЕНИЯ ОШИБОК В КОДЕ
При тестировании могут обнаружиться следующие ошибки:

В apps/accounts/serializer.py:
Строка 23: return должно быть raise
Строка 73: get_post_count должно быть get_posts_count
Строка 76: pcomments должно быть comments
Строка 103: attrs('new_passeord') должно быть attrs['new_password']
В apps/accounts/views.py:
Строка 24: Убрать (queryset) из UserRegistrationSerializer
Строка 92: seriaizer должно быть serializer
Строка 105: requset должно быть request
В apps/main/serializers.py:
Строка 14: get_posts_counts должно быть get_posts_count
Строка 77: validated_data['author'] = self.context['requrst'].user - requrst должно быть request
В apps/main/views.py:
Отсутствует метод get_posts_for_feed() в модели Post
Отсутствуют view функции pinned_posts_only и featured_posts упомянутые в urls.py
В conf/urls.py:
Строка 8: Добавьте / в конец пути: path('api/v1/auth/', include('apps.accounts.urls'))
АВТОМАТИЗИРОВАННЫЕ ТЕСТЫ
Runner Script для всей коллекции
javascript
// Этот скрипт запустит все тесты по порядку
const tests = [
    'Register',
    'Login', 
    'Create Category',
    'Create Post',
    'Get Posts List',
    'Get Post Detail',
    'Update Post',
    'My Posts',
    'Popular Posts',
    'Logout'
];

// Установите порядок выполнения в Collection Runner
Это полное руководство покрывает все аспекты тестирования вашего Django API через Postman, включая как базовую аутентификацию, так и полный функционал блога с постами и категориями.

