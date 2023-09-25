import socket

HOST = '0.0.0.0'    #or Replace "0.0.0.0" with the IP address that appears in the top left corner of the EV3 brick's screen.
                    #0.0.0.0 will listen every port available
PORT = 5555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((HOST, PORT))

server_socket.listen(1)
print("Waiting for a connection...")

client_socket, client_address = server_socket.accept()
print(f"Connection from {client_address}")

while True:
    try:
        data = client_socket.recv(1024).decode()
        if not data:
            print("Connection closed by client.")
            break

        if data == '...':
            print("...")
        elif data == ':right':
            print("right button pressed")

            file_size = int(client_socket.recv(1024).decode())
            with open('received_image.jpg', "wb") as file:
                received_size = 0
                while received_size < file_size:
                    jpg_chunk = client_socket.recv(1024)
                    if not jpg_chunk:
                        break
                    file.write(jpg_chunk)
                    received_size += len(jpg_chunk)
            print("Image received and saved as 'received_image.jpg'")

    except ConnectionResetError:
        print("Connection closed by client.")
        break

file.close()
client_socket.close()
server_socket.close()
