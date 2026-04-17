 🛡️ HomeCam - Facial Recognition Camera
 
 [![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
 [![Flask](https://img.shields.io/badge/Flask-3.x-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
 [![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=for-the-badge&logo=opencv)](https://opencv.org/)
 
 A simple, powerful home facial recognition system with live streaming and unknown person alerts.
 Beware, by default, this runs on HTTP and by nature, is insecure.
 Leaving `0.0.0.0:5000` open allows *anybody* access and is a bad idea in a production environment!
 
 ## Features
 
 - Real-time face recognition from any `/dev/videoX` device
 - Supports multiple known people (add photos to `known_faces/`)
 - Automatically saves unknown faces to `unknowns/` folder
 - Web dashboard with live MJPEG stream and capture button
 - Easy device selection at startup
 - Works remotely on your local network
 
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
 sudo apt install -y cmake build-essential pkg-config libatlas-base-dev libopenblas-dev libjpeg-dev python3-dev
 
 pip install --upgrade pip setuptools wheel
 pip install "setuptools<70.0.0"
 pip install -r requirements.txt
 pip install git+https://github.com/ageitgey/face_recognition_models
 pip install --no-deps --force-reinstall face_recognition
 ```
 
 3. **Add known faces**
 
 Add clear, frontal photos to the `known_faces/` folder:
 - `known_faces/Mom.jpg`
 - `known_faces/Dad.jpg`
 - `known_faces/Alice.jpg`
 etc. The filename (without extension) becomes the label.
 
 ## Running the App
 
 ```bash
 python app.py
 ```
 
 You will be prompted to enter your camera device (e.g. `/dev/video0` or `/dev/video2`).
 
 Then open your browser and go to:
 - `http://127.0.0.1:5000` (on the same machine)
 - or `http://YOUR_LOCAL_IP:5000` from other devices on your network.
 
 ## Project Structure
 
 ```
 known_faces/     ← Add one photo per person here
 unknowns/        ← Unknown faces are saved here automatically
 templates/
 app.py
 ```
 
 ## Troubleshooting
 
 - **Black screen**: Try a different `/dev/videoX` device. Your laptop webcam might be `/dev/video0`.
 - **Camera permission**: `sudo usermod -aG video $USER` then reboot.
 - **"No face found"**: Use well-lit, frontal photos in `known_faces/`.
 
 ## License
 
 MIT License
 
 Made with ❤️ by The-Incredible-Gamma-Man
