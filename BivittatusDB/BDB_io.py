import metaclass
import ctypes
import os
import getpass
from json import dumps, loads
from gzip import compress, decompress
from binascii import hexlify, unhexlify
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Import encryption-related functionalities
try:
    from encrypt import RSAFileEncryptor
except ImportError:
    raise metaclass.BDBException.ImportError(f"Could not import needed files in {__file__}")

# Load the shared library
try:
    io_lib = ctypes.CDLL(f"{os.path.dirname(os.path.abspath(__file__))}/lib_bdb.so")
except:
    raise metaclass.BDBException.ImportError(f"Could not find library lib_bdb.so")

# _CHANDLE class definition
class _CHANDLE:
    def __init__(self):
        pass

    def _call_lib_function(self, func_name, *args, restype=None):
        func = getattr(io_lib, func_name)
        argtypes = []
        for arg in args:
            if isinstance(arg, bytes):
                argtypes.append(ctypes.c_char_p)
            elif isinstance(arg, int):
                argtypes.append(ctypes.c_int)
            else:
                raise TypeError(f"Unsupported argument type: {type(arg)}")
        func.argtypes = argtypes
        if restype:
            func.restype = restype
        return func(*args)

    def CreateDatabase(self, databasename: bytes):
        self._call_lib_function('CreateDatabase', databasename)

    def CreateTable(self, databasename: bytes, tablename: bytes, data: bytes):
        self._call_lib_function('CreateTable', databasename, tablename, data)

    def AddMetaData(self, databasename: bytes, tablename: bytes, metadata: bytes):
        self._call_lib_function('AddMetaData', databasename, tablename, metadata)

    def ReadTable(self, database: bytes, tablename: bytes, metadata: int):
        result = self._call_lib_function('ReadTable', database, tablename, metadata, restype=ctypes.c_char_p)
        return result

    def DeleteTable(self, database: bytes, tablename: bytes):
        self._call_lib_function('DeleteTable', database, tablename)

    def UpdateTable(self, database: bytes, tablename: bytes, data: bytes):
        self._call_lib_function('UpdateTable', database, tablename, data)

    def UpdateMetaTable(self, database: bytes, tablename: bytes, metadata: bytes):
        self._call_lib_function('UpdateMetaTable', database, tablename, metadata)

    def CheckDataSet(self, database: bytes, tablename: bytes) -> bool:
        result = self._call_lib_function('CheckDataSet', f"./{database.decode()}/{tablename.decode()}".encode(), restype=ctypes.c_int)
        return bool(result)

# Key management and encryption handling
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

    def keygen(self):
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

# Main Handler class
class Handler:
    def __init__(self, database_name: str, encrypted: bool = False) -> None:
        self.CHANDLE = _CHANDLE()
        self.encryptor = RSAFileEncryptor(database_name)
        self.key_manager = KeyManager(database_name)
        self.database = database_name
        self.encrypted = encrypted
        self.ext = ".pydb"

    def init(self):
        """Initialize the database, generate keys, and secure the private key if encryption is enabled."""
        self.CHANDLE.CreateDatabase(self.database.encode())
        print("info: Generating keys...")
        self.key_manager.keygen()
        if self.encrypted:
            self.secure()
        return self

    def use(self):
        """Prepare the database for use by removing security if encryption is enabled."""
        if self.encrypted:
            self.remove_secure()
        return self

    def secure(self):
        """Secure the private key with a password."""
        password = getpass.getpass(f"Enter password for {self.database}: ")
        self.key_manager.secure(password)

    def remove_secure(self):
        """Remove security from the private key with a password."""
        password = getpass.getpass(f"Enter password for {self.database}: ")
        self.key_manager.remove_secure(password)

    def CreateTable(self, tablename: str, data: list, metadata: list):
        """Create a table with the given name, data, and metadata."""
        try:
            data = hexlify(compress(dumps(data).encode()))
            metadata = hexlify(compress(dumps(metadata).encode()))
            table_name = (tablename + self.ext).encode()
            self.CHANDLE.CreateTable(self.database.encode(), table_name, data)
            self.CHANDLE.AddMetaData(self.database.encode(), table_name, metadata)
            self.encryptor.encrypt_file(f"./{self.database}/{tablename}.pydb")
        except Exception as e:
            raise metaclass.BDBException.CreationError(f"Problem creating table {tablename}: {e}")

    def DeleteTable(self, tablename: str):
        """Delete the table with the given name."""
        try:
            self.CHANDLE.DeleteTable(self.database.encode(), (tablename + self.ext).encode())
        except Exception as e:
            raise metaclass.BDBException.DeletionError(f"Problem deleting table {tablename}: {e}")

    def UpdateTable(self, tablename: str, data: list):
        """Update the table with the given name with new data."""
        try:
            self.encryptor.decrypt_file(f"./{self.database}/{tablename}.pydb")
            data = hexlify(compress(dumps(data).encode()))
            self.CHANDLE.UpdateTable(self.database.encode(), (tablename + self.ext).encode(), data)
            self.encryptor.encrypt_file(f"./{self.database}/{tablename}.pydb")
        except Exception as e:
            raise metaclass.BDBException.EditError(f"Error updating table {tablename}: {e}")

    def UpdateMetaTable(self, tablename: str, metadata: list):
        """Update the metadata of the table with the given name."""
        try:
            self.encryptor.decrypt_file(f"./{self.database}/{tablename}.pydb")
            metadata = hexlify(compress(dumps(metadata).encode()))
            self.CHANDLE.UpdateMetaTable(self.database.encode(), (tablename + self.ext).encode(), metadata)
            self.encryptor.encrypt_file(f"./{self.database}/{tablename}.pydb")
        except Exception as e:
            raise metaclass.BDBException.EditError(f"Error updating metadata for table {tablename}: {e}")

    def ReadTable(self, tablename: str):
        """Read the data from the table with the given name."""
        try:
            self.encryptor.decrypt_file(f"./{self.database}/{tablename}.pydb")
            data = self.CHANDLE.ReadTable(self.database.encode(), (tablename + self.ext).encode(), int(False))
            data = loads(decompress(unhexlify(data)).decode())
            self.encryptor.encrypt_file(f"./{self.database}/{tablename}.pydb")
            return data
        except Exception as e:
            raise metaclass.BDBException.ReadError(f"Error reading data from table {tablename}: {e}")

    def ReadMetadata(self, tablename: str):
        """Read the metadata from the table with the given name."""
        try:
            self.encryptor.decrypt_file(f"./{self.database}/{tablename}.pydb")
            metadata = self.CHANDLE.ReadTable(self.database.encode(), (tablename + self.ext).encode(), int(True))
            metadata = loads(decompress(unhexlify(metadata)).decode())
            self.encryptor.encrypt_file(f"./{self.database}/{tablename}.pydb")
            return metadata
        except Exception as e:
            raise metaclass.BDBException.ReadError(f"Error reading metadata from table {tablename}: {e}")

    def TableExists(self, tablename: str) -> bool:
        """Check if the table with the given name exists in the database."""
        return self.CHANDLE.CheckDataSet(self.database.encode(), (tablename + self.ext).encode())

# Example usage
if __name__ == "__main__":
    handler = Handler("Hello", True).init().use()
    handler.CreateTable("Test", ["Hello World"], [None])
    print(f"Test table1 exists: {handler.TableExists('Test')}")

    handler.CreateTable("hello_world", ["check"], ["working..."])
    print(f"Test table2 exists: {handler.TableExists('hello_world')}")
    data = handler.ReadTable("hello_world")
    metadata = handler.ReadMetadata("hello_world")
    print(f"{data[0]}: {metadata[0]}")

    handler.DeleteTable("Test")
    print(f"Test table1 deleted: {not handler.TableExists('Test')}")

    handler.UpdateTable("hello_world", ["new check"])
    data = handler.ReadTable("hello_world")
    metadata = handler.ReadMetadata("hello_world")
    print(f"{data[0]}: {metadata[0]}")