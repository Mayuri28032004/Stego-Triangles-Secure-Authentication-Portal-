from flask import Flask, render_template, request, send_file, redirect, url_for, session
import os
from audio_stego import encode_audio, decode_audio
from image_stego import encode_image, decode_image
from video_stego import encode_video, decode_video

app = Flask(__name__)
app.secret_key = "stego_triangle_secure_key_2026"  # Required for session management

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 🔼 In-memory user storage (Resets when server restarts)
USER_DATA = {"admin": "admin123"}

# ================= AUTHENTICATION ROUTES =================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username in USER_DATA and USER_DATA[username] == password:
            session["user"] = username
            # UPDATED: Redirect to dashboard instead of index
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="❌ Invalid Username or Password")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")
        
        if u in USER_DATA:
            return render_template("register.html", error="❌ User already exists!")
        
        USER_DATA[u] = p
        return render_template("login.html", success="✅ Registration Successful! Please Login.")
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# ================= DASHBOARD (NEW HOME) =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dash.html")

# ================= AUDIO PAGE (index.html) =================
@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("index.html")

# ================= IMAGE PAGE =================
@app.route("/image")
def image():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("image.html")

# ================= VIDEO PAGE =================
@app.route("/video")
def video():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("video_stego.html")

# ================= AUDIO ENCODE =================
@app.route("/encode", methods=["POST"])
def encode():
    if "user" not in session: return redirect(url_for("login"))
    
    audio = request.files["audio"]
    secret = request.files["secret"]
    password = request.form["password"]

    audio_path = os.path.join(UPLOAD_FOLDER, audio.filename)
    secret_path = os.path.join(UPLOAD_FOLDER, secret.filename)
    output_audio = os.path.join(OUTPUT_FOLDER, "stego.wav")

    audio.save(audio_path)
    secret.save(secret_path)

    encode_audio(audio_path, secret_path, password, output_audio)
    return send_file(output_audio, as_attachment=True)

# ================= AUDIO DECODE =================
@app.route("/decode", methods=["POST"])
def decode():
    if "user" not in session: return redirect(url_for("login"))
    
    audio = request.files["audio"]
    password = request.form["password"]

    audio_path = os.path.join(UPLOAD_FOLDER, audio.filename)
    output_file = os.path.join(OUTPUT_FOLDER, "extracted_secret")
    audio.save(audio_path)

    extracted_file = decode_audio(audio_path, password, output_file)

    if extracted_file is None:
        return render_template("index.html", error="❌ Wrong password or corrupted file!", highlight_password=True)

    return send_file(extracted_file, as_attachment=True)

# ================= IMAGE ENCODE =================
@app.route("/image_encode", methods=["POST"])
def image_encode():
    if "user" not in session: return redirect(url_for("login"))
    
    image = request.files["image"]
    message = request.form["message"]
    password = request.form["password"]

    if len(password) < 8:
        return render_template("image.html", error="❌ Password must be at least 8 characters long")

    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)
    
    output_image = os.path.join(OUTPUT_FOLDER, "stego_image.png")
    result = encode_image(image_path, message, password, output_image)

    if result and os.path.exists(result):
        return send_file(result, as_attachment=True)
    else:
        return render_template("image.html", error="❌ Encoding failed. Image may be too small.")

# ================= IMAGE DECODE =================
@app.route("/image_decode", methods=["POST"])
def image_decode():
    if "user" not in session: return redirect(url_for("login"))
    
    image = request.files["image"]
    password = request.form["password"]

    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    secret = decode_image(image_path, password)

    if secret is None or "Error" in secret:
        return render_template("image.html", error="❌ Incorrect password or no hidden message found.")

    return render_template("image.html", success="✅ Message Extracted Successfully", secret_message=secret)

# ================= VIDEO ENCODE =================
@app.route("/video_encode", methods=["POST"])
def video_encode():
    if "user" not in session: return redirect(url_for("login"))
    
    video = request.files["video"]
    secret = request.form["secret"]
    password = request.form["password"]

    video_path = os.path.join(UPLOAD_FOLDER, video.filename)
    output_video = os.path.join(OUTPUT_FOLDER, "stego_video.avi")

    video.save(video_path)
    encode_video(video_path, secret, password, output_video)

    return send_file(output_video, as_attachment=True)

# ================= VIDEO DECODE =================
@app.route("/video_decode", methods=["POST"])
def video_decode():
    if "user" not in session: return redirect(url_for("login"))
    
    video = request.files["video"]
    password = request.form["password"]

    video_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(video_path)

    secret = decode_video(video_path, password)

    if secret is None:
        return render_template("video_stego.html", error="❌ Wrong password or invalid video file.")

    output_file = os.path.join(OUTPUT_FOLDER, "video_secret.txt")
    with open(output_file, "w") as f:
        f.write(secret)

    return send_file(output_file, as_attachment=True)

# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)