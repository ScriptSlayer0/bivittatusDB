from binascii import hexlify, unhexlify
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class RSAFileEncryptor:
    def __init__(self, database):
        self.key_size = 4096
        self.database = database
        self.private_key_file = f"./{self.database}/private.pem"
        self.public_key_file = f"./{self.database}/public.pem"

    def generate_keys(self):
        key = RSA.generate(self.key_size)
        private_key = key.export_key()
        public_key = key.publickey().export_key()

        os.makedirs(self.database, exist_ok=True)
        with open(self.private_key_file, "wb") as priv_file:
            priv_file.write(private_key)

        with open(self.public_key_file, "wb") as pub_file:
            pub_file.write(public_key)

    def encrypt_file(self, input_file):
        with open(self.public_key_file, "rb") as pub_file:
            public_key = RSA.import_key(pub_file.read())

        cipher_rsa = PKCS1_OAEP.new(public_key)

        # Generate symmetric key (AES)
        session_key = get_random_bytes(16)

        # Encrypt the session key with RSA
        encrypted_session_key = cipher_rsa.encrypt(session_key)

        # Encrypt file data with AES
        with open(input_file, "rb") as f:
            file_data = f.read()

        cipher_aes = AES.new(session_key, AES.MODE_CBC)
        encrypted_data = cipher_aes.encrypt(pad(file_data, AES.block_size))

        # Save the encrypted session key and file data
        with open(input_file, "wb") as f:
            f.write(cipher_aes.iv)
            f.write(encrypted_session_key)
            f.write(encrypted_data)

    def decrypt_file(self, input_file):
        with open(self.private_key_file, "rb") as priv_file:
            private_key = RSA.import_key(priv_file.read())

        cipher_rsa = PKCS1_OAEP.new(private_key)

        # Read the encrypted session key and file data
        with open(input_file, "rb") as f:
            iv = f.read(16)
            encrypted_session_key = f.read(512)
            encrypted_data = f.read()

        # Decrypt the session key with RSA
        session_key = cipher_rsa.decrypt(encrypted_session_key)

        # Decrypt file data with AES
        cipher_aes = AES.new(session_key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher_aes.decrypt(encrypted_data), AES.block_size)

        with open(input_file, "wb") as f:
            f.write(decrypted_data)


class KeyManager:
    def __init__(self, database_name):
        self.database = database_name
        self.private_key_path = os.path.join(f"./{self.database}", "private.pem")
        self.public_key_path = os.path.join(f"./{self.database}", "public.pem")
        self.private_key = None
        self.public_key = None

        # Load keys if they already exist
        if os.path.exists(self.private_key_path) and os.path.exists(self.public_key_path):
            self.keyload()

    def key_checker(self):
        """Generate RSA keys and store them in the database directory if they do not exist."""
        if os.path.exists(self.private_key_path) and os.path.exists(self.public_key_path):
            print("Keys already exist. Skipping key generation.")
            return

        key = RSA.generate(4096)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        os.makedirs(os.path.dirname(self.private_key_path), exist_ok=True)
        
        with open(self.public_key_path, "wb") as f:
            f.write(public_key)
        with open(self.private_key_path, "wb") as f:
            f.write(private_key)
        print("Keys generated and saved.")

    def keyload(self):
        """Load RSA keys from the database directory."""
        if not os.path.exists(self.private_key_path) or not os.path.exists(self.public_key_path):
            raise FileNotFoundError("Key files do not exist. Please generate keys first.")
        
        with open(self.private_key_path, "rb") as f:
            self.private_key = RSA.import_key(f.read())
        with open(self.public_key_path, "rb") as f:
            self.public_key = RSA.import_key(f.read())

    @staticmethod
    def pad(s, block_size):
        """Pad the input bytes to be a multiple of block_size."""
        padding_len = block_size - len(s) % block_size
        return s + bytes([padding_len]) * padding_len

    @staticmethod
    def unpad(s):
        """Remove padding from the input bytes."""
        padding_len = s[-1]
        return s[:-padding_len]

    def secure(self, password):
        """Encrypt the private key with a password."""
        if not self.private_key:
            raise RuntimeError("Private key not loaded. Cannot encrypt.")

        try:
            with open(self.private_key_path, "rb") as f:
                key = f.read()
            key = self.pad(key, 256)
            password = self.pad(password.encode(), 32)
            iv = get_random_bytes(16)
            cipher = AES.new(password, AES.MODE_CBC, iv)
            ciphertext = hexlify(iv + cipher.encrypt(key))
            with open(self.private_key_path, "wb") as f:
                f.write(ciphertext)
            print("Private key encrypted.")
        except Exception as e:
            raise RuntimeError(f"Problem encrypting data: {e}")

    def remove_secure(self, password):
        """Decrypt the private key with a password."""
        if not os.path.exists(self.private_key_path):
            raise FileNotFoundError("Encrypted private key file does not exist.")
        
        try:
            with open(self.private_key_path, "rb") as f:
                key = unhexlify(f.read())
            password = self.pad(password.encode(), 32)
            iv = key[:AES.block_size]
            cipher = AES.new(password, AES.MODE_CBC, iv)
            decrypted_key = self.unpad(cipher.decrypt(key[AES.block_size:]))
            with open(self.private_key_path, "wb") as f:
                f.write(decrypted_key)
            self.private_key = RSA.import_key(decrypted_key)
            print("Private key decrypted and loaded.")
        except Exception as e:
            raise RuntimeError(f"Problem decrypting data: {e}")

# Example usage:
if __name__ == "__main__":
    encryptor = RSAFileEncryptor("Hello")
    encryptor.generate_keys()

    # Encrypt the file
    encryptor.encrypt_file("Hello/plainfile.txt")

    # Decrypt the file
    encryptor.decrypt_file("Hello/encryptedfile.bin")
