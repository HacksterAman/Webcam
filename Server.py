import cv2
import socket
import struct
import zlib
import pickle

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.1.109', 12345))
server_socket.listen(5)

cap = cv2.VideoCapture(0)

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    if client_socket:
        while True:
            ret, frame = cap.read()

            frame = cv2.resize(frame, (640, 480))

            compressed_frame = zlib.compress(pickle.dumps(frame), level=zlib.Z_BEST_SPEED)

            message_size = struct.pack("L", len(compressed_frame))
            client_socket.sendall(message_size + compressed_frame)

cap.release()
server_socket.close()
