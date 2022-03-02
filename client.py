import socket


def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 65432  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = input(" -> ")  # take input

    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()









#import socket

#HOST = "127.0.0.1"  # The server's hostname or IP address
#PORT = 65432  # The port used by the server

#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#    s.connect((HOST, PORT))
#    s.sendall(b"Hello, world")
#   data = s.recv(1024)

#print(f"Received {data!r}")