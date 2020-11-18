# coding : utf-8

import sys
from PyQt5 import uic,QtCore,QtGui,QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage,QPixmap
from flask import Flask, render_template, Response
import api1
from urllib import *
import time
import threading


from flask import Flask, render_template, Response
from camera import VideoCamera




from camera import VideoCamera
import cv2

face_cascade=cv2.CascadeClassifier("haarcascade_frontface.xml")
ds_factor=0.6

form_class = uic.loadUiType("fream.ui")[0]  #ui파일을 불러 온다.




###########################################################
######################  MAIN  #############################
###########################################################
                    
class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        main_cam.gen(camera)

        t1 = threading.Thread(target=self.pm25)
        t1.daemon=True
        t1.start()
        
     
       
        
        app = Flask(__name__)
        @app.route('/')
        def index():
            # rendering webpage
            return render_template('index.html')
        def gen(camera):
            while True:
                #get camera frame
                frame = camera.get_frame()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        @app.route('/video_feed')
        def video_feed():
            return Response(gen(VideoCamera()),
                            mimetype='multipart/x-mixed-replace; boundary=frame')
        
        
        
####################################################
    
    def set_Image(self,image):
        self.label_cctv.setPixmap(QPixmap.fromImage(image))
    def pm25(self):
        while True:
            api_pm25 = api1.pm25_value
            api_humi = api1.api_humidity
            api_temp = api1.weather_data

            self.lcdNumber_api_pm25.display(api_pm25)
            self.lcdNumber_api_humidity.display(api_humi)
            self.lcdNumber_api_temperature.display(api_temp)
    def closeEvent(self,e):
        self.cam_thread.stop()


######################################################
######################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.run(host='192.168.0.5')
    sys.exit(app.exec_())