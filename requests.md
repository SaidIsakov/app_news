ЧАСТЬ 3: ТЕСТИРОВАНИЕ КОММЕНТАРИЕВ (COMMENTS APP)
Предварительные исправления кода
Перед тестированием необходимо исправить следующие ошибки в коде:

В apps/comments/serializers.py:
Строка 2: from .models import Comments должно быть from .models import Comment
Строка 9: model = Comments должно быть model = Comment
Строка 32: model = Comments должно быть model = Comment
Строка 36: if not Post.objects.filter(id=value.id, status='pablished').exists(): должно быть status='published'
Строка 49: model = Comments должно быть model = Comment
Строка 51: field = ('content',) должно быть fields = ('content',)
Строка 56: replise = serializers.SerializerMethodField() должно быть replies = serializers.SerializerMethodField()
Строка 61: def get_replise(self, obj): должно быть def get_replies(self, obj):
Строка 63: replise = obj.replise.filter(is_active=True).order_by('created_at') должно быть replies = obj.replies.filter(is_active=True).order_by('created_at')
Строка 64: return CommentSerializer(replise, many=True, context=self.context).data должно быть return CommentSerializer(replies, many=True, context=self.context).data
В apps/comments/views.py:
Строка 76: if not Post.objects.filter(id=post_id, status='published').exists(): - убедитесь что это published, а не pablished
Тестирование Comments API
25. Создание комментария к посту
Метод: POST
URL: {{baseUrl}}/api/v1/comments/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "post": {{post_id}},
    "content": "This is my first comment on this amazing post! Thanks for sharing such valuable information."
}
Ожидаемый ответ (201 Created):

json
{
    "id": 1,
    "content": "This is my first comment on this amazing post! Thanks for sharing such valuable information.",
    "author": 1,
    "parent": null,
    "is_active": true,
    "replies_count": 0,
    "is_reply": false,
    "created_at": "2025-08-29T14:00:00Z",
    "updated_at": "2025-08-29T14:00:00Z"
}
Test Script:

javascript
pm.test("Comment created successfully", function () {
    pm.response.to.have.status(201);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('id');
    pm.expect(responseJson.content).to.include('first comment');
    pm.expect(responseJson.is_reply).to.be.false;
    pm.expect(responseJson.replies_count).to.eql(0);

    // Сохраняем ID комментария для дальнейших тестов
    pm.collectionVariables.set("comment_id", responseJson.id);
});
26. Создание ответа на комментарий
Метод: POST
URL: {{baseUrl}}/api/v1/comments/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "post": {{post_id}},
    "parent": {{comment_id}},
    "content": "Great comment! I totally agree with your point of view."
}
Test Script:

javascript
pm.test("Reply to comment created successfully", function () {
    pm.response.to.have.status(201);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('id');
    pm.expect(responseJson.parent).to.eql(parseInt(pm.collectionVariables.get("comment_id")));
    pm.expect(responseJson.is_reply).to.be.true;

    // Сохраняем ID ответа
    pm.collectionVariables.set("reply_id", responseJson.id);
});
27. Получение списка всех комментариев
Метод: GET
URL: {{baseUrl}}/api/v1/comments/
Headers:

Content-Type: application/json
Query Parameters (опционально):

page: 1
post: {{post_id}}
search: amazing
ordering: -created_at
Test Script:

javascript
pm.test("Comments list retrieved successfully", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('results');
    pm.expect(responseJson.results).to.be.an('array');
    pm.expect(responseJson).to.have.property('count');
    pm.expect(responseJson).to.have.property('next');
    pm.expect(responseJson).to.have.property('previous');
});
28. Получение деталей комментария с ответами
Метод: GET
URL: {{baseUrl}}/api/v1/comments/{{comment_id}}/
Headers:

Content-Type: application/json
Ожидаемый ответ (200 OK):

json
{
    "id": 1,
    "content": "This is my first comment...",
    "author": 1,
    "parent": null,
    "is_active": true,
    "replies_count": 1,
    "is_reply": false,
    "created_at": "2025-08-29T14:00:00Z",
    "updated_at": "2025-08-29T14:00:00Z",
    "replies": [
        {
            "id": 2,
            "content": "Great comment! I totally agree...",
            "author": 1,
            "parent": 1,
            "is_active": true,
            "replies_count": 0,
            "is_reply": true,
            "created_at": "2025-08-29T14:05:00Z",
            "updated_at": "2025-08-29T14:05:00Z"
        }
    ]
}
Test Script:

javascript
pm.test("Comment detail with replies retrieved", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('id');
    pm.expect(responseJson).to.have.property('replies');
    pm.expect(responseJson.replies).to.be.an('array');
    pm.expect(responseJson.replies_count).to.be.a('number');
});
29. Обновление комментария
Метод: PATCH
URL: {{baseUrl}}/api/v1/comments/{{comment_id}}/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "content": "This is my updated comment with additional thoughts and insights about the topic."
}
Test Script:

javascript
pm.test("Comment updated successfully", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson.content).to.include('updated comment');
    pm.expect(responseJson.updated_at).to.not.eql(responseJson.created_at);
});
30. Получение комментариев пользователя
Метод: GET
URL: {{baseUrl}}/api/v1/comments/my-comments/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Query Parameters (опционально):

page: 1
is_active: true
search: updated
ordering: -created_at
Test Script:

javascript
pm.test("My comments retrieved successfully", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson.results).to.be.an('array');

    // Проверяем, что все комментарии принадлежат текущему пользователю
    const userId = parseInt(pm.collectionVariables.get("test_user_id"));
    responseJson.results.forEach(function(comment) {
        pm.expect(comment.author).to.eql(userId);
    });
});
31. Получение комментариев к конкретному посту
Метод: GET
URL: {{baseUrl}}/api/v1/comments/post/{{post_id}}/
Headers:

Content-Type: application/json
Ожидаемый ответ (200 OK):

json
{
    "post": {
        "id": 1,
        "title": "My First Tech Post",
        "slug": "my-first-tech-post"
    },
    "comments": [
        {
            "id": 1,
            "content": "This is my updated comment...",
            "author": 1,
            "parent": null,
            "is_active": true,
            "replies_count": 1,
            "is_reply": false,
            "created_at": "2025-08-29T14:00:00Z",
            "updated_at": "2025-08-29T14:10:00Z",
            "replies": [...]
        }
    ],
    "comments_count": 2
}
Test Script:

javascript
pm.test("Post comments retrieved successfully", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('post');
    pm.expect(responseJson).to.have.property('comments');
    pm.expect(responseJson).to.have.property('comments_count');
    pm.expect(responseJson.comments).to.be.an('array');

    // Проверяем структуру поста
    pm.expect(responseJson.post).to.have.property('id');
    pm.expect(responseJson.post).to.have.property('title');
    pm.expect(responseJson.post).to.have.property('slug');

    // Проверяем, что основные комментарии не имеют parent
    responseJson.comments.forEach(function(comment) {
        pm.expect(comment.parent).to.be.null;
        pm.expect(comment.is_reply).to.be.false;
    });
});
32. Получение ответов на комментарий
Метод: GET
URL: {{baseUrl}}/api/v1/comments/{{comment_id}}/replies/
Headers:

Content-Type: application/json
Test Script:

javascript
pm.test("Comment replies retrieved successfully", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('parent_comment');
    pm.expect(responseJson).to.have.property('replies');
    pm.expect(responseJson).to.have.property('replies_count');
    pm.expect(responseJson.replies).to.be.an('array');

    // Проверяем, что все ответы ссылаются на родительский комментарий
    const parentId = parseInt(pm.collectionVariables.get("comment_id"));
    responseJson.replies.forEach(function(reply) {
        pm.expect(reply.parent).to.eql(parentId);
        pm.expect(reply.is_reply).to.be.true;
    });
});
33. Создание вложенного ответа (ответ на ответ)
Метод: POST
URL: {{baseUrl}}/api/v1/comments/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "post": {{post_id}},
    "parent": {{reply_id}},
    "content": "This is a nested reply to the previous response."
}
Test Script:

javascript
pm.test("Nested reply created successfully", function () {
    pm.response.to.have.status(201);
    const responseJson = pm.response.json();
    pm.expect(responseJson.parent).to.eql(parseInt(pm.collectionVariables.get("reply_id")));
    pm.expect(responseJson.is_reply).to.be.true;

    pm.collectionVariables.set("nested_reply_id", responseJson.id);
});
34. Мягкое удаление комментария
Метод: DELETE
URL: {{baseUrl}}/api/v1/comments/{{nested_reply_id}}/
Headers:

Authorization: Bearer {{access_token}}
Test Script:

javascript
pm.test("Comment soft deleted successfully", function () {
    pm.response.to.have.status(204);
});

// Проверяем, что комментарий не отображается в списке активных
pm.test("Deleted comment not in active list", function () {
    pm.sendRequest({
        url: pm.collectionVariables.get("baseUrl") + "/api/v1/comments/",
        method: 'GET',
        header: {
            'Content-Type': 'application/json'
        }
    }, function (err, response) {
        const deletedId = parseInt(pm.collectionVariables.get("nested_reply_id"));
        const comments = response.json().results;
        const deletedComment = comments.find(c => c.id === deletedId);
        pm.expect(deletedComment).to.be.undefined;
    });
});
Тестирование фильтрации и поиска комментариев
35. Фильтрация комментариев по посту
Метод: GET
URL: {{baseUrl}}/api/v1/comments/?post={{post_id}}
Headers:

Content-Type: application/json
Test Script:

javascript
pm.test("Comments filtered by post correctly", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    const postId = parseInt(pm.collectionVariables.get("post_id"));

    responseJson.results.forEach(function(comment) {
        pm.expect(comment.post).to.eql(postId);
    });
});
36. Фильтрация комментариев по автору
Метод: GET
URL: {{baseUrl}}/api/v1/comments/?author={{test_user_id}}
Headers:

Content-Type: application/json
Test Script:

javascript
pm.test("Comments filtered by author correctly", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    const authorId = parseInt(pm.collectionVariables.get("test_user_id"));

    responseJson.results.forEach(function(comment) {
        pm.expect(comment.author).to.eql(authorId);
    });
});
37. Поиск комментариев по содержимому
Метод: GET
URL: {{baseUrl}}/api/v1/comments/?search=amazing
Headers:

Content-Type: application/json
Test Script:

javascript
pm.test("Comment search works correctly", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson.results).to.be.an('array');

    // Проверяем, что найденные комментарии содержат поисковый термин
    responseJson.results.forEach(function(comment) {
        pm.expect(comment.content.toLowerCase()).to.include('amazing');
    });
});
38. Фильтрация только основных комментариев
Метод: GET
URL: {{baseUrl}}/api/v1/comments/?parent__isnull=true
Headers:

Content-Type: application/json
Test Script:

javascript
pm.test("Main comments only filter works", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();

    responseJson.results.forEach(function(comment) {
        pm.expect(comment.parent).to.be.null;
        pm.expect(comment.is_reply).to.be.false;
    });
});
39. Сортировка комментариев
Метод: GET
URL: {{baseUrl}}/api/v1/comments/?ordering=created_at
Headers:

Content-Type: application/json
Test Script:

javascript
pm.test("Comments sorted correctly", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    const comments = responseJson.results;

    if (comments.length > 1) {
        for (let i = 1; i < comments.length; i++) {
            const prev = new Date(comments[i-1].created_at);
            const curr = new Date(comments[i].created_at);
            pm.expect(curr.getTime()).to.be.at.least(prev.getTime());
        }
    }
});
Тестирование прав доступа и безопасности
40. Попытка создания комментария без авторизации
Метод: POST
URL: {{baseUrl}}/api/v1/comments/
Headers:

Content-Type: application/json
Body (JSON):

json
{
    "post": {{post_id}},
    "content": "Unauthorized comment"
}
Ожидаемый ответ (401 Unauthorized):

json
{
    "detail": "Authentication credentials were not provided."
}
41. Попытка редактирования чужого комментария
Сначала создайте второго пользователя и его комментарий, затем попробуйте отредактировать комментарий первого пользователя.

Создание второго пользователя:

Метод: POST
URL: {{baseUrl}}/api/v1/auth/register/
Body (JSON):

json
{
    "email": "user2@example.com",
    "username": "testuser2",
    "first_name": "Second",
    "last_name": "User",
    "password": "TestPassword123!",
    "password_confirm": "TestPassword123!"
}
Test Script:

javascript
pm.test("Second user registered", function () {
    pm.response.to.have.status(201);
    const responseJson = pm.response.json();
    pm.collectionVariables.set("user2_access_token", responseJson.access);
});
Попытка редактирования чужого комментария:

Метод: PATCH
URL: {{baseUrl}}/api/v1/comments/{{comment_id}}/
Headers:

Authorization: Bearer {{user2_access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "content": "Trying to edit someone else's comment"
}
Ожидаемый ответ (403 Forbidden):

json
{
    "detail": "You do not have permission to perform this action."
}
42. Создание комментария к несуществующему посту
Метод: POST
URL: {{baseUrl}}/api/v1/comments/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "post": 99999,
    "content": "Comment to non-existent post"
}
Ожидаемый ответ (400 Bad Request):

json
{
    "post": ["Post not found"]
}
43. Создание ответа на комментарий из другого поста
Метод: POST
URL: {{baseUrl}}/api/v1/comments/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Создайте сначала второй пост и получите его ID, затем:

Body (JSON):

json
{
    "post": {{post2_id}},
    "parent": {{comment_id}},
    "content": "Invalid cross-post reply"
}
Ожидаемый ответ (400 Bad Request):

json
{
    "parent": ["Parent comment must belong to the same post"]
}
Тестирование специальных эндпоинтов
44. Комментарии к черновику поста
Создайте пост со статусом 'draft', затем попробуйте создать к нему комментарий:

Метод: POST
URL: {{baseUrl}}/api/v1/comments/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "post": {{draft_post_id}},
    "content": "Comment to draft post"
}
Ожидаемый ответ (400 Bad Request):

json
{
    "post": ["Post not found"]
}
45. Создание множественных комментариев для тестирования пагинации
Pre-request Script для массового создания:

javascript
const comments = [
    "Excellent article! Very informative.",
    "I disagree with some points made here.",
    "Could you provide more examples?",
    "This helped me understand the topic better.",
    "Looking forward to more posts like this.",
    "Great writing style and clear explanations.",
    "I have a question about the second paragraph.",
    "Thanks for sharing your expertise!",
    "This is exactly what I was looking for.",
    "Please write more about this topic."
];

pm.globals.set("test_comments", JSON.stringify(comments));
pm.globals.set("current_comment_index", "0");
46. Тестирование пагинации комментариев
Метод: GET
URL: {{baseUrl}}/api/v1/comments/?page=1&page_size=5
Headers:

Content-Type: application/json
Test Script:

javascript
pm.test("Comments pagination works correctly", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('count');
    pm.expect(responseJson).to.have.property('next');
    pm.expect(responseJson).to.have.property('previous');
    pm.expect(responseJson.results.length).to.be.at.most(5);

    // Если есть следующая страница, проверяем ссылку
    if (responseJson.next) {
        pm.expect(responseJson.next).to.include('page=2');
    }
});
Тестирование интеграции с другими приложениями
47. Проверка счетчика комментариев в посте
Метод: GET
URL: {{baseUrl}}/api/v1/posts/{{post_slug}}/
Headers:

Content-Type: application/json
Test Script:

javascript
pm.test("Post shows correct comments count", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    pm.expect(responseJson).to.have.property('comments_count');
    pm.expect(responseJson.comments_count).to.be.a('number');
    pm.expect(responseJson.comments_count).to.be.at.least(0);
});
48. Проверка обновления счетчика после создания комментария
Pre-request Script:

javascript
// Получаем текущее количество комментариев
pm.sendRequest({
    url: pm.collectionVariables.get("baseUrl") + "/api/v1/posts/" + pm.collectionVariables.get("post_slug") + "/",
    method: 'GET',
    header: {
        'Content-Type': 'application/json'
    }
}, function (err, response) {
    const currentCount = response.json().comments_count;
    pm.globals.set("comments_count_before", currentCount);
});
Создайте новый комментарий, затем проверьте обновление счетчика:

Test Script:

javascript
pm.test("Comments count updated after creation", function () {
    pm.response.to.have.status(201);

    // Проверяем обновленный счетчик
    pm.sendRequest({
        url: pm.collectionVariables.get("baseUrl") + "/api/v1/posts/" + pm.collectionVariables.get("post_slug") + "/",
        method: 'GET',
        header: {
            'Content-Type': 'application/json'
        }
    }, function (err, response) {
        const newCount = response.json().comments_count;
        const oldCount = parseInt(pm.globals.get("comments_count_before"));
        pm.expect(newCount).to.eql(oldCount + 1);
    });
});
Тестирование граничных случаев
49. Создание комментария с пустым содержимым
Метод: POST
URL: {{baseUrl}}/api/v1/comments/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "post": {{post_id}},
    "content": ""
}
Ожидаемый ответ (400 Bad Request):

json
{
    "content": ["This field may not be blank."]
}
50. Создание комментария с очень длинным содержимым
Метод: POST
URL: {{baseUrl}}/api/v1/comments/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Pre-request Script:

javascript
// Генерируем длинный текст
const longText = "A".repeat(5000);
pm.globals.set("long_comment_text", longText);
Body (JSON):

json
{
    "post": {{post_id}},
    "content": "{{long_comment_text}}"
}
51. Получение комментариев с различными параметрами сортировки
Метод: GET
URL: {{baseUrl}}/api/v1/comments/?ordering=updated_at
Headers:

Content-Type: application/json
52. Тестирование комбинированных фильтров
Метод: GET
URL: {{baseUrl}}/api/v1/comments/?post={{post_id}}&ordering=-created_at&search=comment
Headers:

Content-Type: application/json
Test Script:

javascript
pm.test("Combined filters work correctly", function () {
    pm.response.to.have.status(200);
    const responseJson = pm.response.json();
    const postId = parseInt(pm.collectionVariables.get("post_id"));

    responseJson.results.forEach(function(comment) {
        pm.expect(comment.post).to.eql(postId);
        pm.expect(comment.content.toLowerCase()).to.include('comment');
    });
});
Производительность и нагрузочное тестирование
53. Тест времени отклика для получения комментариев
Метод: GET
URL: {{baseUrl}}/api/v1/comments/post/{{post_id}}/
Headers:

Content-Type: application/json
Test Script:

javascript
pm.test("Comments loading performance", function () {
    pm.expect(pm.response.responseTime).to.be.below(1000);
});

pm.test("Response includes performance data", function () {
    const responseJson = pm.response.json();
    pm.expect(responseJson.comments_count).to.be.a('number');
    console.log(`Loaded ${responseJson.comments_count} comments in ${pm.response.responseTime}ms`);
});
54. Тестирование глубокой вложенности комментариев
Создайте цепочку вложенных ответов (комментарий → ответ → ответ на ответ):

Метод: POST
URL: {{baseUrl}}/api/v1/comments/
Headers:

Authorization: Bearer {{access_token}}
Content-Type: application/json
Body (JSON):

json
{
    "post": {{post_id}},
    "parent": {{comment_id}},
    "content": "Level 1 reply"
}
Затем создайте ответ на этот ответ и так далее.

Интеграционное тестирование
55. Полный жизненный цикл комментария
Pre-request Script для полного теста:

javascript
// Создаем новый пост специально для тестирования комментариев
pm.sendRequest({
    url: pm.collectionVariables.get("baseUrl") + "/api/v1/posts/",
    method: 'POST',
    header: {
        'Authorization': 'Bearer ' + pm.collectionVariables.get("access_token"),
        'Content-Type':
