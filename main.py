import csv
import os
import locale
from time import sleep
from colors import bcolors  

games = []

def Save_data(games, filepath):
    # Sparar alla spel till CSV-fil
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['id', 'name', 'genre', 'rating', 'price', 'short_review', 'long_review']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(games)
    except Exception as error_code:
        print("Fel vid sparning:", error_code)
    return "OK"

def format_currency(value):
    # Formaterar pris med lokalisering (svenska kronor)
    return locale.currency(value, grouping=True)

locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')  

def truncate_string(word, length=65):
    # Kortar en sträng och lägger till "..."
    if len(word) > length:
        return word[:length] + "..."    
    else:
        return word

def list_games(games):
    # Skriver ut en tabell med alla spel
    print(f"{bcolors.CYAN}=== Nintendo Games ==={bcolors.DEFAULT}")
    header = f"{bcolors.YELLOW}{'#':<4} {'NAMN':<30} {'GENRE':<26} {'RATING':<8} {'PRIS':<12} {'BESKRIVNING':<30}{bcolors.DEFAULT}" # Exakta mellanrum mellan alla keys.
    separator = "-" * 155 # Rad för att separera header från raderna
    rows = [] #lista
    
    for index, game in enumerate(games, 1): # Tabelllayout
        name = game['name']
        genre = game['genre']
        rating = game['rating']
        price = game['price']
        short_review = truncate_string(game['short_review'])
        
        # Formatera pris med svenska kronor
        try:
            price_str = locale.currency(float(price), grouping=True)
        except:
            price_str = str(price)
        
        row = f"{index:<4} {name:<30} {genre:<26} {rating:<8} {price_str:<12} {short_review:<30}" # Mellanrum mellan alla values.
        rows.append(row)
    
    inventory_table = "\n".join([header, separator] + rows)
    print(inventory_table)
    return inventory_table

def load_data(filename):
    # Läser spel från CSV-fil till listan
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                games.append({
                    "id": int(row['id']),
                    "name": row['name'],
                    "genre": row['genre'],
                    "price": float(row['price']),
                    "rating": row['rating'],
                    "short_review": row['short_review'],
                    "long_review": row['long_review'],
                })
    except FileNotFoundError:
        print("Databasfil inte funnen!")
    except Exception as e:
        print(f"Fel vid läsning: {e}")

def show_statistics(games):
    os.system('cls')
    
    if not games:
        print("Inga spel i databasen för att visa statistik.")
        input("Tryck Enter för att fortsätta...")
        return
    # Beräkna statistik
    total_games = len(games)
    total_price = sum(game['price'] for game in games)
    average_price = total_price / total_games
    
    # Hitta dyraste och högst betygsatta spelet
    most_expensive = max(games, key=lambda x: x['price'])
    cheapest = min(games, key=lambda x: x['price'])
    highest_rated = max(games, key=lambda x: float(x['rating']) if x['rating'].replace('.','',1).isdigit() else 0)

    print(f"{bcolors.CYAN}=== STATISTIK ==={bcolors.DEFAULT}\n")
    print(f"Totalt antal spel: {total_games}")
    print(f"Genomsnittligt pris: {format_currency(average_price)}")
    print(f"Dyraste spelet: {most_expensive['name']} - {format_currency(most_expensive['price'])}")
    print(f"Billigaste: {cheapest['name']} ({format_currency(cheapest['price'])})")
    print(f"Högst betygsatta spelet: {highest_rated['name']} - Betyg: {highest_rated['rating']}")
    input("\nTryck Enter för att fortsätta...")
def show_detailed_review(game_id, games):
    # Visar lång recension för ett specifikt spel
    os.system('cls')
    list_games(games)
    print("-" * 155) 
    for game in games:
        if game["id"] == game_id:
            print(f"{bcolors.CYAN}=== {game['name']} ==={bcolors.DEFAULT}\n") # Titel med färg för extra tydlighet
            print(f"Genre: {game['genre']}")
            print(f"Rating: {game['rating']}")
            print(f"Pris: {game['price']} kr")
            print(f"\n{bcolors.YELLOW}Recension:{bcolors.DEFAULT}")
            print(game['long_review'])
            input("\nTryck Enter för att fortsätta...")
            return
    print("Inget spel med det ID:t hittades.")
    input("\nTryck Enter för att fortsätta...")

def remove_game(games):
    # Tar bort ett spel från listan
    while True:
        os.system('cls')
        list_games(games)
        print("-" * 155)   
        try:
            game_id = int(input(f"{bcolors.RED}Ange spel ID för att ta bort: {bcolors.DEFAULT}"))
        except ValueError:
            os.system('cls')
            print("Ogiltigt ID. Försök igen.")
            continue
        
        found = False
        for game in games:
            if game["id"] == game_id:
                games.remove(game)
                print("Tar bort spel...")
                Save_data(games, 'db_games.csv')
                sleep(1)
                found = True
                break
        
        if found:
            return
        else:
            print("Inget spel med det ID:t hittades.")
            sleep(1)

def edit_game(games):
    # Redigera ett befintligt spel
    while True:
        os.system('cls')
        list_games(games)
        print("-" * 155)   
        try:
            game_id = int(input("Ange spel ID för att redigera: ")) # Felhantering för ogiltig inmatning
        except ValueError:
            os.system('cls')
            print("Ogiltigt ID. Försök igen.")
            sleep(1)
            continue
        
        found = False # Söker efter spelet att redigera
        for game in games:
            if game["id"] == game_id:
                found = True
                os.system('cls')
                print(f"Redigera {bcolors.CYAN}{game['name']}{bcolors.DEFAULT}:")
                game['name'] = input(f"Namn ({game['name']}): ") or game['name'] # Ändra namn
                game['genre'] = input(f"Genre ({game['genre']}): ") or game['genre'] # Ändra genre
                
                try:
                    rating_input = input(f"Rating ({game['rating']}): ") # Ändra rating med felhantering
                    if rating_input:
                        game['rating'] = float(rating_input)
                except ValueError:
                    print("Ogiltig rating. Behåller tidigare värde.")
                
                try: #Ändra pris med felhantering
                    price_input = input(f"Pris ({game['price']}): ")
                    if price_input:
                        game['price'] = int(price_input)
                except ValueError:
                    print("Ogiltigt pris. Behåller tidigare värde.")
                
                game['short_review'] = truncate_string(input(f"Kort recension ({game['short_review']}): ") or game['short_review']) # Ändra kort recension med truncate så att den vet vad den ska göra.
                game['long_review'] = input(f"Lång recension ({game['long_review']}): ") or game['long_review']
                Save_data(games, 'db_games.csv')
                print("Sparar ändringar...")
                sleep(1)
                break
        
        if found: # Avsluta om spelet hittades och redigerades
            return
        else:
            print("Inget spel med det ID:t hittades.")
            sleep(1)

def add_game(games):
    # Lägg till ett nytt spel
    os.system('cls')    
    print(f"{bcolors.YELLOW}Vilket spel vill du lägga till?{bcolors.DEFAULT}")
    name = input("Namn: ")
    genre = input("Genre: ") 
    
    # Validera rating
    while True:      
        rating = input("Rating (0.0 - 10.0): (T.ex 7.5): ")
        try:
            rating = float(rating)
            if 0.0 <= rating <= 10.0:
                break
            else:
                print("Rating måste vara mellan 0.0 och 10.0.")
        except ValueError:
            print("Ogiltig rating. Ange ett nummer.")
    
    # Validera pris
    while True:      
        price = input("Pris (Exempel: 599): ")
        try:
            price = int(price)
            if 0 <= price <= 10000:
                break
            else:
                print("Pris måste vara mellan 0 och 10000.")
        except ValueError:
            print("Ogiltigt pris. Ange ett heltal.")
    
    short_review = truncate_string(input("Kort recension: "))
    long_review = input("Längre recension: ")
    
    # Beräkna ID som max(id) + 1, inte len(games) + 1
    new_id = max((g.get('id', 0) for g in games), default=0) + 1
    
    games.append({
        "id": new_id,
        "name": name,
        "genre": genre,
        "rating": rating,
        "short_review": short_review,
        "long_review": long_review,
        "price": price
    })
    Save_data(games, 'db_games.csv')
    print(f"{bcolors.YELLOW}Sparar produkt...{bcolors.DEFAULT}")
    sleep(1)
    os.system('cls')    

# Ladda databas vid start
load_data('db_games.csv')

menu_options = [
    "View detailed review",
    "Remove game",
    "Add game",
    "Edit game",
    "Statistics",
    "Finish"
]

# Huvudloop  meny
while True:
    os.system('cls')
    list_games(games)
    print("-" * 155)   
    print(f"{bcolors.YELLOW}MENY:{bcolors.DEFAULT}")
    
    for index, choice in enumerate(menu_options, start=1):
        print(f"{index}. {choice}") 
    
    try:  
        input_choice = int(input(f"\n{bcolors.YELLOW}Välj ett alternativ (1-5): {bcolors.DEFAULT}")) # Inmätning för menyval och felhantering vid ogiltig inmatning
    except ValueError:
       
        continue
    
    if input_choice == 1:
        # Visa lång recension
        os.system('cls')
        try: 
            idx = int(input(f"\n{bcolors.YELLOW}Ange spel ID för att se lång recension: {bcolors.DEFAULT} ")) # Inmätning för id och felhantering vid ogiltig inmatning
            show_detailed_review(idx, games)
        except ValueError:
            print("Ogiltigt ID.")
           
    elif input_choice == 2: # Ta bort spel funktion 
        remove_game(games)
    elif input_choice == 3: # Lägg till spel funktion
        add_game(games)   
    elif input_choice == 4: # Redigera spel funktion
        edit_game(games)
    elif input_choice == 5: # Visa statistics funktion
        show_statistics(games)
    elif input_choice == 6: # Avsluta programmet
        print("Avslutar programmet...")
        sleep(0.5)
        break
    else:
        print("Ogiltigt alternativ (1-5).")
     


