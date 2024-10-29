import secrets
import hashlib

def generate_token(user):
    # Generar un token aleatorio
    token = secrets.token_urlsafe(16)

    # Hasher el token con el ID del usuario
    hashed_token = hashlib.sha256(f"{user.id}{token}".encode()).hexdigest()

    return hashed_token