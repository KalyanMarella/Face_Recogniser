from flask import Flask,Response,url_for,render_template,request
import numpy as np
import cv2 as cv
import joblib
import face_recognition
app=Flask(__name__)
mapp={0:'chiranjeevi',1:'modi',2:'nagarjuna',3:'rajinikanth'}
def face_of_image(image):
    face_location=face_recognition.face_locations(image)
    if len(face_location)!=0:
        top,right,bottom,left=face_location[0]
        image=image[top:bottom,left:right]   
    return image 

model=joblib.load('models/face_recognizer.joblib')

@app.route('/')
def interface():
    return render_template('interface.html')

@app.route('/submit',methods=['POST'])
def getting_data():
    image=request.files["image-input"]
    file_bytes=np.frombuffer(image.read(),np.uint8)
    image=cv.imdecode(file_bytes,cv.IMREAD_COLOR)
    face=face_of_image(image)
    test=face.astype(np.float32)/(255.0)
    test=cv.resize(test,(100,100))
    image=cv.resize(image,(100,100))
    test=test.reshape(-1,100,100,3).copy()
    name=mapp[model.predict(test).argmax()]
    cv.rectangle(image,(0,80),(100,100),(0,0,255),cv.FILLED)
    cv.putText(image,name,(0,90),cv.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    print(name)
    ret, buffer = cv.imencode('.jpg', image)
    if not ret:
        return "Error encoding image", 500
    image_bytes=buffer.tobytes()
    return Response(image_bytes,mimetype='image/jpeg')
if __name__=='__main__':
    app.run(debug=True)
    
