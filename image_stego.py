from PIL import Image
import hashlib
import base64
from cryptography.fernet import Fernet, InvalidToken
import os

# Generate a Fernet key from password
def generate_key(password):
    hash = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(hash))

# Encrypt binary data using password
def encrypt_data(data, password):
    return generate_key(password).encrypt(data)

# Decrypt binary data using password
def decrypt_data(data, password):
    return generate_key(password).decrypt(data)

# Encode secret file into an image
def encode_image(image_path, secret_data_text, password, output_path):
    try:
        # 1. Open any image format (JPG, BMP, PNG) and convert to RGB
        img = Image.open(image_path)
        img = img.convert("RGB")
        pixels = list(img.getdata())

        # 2. Prepare the data (handling text input from your Flask form)
        # If secret_data_text is the actual message string:
        secret_bytes = secret_data_text.encode()

        # 3. Encrypt the data
        encrypted = encrypt_data(secret_bytes, password)

        # 4. Convert encrypted data to binary
        binary_data = ''.join(format(byte, '08b') for byte in encrypted)
        delimiter = '1111111111111110'  # end-of-data marker
        binary_data += delimiter

        # Check if image can hold the secret
        if len(binary_data) > len(pixels) * 3:
            return "Error: Image too small!"

        # 5. Encode binary data into image LSB
        new_pixels = []
        data_index = 0
        
        for pixel in pixels:
            pixel = list(pixel) # Convert tuple to list to modify
            for i in range(3): # R, G, B channels
                if data_index < len(binary_data):
                    pixel[i] = (pixel[i] & 254) | int(binary_data[data_index])
                    data_index += 1
            new_pixels.append(tuple(pixel))

        # 6. CRITICAL FIX: Force Save as PNG
        # PNG is lossless, JPG will destroy the data.
        # We ensure the output path ends in .png
        if not output_path.lower().endswith('.png'):
            output_path = os.path.splitext(output_path)[0] + ".png"

        img.putdata(new_pixels)
        img.save(output_path, "PNG") # Explicitly save as PNG
        return output_path

    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

# Decode secret file from an image
def decode_image(image_path, password):
    try:
        img = Image.open(image_path)
        img = img.convert("RGB")
        pixels = list(img.getdata())

        bits = ""
        for pixel in pixels:
            for channel in pixel:
                bits += str(channel & 1)
                if bits.endswith("1111111111111110"):
                    break
            if bits.endswith("1111111111111110"):
                break

        if not bits.endswith("1111111111111110"):
            return None # No message found

        bits = bits[:-16]  # remove delimiter

        data = bytearray()
        for i in range(0, len(bits), 8):
            data.append(int(bits[i:i+8], 2))

        # Decrypt data
        decrypted = decrypt_data(bytes(data), password)
        return decrypted.decode() # Return as string for your Flask UI

    except InvalidToken:
        return "Error: Incorrect password or corrupted data!"
    except Exception as e:
        print(f"Error decoding image: {e}")
        return None