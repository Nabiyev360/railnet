import base64


my_key = "Railman_Jkey_2025"


def xor_encrypt(number: int, key=my_key) -> str:
    key_bytes = key.encode()
    num_bytes = str(number).encode()

    encrypted_bytes = bytes([num_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(num_bytes))])

    return base64.urlsafe_b64encode(encrypted_bytes).decode()  # Base64 orqali matn shakliga o'tkazamiz


def xor_decrypt(encrypted_text: str, key=my_key) -> int:
    key_bytes = key.encode()
    encrypted_bytes = base64.urlsafe_b64decode(encrypted_text.encode())  # Base64 dan qaytaramiz

    decrypted_bytes = bytes([encrypted_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(encrypted_bytes))])

    return int(decrypted_bytes.decode())  # Raqam sifatida qaytaramiz


original_number = 52404026880010

encrypted = xor_encrypt(original_number)
decrypted = xor_decrypt(encrypted)

# print(f"Shifrlangan: {encrypted}")
# print(f"Ochilgan: {decrypted}")
