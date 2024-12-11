import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


def encrypt_message(message, public_key):
    '''
    This function encrypts a message using the public key provided.
    The message is first encoded to bytes, then encrypted using the public key.

    ***Parameters***
    message: str
        The message to be encrypted.
    public_key: RSAPublicKey
        The public key to be used for encryption.

    ***Returns***
    str
        The encrypted message in base64 format.
    '''
    encrypted_message = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted_message).decode('utf-8')


def decrypt_message(encrypted_message, private_key):
    '''
    This function decrypts a message using the private key provided.
    The encrypted message is first decoded from base64, then decrypted using the private key.

    ***Parameters***
    encrypted_message: str
        The encrypted message in base64 format.
    private_key: RSAPrivateKey

    ***Returns***
    str
        The decrypted message.
    '''
    encrypted_message_bytes = base64.b64decode(encrypted_message.encode('utf-8'))
    decrypted_message = private_key.decrypt(
        encrypted_message_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_message.decode('utf-8')


def load_keys():
    '''
    This function loads the private and public keys from the files.

    ***Returns***
    RSAPrivateKey, RSAPublicKey
        The private and public keys loaded from the files.
    '''
    with open("final_version_codes/user_info_data/private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    with open("final_version_codes/user_info_data/public_key.pem", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    return private_key, public_key