import socket
import subprocess
import numpy as np
import cv2

host = 'localhost'
port = 6969

vlc_location = '/Applications/VLC.app/Contents/MacOS/VLC'

def recieve():
    usr = input('ingrese el usuario: ')
    pwd = input('ingrese la contraseña: ')
    print('Canales:\n    1.Hubbabubbaklubb - Mopedbart\n    2.The Killers - Human')
    canal = input('ingrese el numero del canal que desea ver: ')

    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.connect((host,port))
    s.send((usr + '///' + pwd + '///' + canal).encode('utf-8'))
    print('Conectado por el puerto', port)


    encoded_frame = s.recv(1024)
    queue = []

    while True:
        encoded_frame += s.recv(1024)
        if(len(encoded_frame)) == 2764800:
            frame = np.frombuffer(encoded_frame, dtype=np.uint8).reshape(720,1280,3)
            queue.append(frame)
            cv2.imshow(('Canal'+ str(canal)), frame)
            encoded_frame = s.recv(1024)

if __name__ == "__main__":
    recieve()
    cv2.destroyAllWindows()