import pickle
from operator import truediv
import socket
from champlistloader import load_some_champs
from core import Match
from core import Team
from core import Champion
from core import Shape
from rich import print
from rich.prompt import Prompt
from rich.table import Table

def send_champions(champions, conn):
    for i in champions:
        c = champions[i]
        tpl = c.str_tuple
        print("Read tuple: ")
        print(tpl)
        for n in tpl:
            print("Sending string: " + n)
            conn.sendall(n.encode())
            data = conn.recv(1024).decode() # receive "ok"
#            print(data)
    print("Sending complete: ")
    conn.sendall("complete".encode())

def input_champions(conn, valid_champs, players_champs, opponents_champs):
    while True:
        conn.sendall("Choose champion: ".encode())
        chosen_champ = conn.recv(1024).decode()
#        print(chosen_champ)
        if chosen_champ not in valid_champs:
            conn.sendall((f'The champion {chosen_champ} is not available. Try again.'+"\n").encode())
        elif chosen_champ in players_champs:
            conn.sendall((f'{chosen_champ} is already in your team. Try again.'+"\n").encode())
        elif chosen_champ in opponents_champs:
            conn.sendall((f'{chosen_champ} is in the enemy team. Try again.'+"\n").encode())
        else:
            print("Player chose: " + str(chosen_champ))
            break
    conn.sendall(("ok").encode())
    return str(chosen_champ)


def print_match_summary(match: Match) -> None:

    EMOJI = {
        Shape.ROCK: ':raised_fist-emoji:',
        Shape.PAPER: ':raised_hand-emoji:',
        Shape.SCISSORS: ':victory_hand-emoji:'
    }

    # For each round print a table with the results
    for index, round in enumerate(match.rounds):

        # Create a table containing the results of the round
        round_summary = Table(title=f'Round {index+1}')

        # Add columns for each team
        round_summary.add_column("Red",
                                 style="red",
                                 no_wrap=True)
        round_summary.add_column("Blue",
                                 style="blue",
                                 no_wrap=True)

        # Populate the table
        for key in round:
            red, blue = key.split(', ')
            round_summary.add_row(f'{red} {EMOJI[round[key].red]}',
                                  f'{blue} {EMOJI[round[key].blue]}')
        print(round_summary)
        print('\n')

    # Print the score
    red_score, blue_score = match.score
    print(f'Red: {red_score}\n'
          f'Blue: {blue_score}')

    # Print the winner
    if red_score > blue_score:
        print('\n[red]Red victory! :grin:')
    elif red_score < blue_score:
        print('\n[blue]Blue victory! :grin:')
    else:
        print('\nDraw :expressionless:')

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
dbhost = "127.0.0.1"  # Standard loopback interface address (localhost)
dbport = 65433  # database socket server port number

# Connect to database server
print("Connecting to DB server")
client_socket = socket.socket()  # instantiate
client_socket.connect((dbhost, dbport))  # connect to the server
print("Connected to DB server: " + dbhost + " " + str(dbport))


# Load champions using ´pickle´
champions = pickle.loads(client_socket.recv(4098))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print("Server listening for player 1.")
    s.listen()
    conn1, addr1 = s.accept()
    send_champions(champions, conn1)
    print("Server listening for player 2.")
    s.listen()
    conn2, addr2 = s.accept()
    send_champions(champions, conn2)

#    print("Players connected, sending champions.")

    player_1_champs = []
    player_2_champs = []
    valid_champs = list(champions.keys())

#   TODO Send and print opponents choices of champions
    p1_c1 = input_champions(conn1, valid_champs, player_1_champs, player_2_champs)
    player_1_champs.append(p1_c1)

    p2_c1 = input_champions(conn2, valid_champs, player_2_champs, player_1_champs)
    player_2_champs.append(p2_c1)

    p1_c2 = input_champions(conn1, valid_champs, player_1_champs, player_2_champs)
    player_1_champs.append(p1_c2)

    p2_c2 = input_champions(conn2, valid_champs, player_2_champs, player_1_champs)
    player_2_champs.append(p2_c2)

    match = Match(
        Team([champions[name] for name in player_1_champs]),
        Team([champions[name] for name in player_2_champs])
    )
    match.play()

    # Print a summary
    print_match_summary(match)

    conn1.sendall(pickle.dumps(match))
    conn2.sendall(pickle.dumps(match))
    client_socket.sendall(pickle.dumps(match))

    conn1.close()
    conn2.close()
    client_socket.close()

    print("The server is shut down!")