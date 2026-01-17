import os
import math
import sys
from datetime import datetime
# Importujemy dekorator i kolory bezpośrednio z Twojego pliku cli.py
from cli import command, Color

# --- METADANE PLUGINU (Odczytywane przez Dispatcher._load_python_module) ---
__author__ = "Sebastian Januchowski"
__category__ = "math"
__group__ = "office"
__desc__ = "Profesjonalny kalkulator naukowy z logowaniem historii."

# Konfiguracja ścieżek (Zgodnie ze standardami Polsoft)
HIST_DIR = os.path.expandvars(r"%userprofile%\.polsoft\psCli\Calculator")
HIST_FILE = os.path.join(HIST_DIR, "history.txt")

def save_history(operation, result):
    """Zapisuje logi obliczeń w określonym katalogu historii."""
    if not os.path.exists(HIST_DIR):
        try:
            os.makedirs(HIST_DIR)
        except Exception:
            return # Ciche niepowodzenie, jeśli ścieżka jest niedostępna
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(HIST_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {operation} = {result}\n")
    except Exception as e:
        print(f"{Color.RED}[BŁĄD] Nie można zapisać historii: {e}{Color.RESET}")

def get_num(prompt_text):
    """Pomocnik do obsługi wejścia i konwersji przecinka na kropkę."""
    try:
        val = input(f"{Color.WHITE}{prompt_text}{Color.RESET}").replace(",", ".")
        return float(val)
    except ValueError:
        print(f"{Color.RED}Nieprawidłowa wartość liczbowa.{Color.RESET}")
        return None

def show_history_log():
    """Wyświetla ostatnie 15 wpisów z pliku historii."""
    print(f"\n{Color.CYAN}=== HISTORIA OBLICZEŃ ==={Color.RESET}")
    print(f"{Color.GRAY}Lokalizacja: {HIST_FILE}{Color.RESET}\n")
    if os.path.exists(HIST_FILE):
        with open(HIST_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines[-15:]:
                print(f" {Color.YELLOW}»{Color.RESET} {line.strip()}")
    else:
        print(f"{Color.GRAY}Brak zapisanych rekordów.{Color.RESET}")
    input(f"\n{Color.GRAY}Naciśnij Enter, aby wrócić...{Color.RESET}")

@command(name="kalkulator", aliases=["math", "calc", "kalk"])
def run_calculator(*args):
    """Interaktywny moduł profesjonalnego kalkulatora."""
    # args mogą być użyte później do bezpośrednich obliczeń CLI (np. 'calc 2 + 2')
    
    while True:
        # Czyszczenie ekranu (Windows/Linux)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Nagłówek
        print(f" {Color.GRAY}{datetime.now().year}(c) {__author__}{Color.RESET}")
        print(f"{Color.GREEN}==============================={Color.RESET}")
        print(f"      {Color.CYAN}{Color.BOLD}Kalkulator Pro v1.8{Color.RESET}")
        print(f"{Color.GREEN}==============================={Color.RESET}\n")
        
        # Menu
        print(f"[1] {Color.YELLOW}Dodawanie{Color.RESET}       [6] {Color.YELLOW}Pierwiastkowanie{Color.RESET}")
        print(f"[2] {Color.YELLOW}Odejmowanie{Color.RESET}     [7] {Color.YELLOW}Sinus{Color.RESET}")
        print(f"[3] {Color.YELLOW}Mnożenie{Color.RESET}        [8] {Color.YELLOW}Cosinus{Color.RESET}")
        print(f"[4] {Color.YELLOW}Dzielenie{Color.RESET}       [9] {Color.YELLOW}Tangens{Color.RESET}")
        print(f"[5] {Color.YELLOW}Potęgowanie{Color.RESET}")
        print(f"\n[h] {Color.CYAN}Historia{Color.RESET}    [?] {Color.CYAN}Pomoc{Color.RESET}    [e] {Color.RED}Wyjście do CLI{Color.RESET}\n")

        choice = input(f"{Color.BOLD}Wybór » {Color.RESET}").lower()

        if choice in ["e", "exit", "quit"]:
            break
        elif choice == "h":
            show_history_log()
            continue
        elif choice == "?":
            print(f"\n{Color.CYAN}Info:{Color.RESET} Standardowy moduł matematyczny podwójnej precyzji.")
            print(f"Funkcje trygonometryczne przyjmują wartości w stopniach.")
            input("\nNaciśnij Enter...")
            continue
            
        # Logika Matematyczna
        if choice in "12345":
            a = get_num("Podaj pierwszą liczbę: ")
            b = get_num("Podaj drugą liczbę: ")
            if a is not None and b is not None:
                if choice == '1': res, op = a + b, f"{a} + {b}"
                elif choice == '2': res, op = a - b, f"{a} - {b}"
                elif choice == '3': res, op = a * b, f"{a} * {b}"
                elif choice == '4':
                    if b == 0:
                        print(f"{Color.RED}Błąd: Dzielenie przez zero.{Color.RESET}")
                        input()
                        continue
                    res, op = a / b, f"{a} / {b}"
                elif choice == '5': res, op = math.pow(a, b), f"{a} ^ {b}"
                
                print(f"\n{Color.GREEN}{Color.BOLD}Wynik: {res}{Color.RESET}")
                save_history(op, res)
                input("\nNaciśnij Enter...")

        elif choice == '6':
            a = get_num("Podaj liczbę: ")
            if a is not None:
                if a < 0:
                    print(f"{Color.RED}Błąd: Nie można pierwiastkować liczby ujemnej.{Color.RESET}")
                else:
                    res = math.sqrt(a)
                    print(f"\n{Color.GREEN}{Color.BOLD}Wynik: {res}{Color.RESET}")
                    save_history(f"sqrt({a})", res)
                input("\nNaciśnij Enter...")

        elif choice in "789":
            deg = get_num("Podaj kąt (stopnie): ")
            if deg is not None:
                rad = math.radians(deg)
                if choice == '7': res, fn = math.sin(rad), "sin"
                elif choice == '8': res, fn = math.cos(rad), "cos"
                elif choice == '9': res, fn = math.tan(rad), "tan"
                
                print(f"\n{Color.GREEN}{Color.BOLD}{fn}({deg}) = {res}{Color.RESET}")
                save_history(f"{fn}({deg})", res)
                input("\nNaciśnij Enter...")