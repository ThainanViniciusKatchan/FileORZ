from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
import os

def generate_keys(private_key_path="private_key.pem", public_key_path="public_key.pem"):
    
    # Gera um par de chaves RSA (Privada e Pública) para assinatura.
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Salva a chave privada
    with open(private_key_path, "wb") as f:
        try:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        except Exception as e:
            print(f"Erro ao salvar chave privada: {e}")

    # Salva a chave pública
    with open(public_key_path, "wb") as f:
        try:
            f.write(private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        except Exception as e:
            print(f"Erro ao salvar chave pública: {e}")

def sign_file(file_path, private_key_path="private_key.pem"):
    
    # Gera um arquivo de assinatura (.sig) para o arquivo especificado usando a chave privada.
    if not os.path.exists(private_key_path):
        raise FileNotFoundError(f"Chave privada não encontrada em: {private_key_path}")

    # Carrega a chave privada
    with open(private_key_path, "rb") as key_file:
        try:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )
        except Exception as e:
            print(f"Erro ao carregar chave privada: {e}")

    # Lê o arquivo alvo
    with open(file_path, "rb") as f:
        try:
            data = f.read()
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")

    # Cria a assinatura
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Salva o arquivo de assinatura
    signature_path = file_path + ".sig"
    with open(signature_path, "wb") as f:
        try:
            f.write(signature)
        except Exception as e:
            print(f"Erro ao salvar assinatura: {e}")
    
    return signature_path

def verify_file(file_path, signature_path, public_key_path="public_key.pem"):
    
    # Verifica se o arquivo corresponde à assinatura usando a chave pública.
    with open(public_key_path, "rb") as key_file:
        try:
            public_key = serialization.load_pem_public_key(key_file.read())
        except Exception as e:
            print(f"Erro ao carregar chave pública: {e}")

    with open(file_path, "rb") as f:
        try:
            data = f.read()
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")

    with open(signature_path, "rb") as f:
        try:
            signature = f.read()
        except Exception as e:
            print(f"Erro ao ler assinatura: {e}")

    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False
