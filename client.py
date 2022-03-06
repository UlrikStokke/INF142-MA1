import socket

import pickle

from rich import print
from rich.prompt import Prompt
from rich.table import Table

from champlistloader import load_some_champs
from core import Champion, Match, Shape, Team

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

def client_program():
    host = "127.0.0.1"  # as both code is running on same pc
    port = 65432  # socket server port number

    print("Connecting to server")
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    print("Connected to server: " + host + " " + str(port))

    print("\n"
          "Welcome to [bold yellow]Team Local Tactics[/bold yellow]!"
          "\n"
          "Each player choose a champion each time."
          "\n")
    

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
        data_list = [data_name, data_p1, data_p2, data_p3]
        tpl = tuple(data_list)
        available_champs.add_row(*tpl)

    print(available_champs)

    while True:
        champ_1 = client_socket.recv(1024).decode()
        choice_1 = input(f"{champ_1}")
        client_socket.send(choice_1.encode())
        answer = client_socket.recv(1024).decode()
        if answer == "ok":
            break
        else:
            print(answer)

    # Champ1 complete
    
    while True:
        champ_2 = client_socket.recv(1024).decode()
        choice_2 = input(f"{champ_2}")
        client_socket.send(choice_2.encode())
        answer = client_socket.recv(1024).decode()
        if answer == "ok":
            break
        else:
            print(answer)
    
    # Champ 2 complete

    match = pickle.loads(client_socket.recv(4098))

    print_match_summary(match)

    client_socket.close()  # close the connection

    print("Thank you for playing TNT")


if __name__ == '__main__':
    client_program()