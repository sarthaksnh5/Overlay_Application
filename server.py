from flask import Flask, render_template, Response, request
import cv2
import requests
import threading

app = Flask(__name__)

# Function to get frames from camera
def get_frame():
    camera = cv2.VideoCapture(0)  # Change the index (0) if your camera is on a different device
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Function to get content from another URL
def get_external_content(url):
    response = requests.get(url)
    return response.content

@app.route('/')
def index():
    return render_template('index.html')

# Route to stream camera
@app.route('/video_feed')
def video_feed():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to load content from another URL
@app.route('/external_content')
def external_content():
    external_url = request.args.get('url')
    content = get_external_content(external_url)
    return content

if __name__ == '__main__':
    # Start a thread to continuously get frames from camera
    threading.Thread(target=app.run, kwargs={'debug': False, 'threaded': True}).start()
