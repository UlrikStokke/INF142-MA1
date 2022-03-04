import socket
from champlistloader import load_some_champs
from core import Match
from core import Team
from core import Champion


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
champions = load_some_champs()



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("Server listening.")
    s.listen()
    conn1, addr1 = s.accept()
    #print("Waiting for player 2")
    #s.listen()
    #conn2, addr2 = s.accept()
    #while True:
    for i in champions:
        c = champions[i]
        tpl = c.str_tuple
        print(tpl)
        for n in tpl:
            print("String sent:" + n)
            conn1.sendall(n.encode())
            data = conn1.recv(1024)
    
    conn1.sendall("Finito".encode())
    
    while True:
        data = conn1.recv(1024)

 
        #data1 =conn1.recv(1024)
        #if not data1:
        #    break
        #print(data1)
        #for i in champions
        #conn1.sendall(data1)


    #message1 = "hei"
    #message2 = "hoi"
    #conn1.sendall(s.encode())
    #conn2.sendall(s.encode())


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


