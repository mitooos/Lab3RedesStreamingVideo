import socket
from _thread import *
import threading
import cv2
import numpy as np


port = 6969
host = '0.0.0.0'

video1 = 'arch1.mp4'

video2 = 'arch2.mp4'

direcciones_canal_1 = []
direcciones_canal_2 = []

def stream(canal):
    while True:
        if canal == 1:
            cap = cv2.VideoCapture(video1)
            direcciones = direcciones_canal_1
        if canal == 2:
            cap = cv2.VideoCapture(video2)
            direcciones = direcciones_canal_2
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                encoded_frame = frame.tobytes()
                
                # parte el arreglo en chunks mas pequeños para poder ser enviados
                for i in range(0,2764800,55296):
                    chunk = encoded_frame[i:i+720]
                    for addr in direcciones:
                        s.sendto(chunk, addr)

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
            else:
                break

        cap.release()

def receive_connections():
    while True:
        data, address = s.recvfrom(1024)
        print('Se inicio una conexión con la direccion:', address)
        data = data.decode('utf-8').split('///')
        print('Se recibio el usuario y contraseña:', data[:2])
        canal = int(data[2])
        if canal == 1:
            direcciones_canal_1.append(address)
        else:
            direcciones_canal_2.append(address)
        
        
    

port = 6969
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
print('Socket esta escuchando en el puerto: ' + str(port))

start_new_thread(stream,(1,))
start_new_thread(stream,(2,))

receive_connections()


s.close()
    