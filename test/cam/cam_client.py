# http://picamera.readthedocs.org/en/release-1.3/recipes1.html
# 4.12. Recording to a network stream
import socket
import time
import picamera

myserver ='192.168.1.17'
# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(( myserver, 8000))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.rotation = 180
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)
        # Start recording, sending the output to the connection for 60
        # seconds, then stop
        camera.start_recording(connection, format='h264')
        camera.wait_recording(60)
        camera.stop_recording()
finally:
    connection.close()
    client_socket.close()
