"""
Webcam Streamer

Uses Pygame and HTTPServer to stream USB Camera images via HTTP (Webcam)

HTTP Port, camera resolutions and framerate are hardcoded to keep it
simple but the program can be updated to take options.

Default HTTP Port 8080, 320x240 resolution and 6 frames per second.
Point your browser at http://localhost:8080/

http://www.madox.net/
"""
import pygame
import pygame.camera
import datetime
import signal
import sys
import tempfile
import threading
import time
import os
import BaseHTTPServer
import SocketServer
      
class CameraCapture():
    def __init__(self, device, resolution, fps):
        # Initialize the camera
        self.camera = pygame.camera.Camera(device, resolution)
        self.camera.start()
        
        # Set up a CameraSurface Buffer
        self.camera_surface = pygame.Surface(resolution)
        self.jpeg = ""
        self.jpeg_sema = threading.BoundedSemaphore()
        self.period = 1 / float(fps)
        self.stop = True
        
        # Prepare conditions
        self.frame_count = 0
        self.frame_available = threading.Condition()
        
        # Kick it off
        self.start_capture()

    def get_image(self):
        self.jpeg_sema.acquire()
        jpeg_copy = self.jpeg
        self.jpeg_sema.release()
        return jpeg_copy
  
    def stop_capture(self):
        self.stop = True
  
    def start_capture(self):
        if self.stop == True:
            self.stop = False
            self.capture_image()
      
    def capture_image(self):
        # Time start
        time_start = time.time()
    
        # Capture the image [Blocking until image received]
        self.camera_surface = self.camera.get_image(self.camera_surface)
        
        # Using a tempfile here because pygame image save gets
        # filetype from extension.  Limiting module use so no PIL.
        temp_jpeg = tempfile.NamedTemporaryFile(suffix='.jpg')
        pygame.image.save(self.camera_surface, temp_jpeg.name)
        
        # Read back the JPEG from the tempfile and store it to self
        temp_jpeg.seek(0)
        self.jpeg_sema.acquire()
        self.jpeg = temp_jpeg.read()
        self.jpeg_sema.release()
        temp_jpeg.close()
        
        # Increment frame count and mark new frame condition
        self.frame_available.acquire()
        self.frame_count += 1
        self.frame_available.notifyAll()
        self.frame_available.release()
        
        # If not stopped, prepare for the next capture        if self.stop == False:
        time_elapsed = time.time() - time_start
        if time_elapsed >= self.period:
            time_wait = 0
        else:
            time_wait = self.period - time_elapsed
        t = threading.Timer(time_wait, self.capture_image)
        t.start()

class HTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    doVideo = True
    def __init__(self, server_address, cam_dev, cam_res, cam_fps):
        SocketServer.TCPServer.__init__(self, server_address, HTTPHandler)
        self.camera = CameraCapture(cam_dev, cam_res, cam_fps)
    def thisIsThere(self):
        HTTPHandler.thisIsThere(SocketServer)
    
class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    HTTP Request Handler
    """
   
    def do_GET(self): 
        
        if  self.server.doVideo:  
            # Boundary is an arbitrary string that should not occur in the
            # data stream, using own website address here
            boundary = "www.madox.net" 
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Content-type",
                             "multipart/x-mixed-replace;boundary=%s"
                             % boundary)
            self.end_headers()        
            
            frame_id = self.server.camera.frame_count
            
            while self.server.doVideo:
                self.server.camera.frame_available.acquire()
                while frame_id == self.server.camera.frame_count:
                    self.server.camera.frame_available.wait()      
                self.server.camera.frame_available.release()
                
                frame_id = self.server.camera.frame_count
                response = "Content-type: image/jpeg\n\n"
                response = response + self.server.camera.get_image()
                response = response + "\n--%s\n" % boundary
                self.wfile.write(response)    
            
        else:
            response = self.server.camera.get_image()
            self.send_response(200)
            self.send_header("Content-Length", str(len(response)))
            self.send_header("Content-Type", "image/jpeg")
            self.end_headers()
            self.wfile.write(response)    
    do_HEAD = do_POST = do_GET

class CameraCaptureServer(threading.Thread):
    #myCameraCapture = None
    #http_server = None
    #http_server_thread = None
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        pygame.init()
        pygame.camera.init()
        #signal.signal(signal.SIGINT, quit)
        #signal.signal(signal.SIGTERM, quit)
        self.http_server = HTTPServer(server_address=("", 8080),
                            cam_dev="/dev/video0",
                            cam_res=(320, 240),
                            cam_fps=15)
        self.http_server_thread = threading.Thread(target=self.http_server.serve_forever())
        self.http_server_thread.setDaemon(True)
        self.http_server_thread.start()
        
    def stopCamera(self):
        self.http_server.camera.stop_capture()
        self.http_server.camera.camera.stop()
        #HTTPServer.shutdown(self.http_server)
        #self.http_server.shutdown()
        
    def showVideo(self):
        self.http_server.doVideo = True
        
    def takePicture(self, path):
        now = datetime.datetime.now()
        filePath = path + "/" + str(now.year) + "/" + str(now.month)+ "/" + str(now.day) + "/"+ str(now.hour) + "-" + str(now.minute) + "-" + str(now.microsecond) + ".jpeg"
        if not os.path.exists(filePath[0:filePath.rfind("/")]):
            os.makedirs(filePath[0:filePath.rfind("/")])
        pygame.image.save(self.http_server.camera.camera_surface, filePath)
        self.http_server.doVideo = False
        return filePath
if __name__ == '__main__':

    """
  print "Started webcam streamer"

  def quit(signum, frame):
    print "Quitting..."
    http_server.camera.stop_capture()
    sys.exit(0)

  pygame.init()
  pygame.camera.init()
  
  signal.signal(signal.SIGINT, quit)
  signal.signal(signal.SIGTERM, quit)

  # Localhost, Port 8080, camres=320x240, fps=6
  http_server = HTTPServer(server_address=("", 8080),
                            cam_dev="/dev/video0",
                            cam_res=(320, 240),
                            cam_fps=15)
  
  http_server_thread = threading.Thread(target=
                                       http_server.serve_forever())
  http_server_thread.setDaemon(true)
  http_server_thread.start()
  
  try:
    while True:
      http_server_thread.join(60)
  except KeyboardInterrupt:
    quit()
"""