import cv2
import os

DELIMITER = "#####"

def xor_encrypt_decrypt(text, key):
    result = ""
    for i in range(len(text)):
        result += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    return result


def encode_video(video_path, secret_text, password, output_path):
    encrypted = xor_encrypt_decrypt(secret_text, password) + DELIMITER
    binary = ''.join(format(ord(c), '08b') for c in encrypted)

    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    out = cv2.VideoWriter(
        output_path,
        fourcc,
        cap.get(cv2.CAP_PROP_FPS),
        (
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )
    )

    index = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        for row in frame:
            for pixel in row:
                for i in range(3):
                    if index < len(binary):
                        pixel[i] = (pixel[i] & 254) | int(binary[index])
                        index += 1

        out.write(frame)

    cap.release()
    out.release()


def decode_video(stego_path, password):
    cap = cv2.VideoCapture(stego_path)
    bits = ""

    delimiter_binary = ''.join(format(ord(c), '08b') for c in DELIMITER)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        for row in frame:
            for pixel in row:
                for i in range(3):
                    bits += str(pixel[i] & 1)
                    if bits.endswith(delimiter_binary):
                        cap.release()
                        bits = bits[:-len(delimiter_binary)]

                        chars = [
                            chr(int(bits[i:i+8], 2))
                            for i in range(0, len(bits), 8)
                        ]

                        encrypted_text = ''.join(chars)
                        return xor_encrypt_decrypt(encrypted_text, password)

    return None
