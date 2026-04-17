from flask import Flask, render_template, Response, flash
import cv2
import face_recognition
import os
from datetime import datetime
import time
import threading

app = Flask(__name__)
app.secret_key = 'super-secret-key'

# ========================= CONFIG =========================
print("🔧 HomeCam Setup")
DEVICE_PATH = input("Enter the capture device location (e.g. /dev/video0 or /dev/video2): ").strip()

if not DEVICE_PATH:
    DEVICE_PATH = "/dev/video2"
    print(f"No input given, defaulting to {DEVICE_PATH}")

TOLERANCE = 0.55
ALERT_COOLDOWN = 30

known_faces = {}
last_alert_time = 0
cap = None
lock = threading.Lock()

def load_known_faces():
    global known_faces
    known_dir = "known_faces"
    os.makedirs(known_dir, exist_ok=True)
    known_faces.clear()
    count = 0
    for filename in os.listdir(known_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            name = os.path.splitext(filename)[0]
            path = os.path.join(known_dir, filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_faces[name] = encodings[0]
                print(f"✅ Loaded known face: {name}")
                count += 1
    print(f"Loaded {count} known faces.")
    return count > 0

def gen_frames():
    global cap, last_alert_time
    if cap is None or not cap.isOpened():
        print(f"🎥 Opening camera: {DEVICE_PATH}")
        cap = cv2.VideoCapture(DEVICE_PATH, cv2.CAP_V4L)
        
        if not cap.isOpened():
            print("❌ Failed to open camera. Check the path and permissions.")
            return

        # Camera settings
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        for fourcc in ['MJPG', 'YUYV', 'H264']:
            cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*fourcc))
            if int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) > 0:
                print(f"✅ Camera ready at {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")
                break

    while True:
        with lock:
            success, frame = cap.read()
            if not success:
                time.sleep(0.1)
                continue

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb, model="hog")
            face_encodings = face_recognition.face_encodings(rgb, face_locations)

            unknown_detected = False

            for (top, right, bottom, left), enc in zip(face_locations, face_encodings):
                name = "UNKNOWN"
                color = (0, 0, 255)
                for kname, kenc in known_faces.items():
                    if face_recognition.compare_faces([kenc], enc, tolerance=TOLERANCE)[0]:
                        name = kname
                        color = (0, 255, 0)
                        break
                if name == "UNKNOWN":
                    unknown_detected = True

                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

            if unknown_detected and (time.time() - last_alert_time) > ALERT_COOLDOWN:
                last_alert_time = time.time()
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                os.makedirs("unknowns", exist_ok=True)
                path = f"unknowns/unknown_{ts}.jpg"
                cv2.imwrite(path, frame)
                print(f"🚨 Unknown face saved: {path}")

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    load_known_faces()
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    load_known_faces()
    print(f"\n🚀 HomeCam running on http://0.0.0.0:5000")
    print(f"   Using camera: {DEVICE_PATH}")
    app.run(debug=True, host='0.0.0.0', port=5000)
