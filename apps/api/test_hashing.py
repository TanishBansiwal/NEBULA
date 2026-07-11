from app.auth.hashing import hash_password, verify_password

password = "Nebula123!"

hashed = hash_password(password)

print("Original :", password)
print("Hash     :", hashed)

print("Verified :", verify_password(password, hashed))