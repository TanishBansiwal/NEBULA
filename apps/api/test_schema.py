from app.schemas.user import UserCreate

user = UserCreate(
    email="tanish@example.com",
    username="tanish",
    password="Nebula123!"
)

print(user)