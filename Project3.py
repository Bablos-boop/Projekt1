import time                             # Koncept av tid
import os                               # Vi anvnänder denna för att kunna sudda bort.        
from random import randint              # Tillämpar slumpmässiga grejer
import funktioner as f                  # importerar funktioner från funktioner.py som f
from msvcrt import getwch               # låter oss använda getwch istället för input
from colors import bcolors              # färger

os.system('cls')
print("Welcome to...")                                          #Välkommen.
print(f""" {bcolors.YELLOW} 
____    ____  ____    ____  _____ _    _   ___  _______ 
|  _ \  |  _ \/ ___|  |  _ \| ____| |  | | | \ \/ / ____|
| |_) | | |_) \___ \  | | | |  _| | |  | | | |\  /|  _|  
|  _ < _|  __/ ___) | | |_| | |___| |__| |_| |/  \| |___ 
|_| \_(_)_| (_)____/  |____/|_____|_____\___//_/\_\_____|
      {bcolors.DEFAULT}""")

time.sleep(2) # Ger dig tid att kolla på titeln i 2 sekunder.

while True:                                                    # Loopen som gör så att spelet kan påbörjas och fortsätta tills mman vill sluta.
    
    os.system('cls')
    wins, losses, ties = f.get_stats()
    print(                                                  #Visar tidigare resultat från din sessioj
    f"{bcolors.GREEN}Wins: {wins}{bcolors.DEFAULT} | "                  
    f"{bcolors.RED}Losses: {losses}{bcolors.DEFAULT} | "
    f"{bcolors.YELLOW}Ties: {ties}{bcolors.DEFAULT}\n"
)

    player = f.your_hand()      # Definition av player och computer som får kod från funktioner.py
    computer = f.computer_hand()


    print(f"Computer chose: {computer}")         #Skriver ut vad datorn valde för något.   

    result = f.determine_winner(player, computer)       #Skriver ut resultat beroende på vad man väljer.
    print(result)   

    print("Play again or quit(q)?")       # Frågar om du vill fortsätta spela eller sluta
    your_input = getwch().upper()
    if your_input == 'Q':
        os.system('cls')
        print("SEE YA!")
        break
        