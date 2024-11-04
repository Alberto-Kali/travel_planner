# app/services/auth_service.py
class AuthService:
    def __init__(self, db):
        self.db = db

    def register_user(self, user):
        # Здесь будет логика регистрации пользователя
        return {"message": "User registered successfully"}

    def authenticate_user(self, user):
        # Здесь будет логика аутентификации пользователя
        return {"message": "User authenticated successfully"}