import os

def cleaning_screan():
    if os.name == 'nt': #windows
        os.system('cls')
    else:
        os.system('clear')