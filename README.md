 🛡️ HomeCam - Facial Recognition Camera
 
 [![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
 [![Flask](https://img.shields.io/badge/Flask-3.x-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
 [![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=for-the-badge&logo=opencv)](https://opencv.org/)
 
 A simple, powerful home facial recognition system with live streaming and unknown person alerts.
 
 ## Features
 
 - Real-time face recognition from any `/dev/videoX` device
 - Supports multiple known people (add photos to `known_faces/`)
 - Automatically saves unknown faces to `unknowns/` folder
 - Web dashboard with live MJPEG stream and capture button
 - Easy device selection at startup
 - HTTPS with mkcert
 - Works remotely from your local network
 
 ## Setup
 
 1. **Clone or download the repository**
 
 ```bash
 git clone https://github.com/The-Incredible-Gamma-Man/Facial_Recognition_Python.git
 cd Facial_Recognition_Python
 ```
 
 2. **Create virtual environment and install dependencies**
 
 ```bash
 python3 -m venv venv
 source venv/bin/activate
 
 sudo apt update
 sudo apt install -y cmake build-essential pkg-config libatlas-base-dev libopenblas-dev libjpeg-dev python3-dev libnss3-tools
 
 pip install --upgrade pip setuptools wheel
 pip install "setuptools<70.0.0"
 pip install -r requirements.txt
 pip install git+https://github.com/ageitgey/face_recognition_models
 pip install --no-deps --force-reinstall face_recognition
 ```
 
 3. **Add known faces**
 
 Add clear frontal photos (e.g. `Mom.jpg`) to the `known_faces/` folder. The filename without extension becomes the displayed name.
 
 ## HTTPS Setup with mkcert (Recommended)

**Change `YOUR_LOCAL_IP` before hitting enter**
 
 ```bash
 # Install mkcert
 curl -JLO "https://dl.filippo.io/mkcert/latest?for=linux/amd64"
 chmod +x mkcert-v*-linux-amd64
 sudo cp mkcert-v*-linux-amd64 /usr/local/bin/mkcert
 mkcert -install
 
 # Generate certificates
 mkdir -p certs
 cd certs
 mkcert -cert-file cert.pem -key-file key.pem localhost 127.0.0.1 ::1 YOUR_LOCAL_IP
 ```
 
 ## Running the App
 
 ```bash
 python app.py
 ```
 
 You will be prompted for your camera device. The app now runs on **HTTPS port 5000**.
 
 Access: `https://127.0.0.1:5000` or `https://YOUR_LOCAL_IP:5000`
 
 ## Project Structure
 
 ```
 known_faces/     ← Add one photo per person here
 unknowns/        ← Unknown faces are saved here automatically
 certs/           ← cert.pem and key.pem (for HTTPS)
 templates/
 app.py
 ```
 
 ## Troubleshooting
 
 - **Black screen**: Try a different `/dev/videoX` device.
 - **Camera permission**: `sudo usermod -aG video $USER` then reboot.
 - **"No face found"**: Use well-lit, frontal photos in `known_faces/`.
 - **HTTPS warnings**: Run `mkcert -install` again and restart your browser.
 - **Remote access**: Include your local IP when generating the certificate with mkcert.
 
 ## License
 
 MIT License
 
 Made with ❤️ by The-Incredible-Gamma-Man
