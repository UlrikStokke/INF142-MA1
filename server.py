from operator import truediv
import socket
from champlistloader import load_some_champs
from core import Match
from core import Team
from core import Champion

def send_champions(champions, conn):
    for i in champions:
        c = champions[i]
        tpl = c.str_tuple
        print("Read tuple: ")
        print(tpl)
        for n in tpl:
            print("Sending string: " + n)
            conn.sendall(n.encode())
            data = conn.recv(1024) # receive "ok"
    print("Sending complete: ")
    conn.sendall("complete".encode())
 
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
champions = load_some_champs()



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("Server listening for player 1.")
    s.listen()
    conn1, addr1 = s.accept()
    print("Server listening for player 2.")
    s.listen()
    conn2, addr2 = s.accept()

    print("Players connected, sending champions.")
    send_champions(champions, conn1)
    send_champions(champions, conn2)

    while True:
        data = conn1.recv(1024)