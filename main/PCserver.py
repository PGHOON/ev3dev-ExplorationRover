import socket
import numpy as np
from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
from PIL import Image

Server_Addr = ('192.168.2.2', 12344)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(Server_Addr)

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


            ### predicting the Image ###
            CLASSES = ['Apple', 'Avocado', 'Kiwi', 'Pineapple', 'Cherry', 'Watermelon', 'Mango', 'Banana', 'Orange', 'Strawberry']
            model = load_model('model.h5')      #Train accuracy : 97%, Test accuracy : 45%
            image_path = 'received_image.jpg'   #A pretty decent model, considering that the class number is 10.
            img = Image.open(image_path)
            img = img.resize((32, 32))
            img = np.array(img)
            img = np.expand_dims(img, axis=0)
            img = preprocess_input(img)

            predictions = model.predict(img)

            predicted_class_index = np.argmax(predictions, axis=1)
            predicted_class_name = CLASSES[predicted_class_index[0]]

            print("Predicted class:", predicted_class_name)

    except ConnectionResetError:
        print("Connection closed by client.")
        break

file.close()
client_socket.close()
server_socket.close()