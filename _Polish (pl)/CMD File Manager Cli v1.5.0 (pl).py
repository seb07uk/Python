__author__ = "Sebastian Januchowski"
__category__ = "file manager"
__group__ = "system"
__desc__ = "Menedżer plików CMD Cli: Pełny pakiet z historią i szybkimi linkami"

import os
import shutil
import platform
import subprocess
from datetime import datetime
from pathlib import Path

# --- KONFIGURACJA KOLORÓW I FORMATOWANIA ---
G = "\033[92m"      # Zielony (Sukces)
R = "\033[91m"      # Czerwony (Błąd)
Y = "\033[93m"      # Żółty (Ostrzeżenie/Info)
B = "\033[94m"      # Niebieski (Ramki)
BOLD = "\033[1m"    # Pogrubienie
RESET = "\033[0m"   # Reset formatowania

class FileManager:
    def __init__(self):
        self.msg = ""
        self.save_path = Path.home() / ".polsoft" / "psCLI" / "FileList"
        self.save_path.mkdir(parents=True, exist_ok=True)
        
        if platform.system() == "Windows":
            os.system("title CMD File Manager Cli")
            os.system("mode con: cols=105 lines=50")

    def clear_screen(self):
        os.system('cls' if platform.system() == 'Windows' else 'clear')

    def get_dir_content(self):
        try:
            items = sorted(os.listdir('.'))
            dirs = [d for d in items if os.path.isdir(d)]
            files = [f for f in items if os.path.isfile(f)]
            return dirs, files
        except Exception:
            return [], []

    def draw_menu(self):
        self.clear_screen()
        curr_dir = os.getcwd()
        dirs, files = self.get_dir_content()

        print(f"\n {Y}ZAWARTOŚĆ KATALOGU:{RESET}  {B}[{curr_dir}]{RESET}")
        print(f"{B} ┌" + "─" * 94 + f"┐{RESET}")
        
        for d in dirs:
            display_name = (d[:85] + '...') if len(d) > 85 else d
            padding = 94 - (2 + 5 + 2 + len(display_name))
            print(f"{B} │{RESET}  {G}[DIR]{RESET}  {display_name}" + " " * padding + f"{B}│{RESET}")
        
        if dirs and files:
            print(f"{B} ├" + "─" * 94 + f"┤{RESET}")
        
        for f in files:
            display_name = (f[:85] + '...') if len(f) > 85 else f
            padding = 94 - (10 + len(display_name))
            print(f"{B} │{RESET}          {display_name}" + " " * padding + f"{B}│{RESET}")
            
        print(f"{B} └" + "─" * 94 + f"┘{RESET}")

        header_text = "CMD File Manager Cli"
        margin = (95 - len(header_text)) // 2
        header_line = " " * margin + header_text + " " * (95 - margin - len(header_text))

        print(f"\n{B}╔═══════════════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{B}║{header_line}║{RESET}")
        print(f"{B}╠═══════════════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{B}║{RESET}  [1]  ODŚWIEŻ          [2]  WEJDŹ (CD)       [3]  W GÓRĘ (..)      [4]  INFO O DYSKU          {B}║{RESET}")
        print(f"{B}║{RESET}  [5]  NOWY PLIK        [6]  NOWY FOLDER      [7]  USUŃ PLIK        [8]  USUŃ FOLDER           {B}║{RESET}")
        print(f"{B}║{RESET}  [9]  ZMIEŃ NAZWĘ      [10] KOPIUJ (SHUTIL)  [11] PRZENIEŚ         [12] ZAPISZ LISTĘ          {B}║{RESET}")
        print(f"{B}║{RESET}  [13] BACKUP (LUSTRO)  [14] SZUKAJ           [15] OTWÓRZ ZAPISY    [16] POMOC                 {B}║{RESET}")
        print(f"{B}║{RESET}  [17] O PROGRAMIE      [18] WYJŚCIE                                                           {B}║{RESET}")
        print(f"{B}╚═══════════════════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")
        
        if self.msg:
            print(self.msg)
            self.msg = ""

    def run(self):
        while True:
            self.draw_menu()
            choice = input(f"{B} CMD CLI > {RESET}Wybierz opcję: ").strip()
            if choice == "1": continue
            elif choice == "2": self.enter_dir()
            elif choice == "3": os.chdir("..")
            elif choice == "4": self.disk_info()
            elif choice == "5": self.make_file()
            elif choice == "6": self.make_dir()
            elif choice == "7": self.delete_file()
            elif choice == "8": self.delete_folder()
            elif choice == "9": self.rename_item()
            elif choice == "10": self.copy_item()
            elif choice == "11": self.move_item()
            elif choice == "12": self.save_list()
            elif choice == "13": self.backup()
            elif choice == "14": self.search()
            elif choice == "15": self.open_saves()
            elif choice == "16": self.show_help()
            elif choice == "17": self.show_about()
            elif choice == "18": break
            else: self.msg = f"{R} [!] Nieprawidłowy wybór!{RESET}"

    # ... (pozostałe funkcje logiczne pozostają bez zmian) ...
    def enter_dir(self):
        folder = input(" [?] Folder: ")
        try: os.chdir(folder)
        except Exception as e: self.msg = f"{R} [!] BŁĄD: {e}{RESET}"

    def disk_info(self):
        self.clear_screen()
        print(f"\n{B}  ═══ STATYSTYKI WOLUMENU I KATALOGU ═══{RESET}\n")
        try:
            usage = shutil.disk_usage(os.getcwd())
            print(f" {Y} [ UŻYCIE DYSKU ]{RESET}")
            print(f" Całkowite:  {usage.total // (2**30)} GB")
            print(f" Zajęte:     {usage.used // (2**30)} GB")
            print(f" Wolne:      {usage.free // (2**30)} GB")
            input(f"\n{G}Naciśnij [ENTER], aby wrócić...{RESET}")
        except Exception as e: print(f"{R} [!] BŁĄD: {e}{RESET}")

    def make_file(self):
        name = input(" [+] Nazwa nowego pliku: ")
        try: Path(name).touch(); self.msg = f"{G} [+] Utworzono pomyślnie.{RESET}"
        except Exception as e: self.msg = f"{R} [!] BŁĄD: {e}{RESET}"

    def make_dir(self):
        name = input(" [+] Nazwa nowego folderu: ")
        try: os.makedirs(name, exist_ok=True); self.msg = f"{G} [+] Folder utworzony.{RESET}"
        except Exception as e: self.msg = f"{R} [!] BŁĄD: {e}{RESET}"

    def delete_file(self):
        name = input(" [!] Plik do usunięcia: ")
        try: os.remove(name); self.msg = f"{G} [+] Usunięto.{RESET}"
        except Exception as e: self.msg = f"{R} [!] BŁĄD: {e}{RESET}"

    def delete_folder(self):
        name = input(" [!] Folder do usunięcia: ")
        try: shutil.rmtree(name); self.msg = f"{G} [+] Katalog usunięty.{RESET}"
        except Exception as e: self.msg = f"{R} [!] BŁĄD: {e}{RESET}"

    def rename_item(self):
        old = input(" [!] Obecna nazwa: ")
        new = input(" [!] Nowa nazwa: ")
        try: os.rename(old, new); self.msg = f"{G} [+] Zmieniono nazwę.{RESET}"
        except Exception as e: self.msg = f"{R} [!] BŁĄD: {e}{RESET}"

    def copy_item(self):
        src, dst = input(" [?] Źródło: "), input(" [?] Cel: ")
        try:
            if os.path.isdir(src): shutil.copytree(src, dst, dirs_exist_ok=True)
            else: shutil.copy2(src, dst)
            self.msg = f"{G} [+] Skopiowano.{RESET}"
        except Exception as e: self.msg = f"{R} [!] BŁĄD: {e}{RESET}"

    def move_item(self):
        src, dst = input(" [?] Źródło: "), input(" [?] Cel: ")
        try: shutil.move(src, dst); self.msg = f"{G} [+] Przeniesiono.{RESET}"
        except Exception as e: self.msg = f"{R} [!] BŁĄD: {e}{RESET}"

    def save_list(self):
        folder_name = os.path.basename(os.getcwd()) or "DYSK"
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = self.save_path / f"{folder_name}_{timestamp}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"RAPORT - {datetime.now()}\n\n")
                for item in os.listdir('.'): f.write(f"{item}\n")
            self.msg = f"{G} [+] Lista zapisana.{RESET}"
        except Exception as e: self.msg = f"{R} [!] BŁĄD: {e}{RESET}"

    def search(self):
        query = input(" [?] Fraza: ")
        print(f"\n {Y}WYNIKI:{RESET}")
        print(f"{B} ┌" + "─" * 94 + f"┐{RESET}")
        for path in Path('.').rglob(f"*{query}*"):
            line = str(path)[:90]
            print(f"{B} │{RESET}  {line:<91}{B}│{RESET}")
        print(f"{B} └" + "─" * 94 + f"┘{RESET}")
        input(f"\n{G}Powrót [ENTER]...{RESET}")

    def open_saves(self):
        try:
            if platform.system() == "Windows": os.startfile(self.save_path)
            else: subprocess.run(["xdg-open", str(self.save_path)])
        except Exception: pass

    def backup(self):
        src, dst = input(" [?] Źródło: "), input(" [?] Cel: ")
        try: shutil.copytree(src, dst, dirs_exist_ok=True); self.msg = f"{G} [+] Backup OK.{RESET}"
        except Exception as e: self.msg = f"{R} [!] BŁĄD: {e}{RESET}"

    def show_help(self):
        self.clear_screen()
        # Szerokość wnętrza ramki: 91 znaków
        print(f"{B}╔═══════════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{B}║{RESET}                  DOKUMENTACJA SYSTEMOWA I INSTRUKCJA OBSŁUGI                              {B}║{RESET}")
        print(f"{B}╠═══════════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{B}║{RESET}  {Y}1. NAWIGACJA I SYSTEM{RESET}                                                                    {B}║{RESET}")
        print(f"{B}║{RESET}  [1] ODŚWIEŻ     - Aktualizuje widok plików w bieżącym folderze.                          {B}║{RESET}")
        print(f"{B}║{RESET}  [2] WEJDŹ (CD)  - Przechodzi do wskazanego folderu (podaj nazwę).                        {B}║{RESET}")
        print(f"{B}║{RESET}  [3] W GÓRĘ (..) - Wraca do katalogu nadrzędnego.                                         {B}║{RESET}")
        print(f"{B}║{RESET}  [4] INFO DYSKU  - Wyświetla zajętość miejsca na bieżącym wolumenie.                      {B}║{RESET}")
        print(f"{B}║{RESET}                                                                                           {B}║{RESET}")
        print(f"{B}║{RESET}  {Y}2. ZARZĄDZANIE PLIKAMI{RESET}                                                                   {B}║{RESET}")
        print(f"{B}║{RESET}  [5] NOWY PLIK   - Tworzy pusty plik tekstowy lub systemowy.                              {B}║{RESET}")
        print(f"{B}║{RESET}  [6] NOWY FOLDER - Tworzy nową strukturę katalogu.                                        {B}║{RESET}")
        print(f"{B}║{RESET}  [7] USUŃ PLIK   - Trwale usuwa plik z dysku.                                             {B}║{RESET}")
        print(f"{B}║{RESET}  [8] USUŃ FOLDER - Kasuje folder wraz z całą jego zawartością.                            {B}║{RESET}")
        print(f"{B}║{RESET}                                                                                           {B}║{RESET}")
        print(f"{B}║{RESET}  {Y}3. OPERACJE ZAAWANSOWANE{RESET}                                                                 {B}║{RESET}")
        print(f"{B}║{RESET}  [9] ZMIEŃ NAZWĘ - Zmienia nazwę pliku lub folderu.                                       {B}║{RESET}")
        print(f"{B}║{RESET}  [10] KOPIUJ     - Kopiuje elementy (wymaga modułu shutil).                               {B}║{RESET}")
        print(f"{B}║{RESET}  [11] PRZENIEŚ   - Przenosi plik/folder do innej lokalizacji.                             {B}║{RESET}")
        print(f"{B}║{RESET}  [13] BACKUP     - Tworzy kopię zapasową (Lustro) wybranego źródła.                       {B}║{RESET}")
        print(f"{B}║{RESET}                                                                                           {B}║{RESET}")
        print(f"{B}║{RESET}  {Y}4. NARZĘDZIA I EKSPORT{RESET}                                                                   {B}║{RESET}")
        print(f"{B}║{RESET}  [12] ZAPISZ L.  - Eksportuje listę plików do formatu .txt.                               {B}║{RESET}")
        print(f"{B}║{RESET}  [14] SZUKAJ     - Przeszukuje katalogi w głąb wg zadanej frazy.                          {B}║{RESET}")
        print(f"{B}║{RESET}  [15] OTWÓRZ Z.  - Otwiera systemowy folder z zapisanymi raportami.                       {B}║{RESET}")
        print(f"{B}╠═══════════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"{B}║{RESET}  SKRÓTY: Wybierz numer [1-18] i zatwierdź [ENTER].                                        {B}║{RESET}")
        print(f"{B}╚═══════════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
        input(f"\n{G}  Naciśnij [ENTER], aby wrócić do menu...{RESET}")

    def show_about(self):
        self.clear_screen()
        print(f"{B}╔══════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"║                                O PROGRAMIE                               ║")
        print(f"╠══════════════════════════════════════════════════════════════════════════╣\n")
        print(f" Nazwa:       CMD File Manager Cli")
        print(f" Wersja:      1.5.0")
        print(f" Autor:       {__author__}")
        print(f" Kategoria:   {__category__}")
        print(f" Email:       polsoft.its@fastservice.com")
        print(f" GitHub:      https://github.com/seb07uk")
        print(f"\n Opis: {__desc__}")
        print(f"\n{B}╚══════════════════════════════════════════════════════════════════════════╝{RESET}")
        input(f"\n{G}Naciśnij [ENTER], aby wrócić...{RESET}")

if __name__ == "__main__":
    app = FileManager()
    app.run()