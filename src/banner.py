from pystyle import Colors, Colorate
from pyfiglet import figlet_format
import os


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


text = "ASTROMODEL"


banner = figlet_format(text, font="slant") 

gradient_text = Colorate.Vertical(Colors.blue_to_cyan, banner)

def run():
    clear_console()


    print(gradient_text)