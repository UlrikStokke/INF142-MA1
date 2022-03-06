import socket

from rich import print
from rich.prompt import Prompt
from rich.table import Table

from champlistloader import load_some_champs
from core import Champion, Match, Shape, Team


def client_program():
    host = "127.0.0.1"  # as both code is running on same pc
    port = 65432  # socket server port number

    print("Connecting to server")
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    print("Connected to server: " + host + " " + str(port))

    print('''Welcome to Team Local Tactics!
             Each player choose a champion each time.''')
    
 #   message = input(" -> ")  # take input

    # Create a table containing available champions
    available_champs = Table(title='Available champions')
    
    # Add the columns Name, probability of rock, probability of paper and
    # probability of scissors
    available_champs.add_column("Name", style="cyan", no_wrap=True)
    available_champs.add_column("prob(:raised_fist-emoji:)", justify="center")
    available_champs.add_column("prob(:raised_hand-emoji:)", justify="center")
    available_champs.add_column("prob(:victory_hand-emoji:)", justify="center")

    while True:
        data_name = client_socket.recv(1024).decode()  # receive data
        if data_name == "complete":
            break
        client_socket.send("ok".encode())
        data_p1 = client_socket.recv(1024).decode()  # receive data
        client_socket.send("ok".encode())
        data_p2 = client_socket.recv(1024).decode()  # receive data
        client_socket.send("ok".encode())
        data_p3 = client_socket.recv(1024).decode()  # receive data
        client_socket.send("ok".encode())
        #print("received: " + data_name + " ...")
        data_list = [data_name, data_p1, data_p2, data_p3]
        tpl = tuple(data_list)
        available_champs.add_row(*tpl)

    print(available_champs)

    while True:
        champ_1 = client_socket.recv(1024).decode()
        choice_1 = input(f"{champ_1}")
#        print(choice_1)
        client_socket.send(choice_1.encode())
        answer = client_socket.recv(1024).decode()
        if answer == "ok":
            break
        else:
            print(answer)

#    print("completed - champ1")
    
    while True:
        champ_2 = client_socket.recv(1024).decode()
        choice_2 = input(f"{champ_2}")
#        print(choice_2)
        client_socket.send(choice_2.encode())
        answer = client_socket.recv(1024).decode()
        if answer == "ok":
            break
        else:
            print(answer)

#    print("completed - champ2")
    while True:
        data = client_socket.recv(1024)

   #while message.lower().strip() != 'bye':
    #    client_socket.send(message.encode())  # send message
     #   data = client_socket.recv(1024).decode()  # receive response

      #  print('Received from server: ' + data)  # show in terminal

       # message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()