from flask import Flask, render_template, Response
import cv2
import face_recognition as fr
import numpy as np
import os

app = Flask(__name__)

def Recognizer(AllPersonName, AllEncodingData, frame):
    RGBFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    CapturedFaceLocations = fr.face_locations(RGBFrame)
    AllCapturedFaceEncodings = fr.face_encodings(RGBFrame, CapturedFaceLocations)

    detected_names = []

    for EachCapturedFaceEncodingData in AllCapturedFaceEncodings:
        matches = fr.compare_faces(AllEncodingData, EachCapturedFaceEncodingData)
        PersonName = ""
        FaceDistance = fr.face_distance(AllEncodingData, EachCapturedFaceEncodingData)
        BestMatchIndex = np.argmin(FaceDistance)
        if matches[BestMatchIndex]:
            PersonName = AllPersonName[BestMatchIndex]
            detected_names.append(PersonName)

    return detected_names

def ImageProcessor(frame):
    ImageEncoding = fr.face_encodings(frame)[0]
    return ImageEncoding

@app.route('/')
def index():
    return render_template('index.html')

def video_feed():
    vCap = cv2.VideoCapture(0)
    PhotoDirectory = "./photos"
    AllPhotoName = os.listdir(PhotoDirectory)
    AllPhotoPath = []
    AllPhotoEncodingData = []
    AllPersonName = []
    
    for EachName in AllPhotoName:
        AllPhotoPath.append(os.path.join(PhotoDirectory, EachName))
        AllPersonName.append(EachName.split(".")[0])
    
    for EachPath in AllPhotoPath:
        ImageData = fr.load_image_file(EachPath)
        AllPhotoEncodingData.append(ImageProcessor(ImageData))

    while True:
        success, frame = vCap.read()
        if not success:
            break

        detected_names = Recognizer(AllPersonName, AllPhotoEncodingData, frame)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    vCap.release()

@app.route('/video_feed')
def video_feed_route():
    return Response(video_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='192.168.1.110', debug=False)
