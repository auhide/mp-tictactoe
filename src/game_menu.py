'''A menu that gives you a choice, whether you want to create a game or join one.'''

import os
from host_client import (Host,
                         welcome_ui,
                         get_server_choice)
from guest_client import (Guest,
                          welcome_ui,
                          get_server_choice)



def run_host_client():

    welcome_ui()
    ip, port = get_server_choice()

    Host(ip, port)


def run_guest_client():

    welcome_ui()
    ip, port = get_server_choice()

    Guest(ip, port)



def get_client_choice():
    '''
    Returns 
    1 if the user chooses to Create a Game
    2 if the user choose to Join a Game
    '''

    client_type = 0

    while client_type != 1 and client_type != 2:
        try:
            print("-------------------------------------------------")
            client_type = int(input("Enter...\n(1)To Create a Game\t\t(2)To Join a Game\n"))
            print("-------------------------------------------------")
        except:
            pass
    
    return client_type



if __name__ == "__main__":

    client_type = get_client_choice()

    os.system("cls")

    if client_type == 1:
        run_host_client()
    else:
        run_guest_client()