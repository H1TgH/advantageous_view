# src/api/users/router.py
from fastapi import APIRouter, Depends, status, HTTPException
from api.users.schemas import (
    LoginResponseSchema,
    LoginSchema,
    RegistrationSchema,
    TokenSchema,
    UserResponseSchema  # если есть
)

# Создаём роутер
users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# === ВРЕМЕННЫЕ ЗАГЛУШКИ ДЛЯ ТЕСТА (без БД) ===
# Удалите этот код, когда подключите реальную базу данных

# Хранилище пользователей в памяти (только для разработки!)
_fake_users_db: dict[str, dict] = {}
_fake_token_counter = 1000


@users_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
    description="Создаёт нового пользователя (тестовая заглушка)"
)
async def register(user_data: RegistrationSchema):
    """
    Регистрация пользователя.
    
    В реальной версии:
    - Проверка уникальности email
    - Хэширование пароля
    - Сохранение в БД
    - Отправка письма подтверждения
    """
    
    # Проверка: не занят ли email
    if user_data.email in _fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже зарегистрирован"
        )
    
    # Сохраняем пользователя (в реальном приложении — в БД)
    _fake_users_db[user_data.email] = {
        "email": user_data.email,
        "name": user_data.name,
        "password": user_data.password,  # ⚠️ В продакшене — только хэш!
        "is_active": True,
        "created_at": "2024-01-01T00:00:00Z"
    }
    
    # Возвращаем успешный ответ
    return {
        "message": "Пользователь успешно зарегистрирован",
        "email": user_data.email,
        "name": user_data.name
    }


@users_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponseSchema,
    summary="Вход в систему",
    description="Возвращает access и refresh токены (тестовая заглушка)"
)
async def login(creds: LoginSchema):
    """
    Аутентификация пользователя.
    
    В реальной версии:
    - Проверка email и пароля (с хэшем)
    - Генерация JWT токенов
    - Логирование входа
    """
    
    # Проверка: существует ли пользователь
    user = _fake_users_db.get(creds.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Проверка пароля (в реальном приложении — сравнение хэшей)
    if user["password"] != creds.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Генерация фейковых токенов (в реальности — JWT с подписью)
    global _fake_token_counter
    _fake_token_counter += 1
    
    access_token = f"fake_access_{creds.email}_{_fake_token_counter}"
    refresh_token = f"fake_refresh_{creds.email}_{_fake_token_counter + 1000}"
    
    return LoginResponseSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@users_router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    response_model=TokenSchema,
    summary="Обновление access токена",
    description="Возвращает новый access токен по refresh токену (тестовая заглушка)"
)
async def refresh(token: TokenSchema):
    """
    Обновление токена доступа.
    
    В реальной версии:
    - Валидация refresh токена (подпись, срок)
    - Проверка в blacklisted токенах
    - Генерация нового access токена
    """
    
    # Простая валидация фейкового токена
    if not token.token.startswith("fake_refresh_"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный refresh токен"
        )
    
    # Генерация нового фейкового access токена
    global _fake_token_counter
    _fake_token_counter += 1
    new_access_token = f"fake_access_refreshed_{_fake_token_counter}"
    
    return TokenSchema(token=new_access_token)


@users_router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Получить данные текущего пользователя",
    description="Возвращает профиль авторизованного пользователя (тестовая заглушка)"
)
async def get_current_user(
    # В реальности здесь будет: current_user: User = Depends(get_current_user)
    token: str = None  # заглушка
):
    """
    Получение профиля пользователя.
    
    В реальной версии требует валидный access токен в заголовке:
    Authorization: Bearer <token>
    """
    
    # Для теста возвращаем данные первого пользователя
    if _fake_users_db:
        first_user = next(iter(_fake_users_db.values()))
        return {
            "email": first_user["email"],
            "name": first_user["name"],
            "is_active": first_user["is_active"]
        }
    
    # Если пользователей нет — возвращаем тестовые данные
    return {
        "email": "test@example.com",
        "name": "Тестовый пользователь",
        "is_active": True
    }