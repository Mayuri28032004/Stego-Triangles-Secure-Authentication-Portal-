import wave
import numpy as np
import hashlib
from cryptography.fernet import Fernet, InvalidToken
import base64

# ---------------- ENCRYPTION ---------------- #

def generate_key(password):
    hash = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(hash))

def encrypt_data(data, password):
    key = generate_key(password)
    return key.encrypt(data)

def decrypt_data(data, password):
    key = generate_key(password)
    return key.decrypt(data)

# ---------------- STEGANOGRAPHY ---------------- #

def encode_audio(audio_path, secret_path, password, output_path):

    if not audio_path.lower().endswith(".wav"):
        raise ValueError("Only WAV audio files are supported")

    with open(secret_path, "rb") as f:
        secret_data = f.read()

    encrypted_data = encrypt_data(secret_data, password)
    secret_bits = ''.join(format(byte, '08b') for byte in encrypted_data) + '1111111111111110'

    audio = wave.open(audio_path, "rb")
    frames = bytearray(audio.readframes(audio.getnframes()))

    for i in range(len(secret_bits)):
        frames[i] = (frames[i] & 254) | int(secret_bits[i])

    with wave.open(output_path, "wb") as stego:
        stego.setparams(audio.getparams())
        stego.writeframes(frames)

    audio.close()

def decode_audio(audio_path, password, output_file):

    if not audio_path.lower().endswith(".wav"):
        return None

    try:
        audio = wave.open(audio_path, "rb")
        frames = bytearray(audio.readframes(audio.getnframes()))

        bits = ""
        for byte in frames:
            bits += str(byte & 1)
            if bits.endswith("1111111111111110"):
                break

        bits = bits[:-16]

        data = bytearray()
        for i in range(0, len(bits), 8):
            data.append(int(bits[i:i+8], 2))

        decrypted_data = decrypt_data(bytes(data), password)

        output_path = output_file + ".txt"
        with open(output_path, "wb") as f:
            f.write(decrypted_data)

        audio.close()
        return output_path

    except (InvalidToken, wave.Error):
        return None
