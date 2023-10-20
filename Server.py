import cv2
import socket
import struct
import pickle

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.1.109', 12345))
server_socket.listen(5)

fps=15

cap = cv2.VideoCapture(0)
cap.set(5, fps) 

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    if client_socket:
        while True:
            ret, frame = cap.read()

            frame = cv2.resize(frame, (320, 240))
            _, encoded_frame = cv2.imencode('.jpg', frame)
            data = pickle.dumps(encoded_frame)

            message_size = struct.pack("L", len(data))
            client_socket.sendall(message_size + data)

cap.release()
server_socket.close()
