import socket
from champlistloader import load_some_champs
from core import Match
from core import Team


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
champions = load_some_champs()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn1, addr1 = s.accept()
    print("Waiting for player 2")
    s.listen()
    conn2, addr2 = s.accept()
    message1 = "hei"
    message2 = "hoi"
    conn1.sendall(champions.encode())
    conn2.sendall(champions.encode())










    #with conn1:
    #    while True:
    #        data1 =conn1.recv(1024)
    #        if not data1:
    #            break
    #        print(data1)
    #        conn1.sendall(data1)




#champions = load_some_champs()
#player1 = []
#player2 = [] 
#print_available_champs(champions)
#print('\n')

#Valg av spillere, en om gangen

#match = Match(
#        Team([champions[name] for name in player1]),
#        Team([champions[name] for name in player2])
#    )
#    match.play()
#send match summary til clients


