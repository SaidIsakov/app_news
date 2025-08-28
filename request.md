Руководство по тестированию Django API в Postman
Предварительная настройка
1. Создание коллекции в Postman
Откройте Postman
Создайте новую коллекцию: Django Auth API
В настройках коллекции создайте переменные:
baseUrl: http://localhost:8000 (или ваш домен)
access_token: (будет заполняться автоматически)
refresh_token: (будет заполняться автоматически)
2. Запуск Django сервера
bash
python manage.py runserver
Тестирование эндпоинтов
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
    "message": "User registered successfuly"
}
Тест Script (Tests tab):

javascript
pm.test("Registration successful", function () {
    pm.response.to.have.status(201);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('access');
    pm.expect(responseJson).to.have.property('refresh');
    
    // Сохраняем токены
    pm.collectionVariables.set("access_token", responseJson.access);
    pm.collectionVariables.set("refresh_token", responseJson.refresh);
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
Ожидаемый ответ (200 OK):

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
    "message": "User login successfuly"
}
Тест Script:

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
Ожидаемый ответ (200 OK):

json
{
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
}
Тест Script:

javascript
pm.test("Profile retrieved successfully", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('id');
    pm.expect(responseJson).to.have.property('email');
});
4. Обновление профиля
Метод: PATCH или PUT
URL: {{baseUrl}}/api/v1/auth/profile/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON) для PATCH:

json
{
    "first_name": "UpdatedTest",
    "bio": "This is my updated bio"
}
Ожидаемый ответ (200 OK):

json
{
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "UpdatedTest",
    "last_name": "User",
    "full_name": "UpdatedTest User",
    "avatar": null,
    "bio": "This is my updated bio",
    "created_at": "2025-08-27T12:00:00Z",
    "updated_at": "2025-08-27T12:05:00Z",
    "posts_count": 0,
    "comments_count": 0
}
5. Смена пароля
Метод: PUT или PATCH
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
Ожидаемый ответ (200 OK):

json
{
    "message": "Password changed successfully"
}
6. Обновление токена
Метод: POST
URL: {{baseUrl}}/api/v1/auth/token/refresh/
Headers:

Content-Type: application/json
Body (JSON):

json
{
    "refresh": "{{refresh_token}}"
}
Ожидаемый ответ (200 OK):

json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
Тест Script:

javascript
pm.test("Token refreshed successfully", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('access');
    
    // Обновляем access токен
    pm.collectionVariables.set("access_token", responseJson.access);
});
7. Выход из системы
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
Ожидаемый ответ (200 OK):

json
{
    "message": "Logout successful"
}
Тестирование ошибок
1. Регистрация с некорректными данными
Тест 1: Пароли не совпадают

json
{
    "email": "test2@example.com",
    "username": "testuser2",
    "first_name": "Test",
    "last_name": "User",
    "password": "TestPassword123!",
    "password_confirm": "DifferentPassword123!"
}
Тест 2: Слабый пароль

json
{
    "email": "test3@example.com",
    "username": "testuser3",
    "first_name": "Test",
    "last_name": "User",
    "password": "123",
    "password_confirm": "123"
}
Тест 3: Дублирующийся email

json
{
    "email": "test@example.com",
    "username": "testuser4",
    "first_name": "Test",
    "last_name": "User",
    "password": "TestPassword123!",
    "password_confirm": "TestPassword123!"
}
2. Вход с неверными данными
Тест: Неверный пароль

json
{
    "email": "test@example.com",
    "password": "WrongPassword123!"
}
Ожидаемый ответ (400 Bad Request):

json
{
    "non_field_errors": ["User not found."]
}
3. Доступ без токена
Попробуйте обратиться к /api/v1/auth/profile/ без заголовка Authorization.

Ожидаемый ответ (401 Unauthorized):

json
{
    "detail": "Authentication credentials were not provided."
}
Последовательность тестирования
Регистрация → сохранить токены
Просмотр профиля → проверить данные пользователя
Обновление профиля → изменить некоторые поля
Смена пароля → изменить пароль
Выход → завершить сессию
Вход с новым паролем → проверить, что пароль изменился
Обновление токена → проверить обновление access токена
Финальный выход
Дополнительные советы
Автоматизация токенов
Создайте Pre-request Script на уровне коллекции:

javascript
// Проверяем, есть ли токен и не истек ли он
const token = pm.collectionVariables.get("access_token");
if (!token) {
    console.log("No access token found");
}
Переменные среды
Создайте разные среды для разработки и тестирования:

Development: http://localhost:8000
Testing: http://localhost:8001
Production: https://yourdomain.com
Тестирование файлов
Для тестирования загрузки аватара используйте form-data:

Content-Type: multipart/form-data
И добавьте файл в поле avatar.

Исправление найденных ошибок в коде
В процессе тестирования вы можете обнаружить следующие ошибки в коде:

В serializer.py, строка 23: return должен быть raise
В serializer.py, строка 73: get_post_count должен быть get_posts_count
В serializer.py, строка 76: pcomments должен быть comments
В serializer.py, строка 103: attrs('new_passeord') должно быть attrs['new_password']
В views.py, строка 24: Уберите (queryset) из UserRegistrationSerializer
В views.py, строка 92: seriaizer должно быть serializer
В views.py, строка 105: requset должно быть request
В urls.py, строка 8: Добавьте / в конец пути: path('api/v1/auth/', include('apps.accounts.urls'))
Эти исправления необходимы для корректной работы API.

