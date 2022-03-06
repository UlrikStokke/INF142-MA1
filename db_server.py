from operator import truediv
import socket
import pickle
from champlistloader import load_some_champs
from core import Match
from core import Team
from core import Champion
from core import Shape
from rich import print
from rich.prompt import Prompt
from rich.table import Table

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
DBPORT = 65433  # Port to listen on (non-privileged ports are > 1023)

# Load the champions from file
champions = load_some_champs()
print("Champions loaded from file.")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Wait for the game server to connect
    s.bind((HOST, DBPORT))
    print("DB server listening for game server.")
    s.listen()
    conn, addr = s.accept()

    # Send the champions to the game server
    conn.sendall(pickle.dumps(champions))
    print("Champions sent to game server.")

    print("DB server waiting for game results.")

    match = pickle.loads(conn.recv(4098))

    print_match_summary(match)

    with open("match_history.txt", "a+") as f:
        f.seek(0)
        data = f.read(100)
        if len(data) > 0 :
            f.write("\n")
        red_score, blue_score = match.score
        f.write(f"{red_score},{blue_score}")

    conn.close()
    print("The database server is shut down.")

    #while True:
        #TODO
        # Add code for receiving match statistics and store it to file
        #data = conn.recv(1024)