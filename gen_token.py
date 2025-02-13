import secrets

# Generate a 32-character URL-safe token
token = secrets.token_urlsafe(32)
print(token)
