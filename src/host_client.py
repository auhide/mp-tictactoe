'''The server side for my Server-Client Tic-Tac-Toe Application.'''


import re
import os
import socket
import threading
import pickle
from tictactoe_constants import (BUFFER_SIZE, 
                                 IP, PORT, 
                                 GAME_DISPLAY,
                                 WINNING_COMBOS,
                                 SERVER_PATTERN)


class Host:
    '''
    This class acts like a server, it accepts
    one connection and then the game is on!
    '''
    
    server_socket = None

    def __init__(self, ip=None, port=None):
        
        if ip != None and port != None:
            self.ip = ip
            self.port = port
            self.foreign_username = None
            self.my_username = None
            self.conn = None
            self.game_display = GAME_DISPLAY
            self.all_choices = []
            self.my_choices = []

            self.server_start()
            print("The Game Has Ended!")
        else:
            print(f"{__class__.__name__} takes an IP and a PORT as arguments!")

    
    def socket_create(self):
        '''Creating a socket and binding it to given IP and PORT'''

        try:
            self.server_socket = socket.socket()
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)            
            self.server_socket.bind((self.ip, self.port))
            print(f"Server {self.ip}:{self.port} has been created")
            
            self.server_socket.listen(5)
        except socket.error:
            print("Error, while creating the socket!")
    

    def first_interaction(self, connection):
        '''
        Sending username to the other player.
        Receiving a username from the other player.
        '''

        print("Waiting for a player to join...")

        # Getting the username of the Client
        self.foreign_username = connection.recv(BUFFER_SIZE).decode()
        print(f"{self.foreign_username} has entered the game!")

        # Getting your username and sending it to the Client
        self.my_username = input("Enter your username: ")
        connection.send(self.my_username.encode())

    
    def enter_choice(self):
        '''
        Checks whether the entered choice is valid.
        Has to be a number.
        Has to be between 1 and 9.
        Doesn't have to be already entered as a choice.(not in self.all_choices)
        '''


        while True:
                try:
                    my_choice = int(input(f"{self.my_username}: ").strip())
                    if my_choice not in self.all_choices and (my_choice >= 1 and my_choice <= 9):
                        self.all_choices.append(my_choice)
                        break
                except:
                    print("You have to enter an integer(from 1 to 9)!")

        return my_choice

    
    def display(self, pos, player, display):
        '''
        Function that based on player's position displays
        the game board. 
        '''

        print("---------")
        for row in display:
            for i, val in enumerate(row):
                if val == pos:
                    row[i] = player
                print("|" + str(row[i]) + "|", end="")
            print("")
            print("---------")

        return display
    
    
    def win_check(self, name):
        '''
        Checks whether a combination of three choices of the player
        are equal to one of the winning combinations.
        '''

        for combo in WINNING_COMBOS:

            if all(choice in self.my_choices for choice in combo):
                print(f"CONGRATULATIONS {name}! YOU WON!")
                return True
                break


    def clear_board(self):
        '''
        Resets the list of all choices, the choices of the player,
        and the gameboard.
        '''

        
        self.all_choices = []
        self.my_choices = []

        self.game_display = [
                                ["1", "2", "3"],
                                ["4", "5", "6"],
                                ["7", "8", "9"]
                            ]


    def restart(self):
        '''
        Asks the player whether they want to play or not.
            -If they want to play, the clear_board() and play()
        functions are getting called and the game starts.
            -Else, the function returns False.
        '''

        while True:
            choice = input("\nDo you want to play again? [y/n]: ").strip()
            if choice.lower() == "y":
                self.clear_board()
                self.play(self.conn)
            elif choice.lower() == "n":
                return False


    def play(self, connection):
        '''Method that triggers the begining of the game for this .'''

        self.first_interaction(connection)

        # Displaying the starting Gameboard.
        curr_display = self.display(0, "", self.game_display)

        while True:
            
            # Getting the choice of the Guest.
            print(f"Waiting for {self.foreign_username}...")
            foreign_choice = connection.recv(BUFFER_SIZE).decode()
            
            # Checking if the Host lost, 
            # if not - appending the value to the list of choices.
            if foreign_choice != "You Lost :((":
                self.all_choices.append(int(foreign_choice))
            elif foreign_choice == "You Lost :((":
                print("You Lost :((")
                if not self.restart():
                    break

            # Displaying the Gameboard after the choice of the Guest.
            os.system("cls")            
            curr_display = self.display(foreign_choice, "X", curr_display)

            # print(f"{self.foreign_username}'s last choice: {foreign_choice}")

            # Getting the choice of the Host
            my_choice = self.enter_choice()
            self.my_choices.append(str(my_choice))

            # Display the Gameboard after choice of the Host.
            os.system("cls")
            curr_display = self.display(str(my_choice), "O", curr_display)

            # Check if the Host won and then ask him for a restart.
            if self.win_check(self.my_username):
                connection.send("You Lost :((".encode())

                if not self.restart():
                    break

            # Checking for a Draw and then asking for a restart.
            if len(self.all_choices) == 9:
                print("DRAW")

                if not self.restart():
                    break

            # Send the choice of the Host to the Guest.
            connection.send(str(my_choice).encode())


    def server_start(self):
        '''
        Using the created socket, this method accepts a connection,
        and then triggers the game to start. If the game ends, the while
        loop breaks and the server socket is closed.
        '''

        self.socket_create()
        
        while True:
            self.conn, addr = self.server_socket.accept()

            # print(f"Connected with {addr[0]}:{addr[1]}")
            if self.conn:
                self.play(self.conn)
                break

        self.server_socket.close()


def get_server_choice():
    '''
    A method that takes the IP and the PORT from the user.
    It has some restrictions like the IP:PORT pattern and
    the number port size.

    Returns a tuple of IP and PORT.
    '''

    while True:
        try:
            server = input("Create server--> ").strip().split(":")
            if int(server[1]) > 1024 and re.search(SERVER_PATTERN, ":".join(server)):
                break
            else:
                print("***The port has to be greater than 1024!***\n")
        except:
            print("***The format for the server input is: (IP:PORT)!***\n")

    ip = server[0]
    port = int(server[1])

    return ip, port

def welcome_ui():
    '''This is the initial text that appeаrs as the game starts.'''

    print("-------------------------------------------------------")
    print("| \t  Welcome to the Tic-Tac-Toe Client!          |")
    print("-------------------------------------------------------")
    print("\n----------------You are the Host-----------------------")
    print("|           As a Host, you have to be the one         |\n|          that has entered the server first!         |")
    print("-------------------------------------------------------")


if __name__ == "__main__":
    
    welcome_ui()
    ip, port = get_server_choice()

    Host(ip, port)