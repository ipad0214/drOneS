from flask import Flask, Response
from camera import VideoCamera
  
    
def run(onArm): 
    app = Flask(__name__)        

    #@app.route('/')
    #def index():
    #   return "hello world"
    
    def gen(camera):
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
    @app.route('/')
    def video_feed():
        return Response(gen(VideoCamera(onArm)),
                        mimetype='multipart/x-mixed-replace; boundary=frame')      
    
    app.run(port=50000, debug=True, threaded=True, use_reloader=False)