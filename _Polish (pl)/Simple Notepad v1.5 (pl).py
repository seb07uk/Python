import os
import datetime
import sys
import msvcrt  # Biblioteka do obsługi klawiszy na Windows (bez Entera)

# Importowanie klasy Color i dekoratora z głównego pliku cli.py
try:
    from cli import Color, command
except ImportError:
    class Color:
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        GRAY = '\033[90m'
        RESET = '\033[0m'
    def command(name=None, aliases=None):
        def decorator(func):
            func.is_command = True
            func.command_name = name if name else func.__name__
            func.aliases = aliases if aliases else []
            return func
        return decorator

# --- METADANE (Wczytywane przez cli.py) ---
__author__ = "Sebastian Januchowski"
__category__ = "narzedzia"
__group__ = "python"
__desc__ = "Prosty Notatnik PRO z funkcją AutoSave i szybką nawigacją"

# Ścieżka przechowywania notatek
TARGET_DIR = os.path.expandvars(r"%USERPROFILE%\.polsoft\psCLI\Notepad")

def zapewnij_katalog():
    """Tworzy folder notatek, jeśli nie istnieje."""
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

def pobierz_notatki():
    """Pobiera listę plików .txt, sortując od najnowszych."""
    if not os.path.exists(TARGET_DIR):
        return []
    pliki = [f for f in os.listdir(TARGET_DIR) if f.endswith(".txt")]
    pliki.sort(key=lambda x: os.path.getmtime(os.path.join(TARGET_DIR, x)), reverse=True)
    return pliki

@command(name="notepad", aliases=["notatnik", "n"])
def notepad_main(*args):
    """Główna pętla interaktywnego notatnika."""
    zapewnij_katalog()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Color.BLUE}================================{Color.RESET}")
        print(f"      Simple Notepad v1.5")
        print(f"{Color.BLUE}================================{Color.RESET}")
        print(f"[1] {Color.GREEN}Nowa notatka (Auto-Save){Color.RESET}")
        print(f"[2] {Color.BLUE}Przeglądaj (W/S/O/D){Color.RESET}")
        print(f"[H] {Color.YELLOW}Pomoc / Instrukcja{Color.RESET}")
        print(f"[A] {Color.YELLOW}O autorze{Color.RESET}")
        print(f"[X] {Color.RED}Wyjście{Color.RESET}")
        print(f"{Color.BLUE}================================{Color.RESET}")
        
        # Przechwytywanie klawisza w menu głównym
        wybor = msvcrt.getch().decode('utf-8').lower()

        if wybor == '1':
            nowa_notatka()
        elif wybor == '2':
            przegladaj_notatki()
        elif wybor == 'h':
            wyswietl_pomoc()
        elif wybor == 'a':
            wyswietl_o_autorze()
        elif wybor in ['x', 'q']:
            break

def nowa_notatka():
    os.system('cls')
    print(f"{Color.GREEN}Wpisz treść notatki.{Color.RESET}")
    print(f"{Color.YELLOW}(Naciśnij CTRL+Z, a następnie ENTER, aby zapisać){Color.RESET}")
    print("-" * 32)
    
    try:
        tresc = sys.stdin.read()
        if not tresc.strip():
            print(f"\n{Color.RED}[!] Anulowano lub notatka jest pusta.{Color.RESET}")
            os.system("timeout /t 2 >nul")
            return

        ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nazwa_pliku = f"Notatka_{ts}.txt"
        sciezka = os.path.join(TARGET_DIR, nazwa_pliku)
        
        with open(sciezka, "w", encoding="utf-8") as f:
            f.write(tresc)
            
        print(f"\n{Color.GREEN}[OK] Zapisano automatycznie jako: {nazwa_pliku}{Color.RESET}")
        os.system("timeout /t 2 >nul")
    except EOFError:
        pass

def przegladaj_notatki():
    wybrany = 0
    while True:
        notatki = pobierz_notatki()
        if not notatki:
            os.system('cls')
            print(f"{Color.RED}[!] Nie znaleziono żadnych notatek.{Color.RESET}")
            os.system("pause")
            return

        os.system('cls')
        print(f"{Color.BLUE}--- LISTA (W/S - Nawigacja, O - Otwórz, D - Usuń, Q - Powrót) ---{Color.RESET}\n")
        
        for i, plik in enumerate(notatki):
            if i == wybrany:
                print(f" {Color.GREEN}> {plik} {Color.RESET}")
            else:
                print(f"   {plik}")
        
        print(f"\n{Color.GRAY}Notatek: {len(notatki)} | W=Góra, S=Dół, O=Otwórz, D=Usuń, Q=Wstecz{Color.RESET}")
        
        klawisz = msvcrt.getch().decode('utf-8').lower()

        if klawisz == 'q': 
            break
        elif klawisz == 'w' and wybrany > 0: 
            wybrany -= 1
        elif klawisz == 's' and wybrany < len(notatki) - 1: 
            wybrany += 1
        elif klawisz == 'o' or klawisz == '\r': # \r to klawisz Enter
            otworz_notatke(notatki[wybrany])
        elif klawisz == 'd': 
            usun_notatke(notatki[wybrany])

def otworz_notatke(nazwa_pliku):
    os.system('cls')
    sciezka = os.path.join(TARGET_DIR, nazwa_pliku)
    print(f"{Color.YELLOW}Plik: {nazwa_pliku}{Color.RESET}")
    print(f"{Color.BLUE}{'-'*40}{Color.RESET}")
    try:
        with open(sciezka, 'r', encoding='utf-8') as f:
            print(f.read())
    except Exception as e:
        print(f"{Color.RED}Błąd odczytu: {e}{Color.RESET}")
    print(f"{Color.BLUE}{'-'*40}{Color.RESET}")
    print("Naciśnij dowolny klawisz, aby wrócić do listy...")
    msvcrt.getch()

def usun_notatke(nazwa_pliku):
    print(f"\n{Color.RED}[?] Czy na pewno usunąć: {nazwa_pliku}? (T/N){Color.RESET}")
    potwierdzenie = msvcrt.getch().decode('utf-8').lower()
    if potwierdzenie == 't' or potwierdzenie == 'y':
        try:
            os.remove(os.path.join(TARGET_DIR, nazwa_pliku))
            print(f"{Color.GREEN}[OK] Plik usunięty.{Color.RESET}")
            os.system("timeout /t 1 >nul")
        except:
            pass

def wyswietl_pomoc():
    os.system('cls')
    print(f"{Color.BLUE}==================================={Color.RESET}")
    print(f"            POMOC NOTATNIKA")
    print(f"{Color.BLUE}==================================={Color.RESET}\n")
    print(f"{Color.GREEN}1. Tworzenie:{Color.RESET} Wybierz [1], wpisz tekst. Zakończ {Color.YELLOW}CTRL+Z + Enter{Color.RESET}")
    print(f"{Color.GREEN}2. Przeglądanie:{Color.RESET} Użyj {Color.YELLOW}W/S{Color.RESET} do ruchu, {Color.YELLOW}O{Color.RESET} aby otworzyć.")
    print(f"{Color.GREEN}3. Lokalizacja:{Color.RESET} {TARGET_DIR}\n")
    print("Naciśnij dowolny klawisz, aby wrócić...")
    msvcrt.getch()

def wyswietl_o_autorze():
    os.system('cls')
    print(f"{Color.BLUE}==================================={Color.RESET}")
    print(f"            O AUTORZE")
    print(f"{Color.BLUE}==================================={Color.RESET}\n")
    print(f"{Color.GREEN}Autor:{Color.RESET}  Sebastian Januchowski")
    print(f"{Color.GREEN}Email:{Color.RESET}  polsoft.its@fastservice.com")
    print(f"{Color.GREEN}GitHub:{Color.RESET} https://github.com/seb07uk\n")
    print(f"{Color.BLUE}==================================={Color.RESET}")
    print("\nNaciśnij dowolny klawisz, aby wrócić...")
    msvcrt.getch()

if __name__ == "__main__":
    notepad_main()