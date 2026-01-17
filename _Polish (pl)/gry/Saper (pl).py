import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time
import os

# --- KONFIGURACJA ŚCIEŻEK POLSOFT ---
USER_PROFILE = os.environ.get('USERPROFILE', os.path.expanduser('~'))
HISTORY_DIR = os.path.join(USER_PROFILE, ".polsoft", "psCli", "History", "Games")
LOG_FILE = os.path.join(HISTORY_DIR, "minesweeper_scores.log")
HOF_FILE = os.path.join(HISTORY_DIR, "hall_of_fame.txt")

if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.master.title("Minesweeper.py - Polsoft System")
        self.master.configure(bg="#282a36")
        
        # Ustawienia początkowe
        self.rows = 10
        self.cols = 10
        self.mines_count = 12
        
        self.game_over = False
        self.buttons = []
        self.mines = set()
        self.revealed = set()
        self.start_time = None
        
        self.setup_menu()
        self.setup_ui()
        self.reset_game()

    def setup_menu(self):
        menubar = tk.Menu(self.master)
        
        # Menu Gra
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="Nowa Gra [N]", command=self.reset_game)
        game_menu.add_command(label="Top 5 [T]", command=self.show_top5)
        game_menu.add_command(label="Opcje [O]", command=self.show_options)
        game_menu.add_separator()
        game_menu.add_command(label="Wyjdź [Q]", command=self.master.quit)
        menubar.add_cascade(label="Gra", menu=game_menu)
        
        # Menu Pomoc
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="O autorze", command=self.show_about)
        menubar.add_cascade(label="Pomoc", menu=help_menu)
        
        self.master.config(menu=menubar)

    def setup_ui(self):
        self.status_frame = tk.Frame(self.master, bg="#44475a", pady=5)
        self.status_frame.pack(fill="x")
        
        self.label_mines = tk.Label(self.status_frame, text="Miny: 0", 
                                    bg="#44475a", fg="#ff79c6", font=("Consolas", 10, "bold"))
        self.label_mines.pack(side="left", padx=10)
        
        self.label_time = tk.Label(self.status_frame, text="Czas: 0s", 
                                   bg="#44475a", fg="#f1fa8c", font=("Consolas", 10, "bold"))
        self.label_time.pack(side="right", padx=10)

        self.grid_frame = tk.Frame(self.master, bg="#282a36", padx=10, pady=10)
        self.grid_frame.pack()

    def reset_game(self):
        self.game_over = False
        self.start_time = time.time()
        self.revealed.clear()
        self.label_mines.config(text=f"Miny: {self.mines_count}")
        
        # Rozmieszczenie min
        self.mines = set()
        while len(self.mines) < self.mines_count:
            pos = (random.randint(0, self.rows-1), random.randint(0, self.cols-1))
            self.mines.add(pos)
            
        # Odświeżenie przycisków
        for row_btns in self.buttons:
            for btn in row_btns: btn.destroy()
        self.buttons = []
        
        for r in range(self.rows):
            row_btns = []
            for c in range(self.cols):
                btn = tk.Button(self.grid_frame, width=3, height=1, font=("Consolas", 9, "bold"),
                               relief="raised", bg="#6272a4", fg="white", activebackground="#bd93f9")
                btn.bind('<Button-1>', lambda e, r=r, c=c: self.left_click(r, c))
                btn.bind('<Button-3>', lambda e, r=r, c=c: self.right_click(r, c))
                btn.grid(row=r, column=c, padx=1, pady=1)
                row_btns.append(btn)
            self.buttons.append(row_btns)
        
        self.update_timer()

    def update_timer(self):
        if not self.game_over and self.start_time:
            elapsed = int(time.time() - self.start_time)
            self.label_time.config(text=f"Czas: {elapsed}s")
            self.master.after(1000, self.update_timer)

    def left_click(self, r, c):
        if self.game_over or (r, c) in self.revealed: return
        if (r, c) in self.mines:
            self.end_game(False)
        else:
            self.reveal(r, c)
            if len(self.revealed) == (self.rows * self.cols) - self.mines_count:
                self.end_game(True)

    def right_click(self, r, c):
        btn = self.buttons[r][c]
        if self.game_over or (r, c) in self.revealed: return
        if btn.cget("text") == "F":
            btn.config(text="", fg="white")
        else:
            btn.config(text="F", fg="#ff5555")

    def reveal(self, r, c):
        if (r, c) in self.revealed: return
        self.revealed.add((r, c))
        count = sum(1 for nr, nc in self.get_neighbors(r, c) if (nr, nc) in self.mines)
        btn = self.buttons[r][c]
        btn.config(relief="sunken", bg="#44475a", state="disabled")
        
        if count > 0:
            colors = ["", "#8be9fd", "#50fa7b", "#ffb86c", "#ff79c6", "#bd93f9", "#ff5555", "white", "white"]
            btn.config(text=str(count), disabledforeground=colors[count])
        else:
            for nr, nc in self.get_neighbors(r, c):
                self.reveal(nr, nc)

    def get_neighbors(self, r, c):
        for dr, dc in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                yield nr, nc

    def end_game(self, won):
        self.game_over = True
        elapsed = int(time.time() - self.start_time)
        
        for r, c in self.mines:
            self.buttons[r][c].config(text="*", bg="#ff5555" if not won else "#50fa7b")
        
        if won:
            name = simpledialog.askstring("Zwycięstwo!", f"Czas: {elapsed}s\nImię gracza:", initialvalue="Gracz")
            player_name = name if name else "Anonim"
            self.log_score(elapsed, "WIN", player_name)
            self.update_hof()
            messagebox.showinfo("Koniec", f"Brawo {player_name}! Twój czas: {elapsed}s")
        else:
            self.log_score(elapsed, "FAIL", "---")
            messagebox.showinfo("Koniec", "BUM! Przegrana.")
        
        self.reset_game()

    def log_score(self, elapsed, status, name):
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{now}] NAME: {name} | STATUS: {status} | CZAS: {elapsed:03d}s | minesweeper.py\n")

    def update_hof(self):
        entries = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    if "STATUS: WIN" in line:
                        try:
                            date_str = line.split("]")[0].replace("[", "")
                            name = line.split("NAME:")[1].split("|")[0].strip()
                            t = int(line.split("CZAS:")[1].split("s")[0].strip())
                            entries.append((t, name, date_str))
                        except: continue
        
        entries.sort()
        top = entries[:5]
        
        with open(HOF_FILE, "w", encoding="utf-8") as f:
            f.write("=== SAPER HALL OF FAME ===\n\n")
            f.write(f"{'POZ':<4} {'GRACZ':<15} {'CZAS':<10} {'DATA':<20}\n")
            f.write("-" * 55 + "\n")
            for i, (t, name, date_str) in enumerate(top):
                f.write(f"{i+1:<4} {name[:15]:<15} {t:<3} sek.   {date_str:<20}\n")

    def show_top5(self):
        self.update_hof()
        if os.path.exists(HOF_FILE):
            with open(HOF_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                messagebox.showinfo("Hall of Fame", content)
        else:
            messagebox.showinfo("Top 5", "Brak wygranych partii.")

    def show_options(self):
        new_mines = simpledialog.askinteger("Opcje", "Liczba min (5-50):", initialvalue=self.mines_count)
        if new_mines:
            self.mines_count = min(max(new_mines, 5), 50)
            self.reset_game()

    def show_about(self):
        about_text = (
            "Saper Systemowy v2.3\n\n"
            "Author: Sebastian Januchowski\n"
            "Email: polsoft.its@fastservice.com\n"
            "GitHub: https://github.com/seb07uk\n\n"
            "System: Polsoft psCli History"
        )
        messagebox.showinfo("About", about_text)

if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()