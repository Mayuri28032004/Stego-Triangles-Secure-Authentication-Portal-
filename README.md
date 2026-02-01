Stego Triangle 🚀
Stego Triangle is a secure multimedia steganography web application designed to conceal confidential information within audio, image, and video files. By combining encryption with data-hiding techniques, it ensures that sensitive information remains both unreadable and unnoticed.

✨ Key Features
Audio Steganography: Uses Least Significant Bit (LSB) encoding on WAV files.
Image Steganography: Hides secret text within PNG/JPG pixels.
Video Steganography: Implements frame-based steganography for video files.
Dual-Layer Security: Integrates AES encryption and password-based locks to prevent unauthorized access.
Modern UI: Features a dark-themed, responsive web interface built with Glassmorphism CSS.

1. FOLDER STRUCTURE
------------------
secure-audio-stego/
│
├── app.py              # Flask Backend / Controller
├── audio_stego.py      # Audio Steganography Logic
├── image_stego.py      # Image Steganography Logic
├── video_stego.py      # Video Steganography Logic
│
├── static/             # Assets Folder
│   └── style.css       # Global Project Styling
│
├── templates/          # UI Components (HTML)
│   ├── login.html      # Authentication
│   ├── register.html   # User Signup
│   ├── dash.html       # Project Dashboard
│   ├── index.html      # Audio Module
│   ├── image.html      # Image Module
│   └── video_stego.html# Video Module
│
├── uploads/            # Temporary storage for input files
└── outputs/            # Storage for encoded/decoded files

2. PREREQUISITES
---------------
Ensure Python 3.x is installed. Install required libraries:
pip install flask pillow cryptography opencv-python numpy

3. HOW TO RUN
------------
1. Open terminal/command prompt in the "secure-audio-stego" folder.
2. Execute command: python app.py
3. Open browser and visit: http://127.0.0.1:5000
4. Default login: admin / admin123

4. CORE TECHNOLOGIES
-------------------
- Backend: Flask (Python)
- Frontend: HTML5, CSS3 (Glassmorphism UI)
- Security: Cryptography (Fernet/AES), LSB manipulation


📂 Project Modules
Login Portal: Secure authentication for users to access the "Vault".
Encoding: Upload a media file, enter a secret message/file, and set a password to generate a "Stego" file.
Decoding: Upload a Stego file and provide the correct password to extract the hidden data.


👥 Authors
Mayuri P. Bobade
Harshika D. Chhoundiya
Guide: Prof. Pravin Dhande|Prof. Kesar Ma'am.
