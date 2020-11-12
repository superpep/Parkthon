from passlib.context import CryptContext

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

def encrypt_password(password):
    """
    Funció que retorna la contrasenya enviada en sha256

    Entrada:
        password (string): contrasenya

    Eixida:
        (string) contrasenya encriptada en sha256
    """
    return pwd_context.encrypt(password)


def check_encrypted_password(password, hashed):
    """
    Comprova si la contrasenya enviada és la mateixa que la encriptada

    Entrada:
        password (string): contrasenya sense encriptar
        hashed (string): contrasenya encriptada

    Eixida:
        (boolean) True si la contrasenya és correcta
                  False si no ho és
    """
    return pwd_context.verify(password, hashed)