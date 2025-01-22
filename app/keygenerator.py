import os

secret_key = os.urandom(32)
secret_key_hex = secret_key.hex()
print(secret_key_hex)

#  os.urandom(32) generates a 32-byte (256-bit) random value using the operating system's random number generator. 
# This value can be used as a secure secret key.