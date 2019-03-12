'''All constants for the Server-Client Tic-Tac-Toe'''


BUFFER_SIZE = 1024
IP = "127.0.0.1"
PORT = 2222

ALL_CHOICES = []
MY_CHOICES = []

GAME_DISPLAY =  [
                    ["1", "2", "3"],
                    ["4", "5", "6"],
                    ["7", "8", "9"]
                ]

WINNING_COMBOS  =  [   
                        ["1", "4", "7"],
                        ["2", "5", "8"],
                        ["3", "6", "9"],
                        ["1", "2", "3"],
                        ["4", "5", "6"],    
                        ["7", "8", "9"],
                        ["1", "5", "9"],
                        ["3", "5", "7"]
                    ]

SERVER_PATTERN = r"[0-9]+(?:\.[0-9]+){3}:[0-9]+"