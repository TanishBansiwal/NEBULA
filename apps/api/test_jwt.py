from app.auth.jwt import create_access_token

token = create_access_token(
    {"sub": "tanish@example.com"}
)

print(token)