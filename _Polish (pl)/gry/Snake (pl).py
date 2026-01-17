import turtle
import time
import random
import os

# --- KONFIGURACJA ŚCIEŻEK ---
USER_PROFILE = os.environ.get('USERPROFILE', os.path.expanduser('~'))
HISTORY_DIR = os.path.join(USER_PROFILE, ".polsoft", "psCli", "History", "Games")
LOG_FILE = os.path.join(HISTORY_DIR, "snake_scores.log")

if not os.path.exists(HISTORY_DIR):
    os.makedirs(HISTORY_DIR)

# --- USTAWIENIA EKRANU ---
wn = turtle.Screen()
wn.title("Snake.py - Polsoft System")
wn.bgcolor("#0f0f0f")
wn.setup(width=600, height=450)
wn.tracer(0)

# --- ZMIENNE GLOBALNE ---
score = 0
speed_level = 3 
delay = 0.1
segments = []
game_state = "MENU"

# --- OBIEKTY GRY ---
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("#50fa7b")
head.penup()
head.hideturtle()
head.direction = "stop"

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("#ff5555")
food.penup()
food.hideturtle()

pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()

# --- FUNKCJE SYSTEMOWE ---

def log_result(final_score):
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{now}] WYNIK: {final_score:04d} | POZIOM: {speed_level} | snake.py\n"
    try:
        with open(LOG_FILE, "a") as f:
            f.write(entry)
    except: pass

def get_top_5():
    if not os.path.exists(LOG_FILE):
        return ["Brak wyników"]
    scores = []
    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                if "WYNIK:" in line:
                    val = int(line.split("WYNIK:")[1].split("|")[0].strip())
                    scores.append(val)
        scores.sort(reverse=True)
        return list(dict.fromkeys(scores))[:5]
    except:
        return ["Błąd odczytu"]

# --- FUNKCJE RENDERUJĄCE ---

def show_menu():
    global game_state
    game_state = "MENU"
    pen.clear()
    head.hideturtle()
    food.hideturtle()
    pen.goto(0, 80)
    pen.color("#bd93f9")
    pen.write("S N A K E   S Y S T E M", align="center", font=("Consolas", 24, "bold"))
    pen.color("white")
    pen.goto(0, -70)
    pen.write("[N] Nowa Gra\n[O] Opcje (Prędkość)\n[T] Top 5\n[H] Pomoc\n[Q] Wyjdź", 
             align="center", font=("Consolas", 14, "normal"))
    wn.update()

def show_options():
    global game_state
    game_state = "OPTIONS"
    pen.clear()
    pen.goto(0, 80)
    pen.color("#8be9fd")
    pen.write("USTAWIENIA PRĘDKOŚCI", align="center", font=("Consolas", 20, "bold"))
    pen.color("white")
    pen.goto(0, 0)
    msg = f"Aktualny Poziom: {speed_level}\n\nNaciśnij [1-5] aby zmienić\nNaciśnij [M] aby wrócić"
    pen.write(msg, align="center", font=("Consolas", 14, "normal"))
    wn.update()

def set_speed(level):
    global speed_level
    speed_level = int(level)
    if game_state == "OPTIONS":
        show_options()

def show_help():
    global game_state
    game_state = "HELP"
    pen.clear()
    pen.color("#f1fa8c")
    pen.goto(0, 110)
    pen.write("STEROWANIE", align="center", font=("Consolas", 18, "bold"))
    pen.color("white")
    pen.goto(0, 20)
    instructions = (
        "Strzałki: Ruch Wężem\n"
        "M: Menu Główne | Q: Wyjście\n"
        "1-5: Poziom Prędkości (w Opcjach)\n"
        "Zjadaj czerwone punkty, aby rosnąć."
    )
    pen.write(instructions, align="center", font=("Consolas", 11, "normal"))
    pen.color("#6272a4")
    pen.goto(0, -70)
    pen.write("------------------------------------", align="center", font=("Consolas", 10, "normal"))
    pen.goto(0, -95)
    pen.write("Autor: Sebastian Januchowski", align="center", font=("Consolas", 10, "bold"))
    pen.goto(0, -115)
    pen.write("Email: polsoft.its@fastservice.com", align="center", font=("Consolas", 10, "normal"))
    pen.goto(0, -135)
    pen.write("GitHub: https://github.com/seb07uk", align="center", font=("Consolas", 10, "normal"))
    pen.color("white")
    pen.goto(0, -180)
    pen.write("Naciśnij [M], aby wrócić do Menu", align="center", font=("Consolas", 10, "italic"))
    wn.update()

def show_top5():
    global game_state
    game_state = "TOP5"
    pen.clear()
    pen.goto(0, 80)
    pen.color("#f1fa8c")
    pen.write("TOP 5 WYNIKÓW:", align="center", font=("Consolas", 18, "bold"))
    top = get_top_5()
    pen.color("white")
    y_pos = 30
    for i, s in enumerate(top):
        pen.goto(0, y_pos)
        pen.write(f"{i+1}. {s}", align="center", font=("Consolas", 14, "normal"))
        y_pos -= 30
    pen.goto(0, -140)
    pen.write("Naciśnij [M], aby wrócić", align="center", font=("Consolas", 10, "italic"))
    wn.update()

# --- LOGIKA GRY ---

def start_game():
    global game_state, score, delay, segments
    game_state = "PLAYING"
    pen.clear()
    score = 0
    delay = 0.22 - (speed_level * 0.04)
    head.goto(0, 0)
    head.direction = "stop"
    head.showturtle()
    food.showturtle()
    for s in segments: s.hideturtle()
    segments.clear()
    update_hud()

def update_hud():
    pen.clear()
    pen.goto(0, 180)
    pen.color("white")
    pen.write(f"Wynik: {score}  |  Poziom: {speed_level}", align="center", font=("Consolas", 14, "bold"))

def go_up(): 
    if head.direction != "down": head.direction = "up"
def go_down(): 
    if head.direction != "up": head.direction = "down"
def go_left(): 
    if head.direction != "right": head.direction = "left"
def go_right(): 
    if head.direction != "left": head.direction = "right"

def move():
    if head.direction == "up": head.sety(head.ycor() + 20)
    if head.direction == "down": head.sety(head.ycor() - 20)
    if head.direction == "left": head.setx(head.xcor() - 20)
    if head.direction == "right": head.setx(head.xcor() + 20)

# --- MAPOWANIE KLAWISZY ---
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")
wn.onkeypress(start_game, "n")
wn.onkeypress(show_options, "o")
wn.onkeypress(show_top5, "t")
wn.onkeypress(show_help, "h")
wn.onkeypress(show_menu, "m")
wn.onkeypress(lambda: set_speed(1), "1")
wn.onkeypress(lambda: set_speed(2), "2")
wn.onkeypress(lambda: set_speed(3), "3")
wn.onkeypress(lambda: set_speed(4), "4")
wn.onkeypress(lambda: set_speed(5), "5")
wn.onkeypress(wn.bye, "q")

# --- GŁÓWNA PĘTLA ---
show_menu()

while True:
    wn.update()
    if game_state == "PLAYING":
        if abs(head.xcor()) > 290 or abs(head.ycor()) > 210:
            log_result(score)
            time.sleep(0.5)
            for s in segments: s.hideturtle()
            show_menu()
            continue

        if head.distance(food) < 20:
            food.goto(random.randint(-14, 14)*20, random.randint(-10, 8)*20)
            new_seg = turtle.Turtle("square")
            new_seg.color("#6272a4")
            new_seg.penup()
            segments.append(new_seg)
            score += 10
            delay = max(0.01, delay - (0.001 * speed_level))
            update_hud()

        for i in range(len(segments)-1, 0, -1):
            segments[i].goto(segments[i-1].xcor(), segments[i-1].ycor())
        if len(segments) > 0:
            segments[0].goto(head.xcor(), head.ycor())

        move()

        for seg in segments:
            if seg.distance(head) < 20:
                log_result(score)
                time.sleep(0.5)
                for s in segments: s.hideturtle()
                show_menu()
        
        time.sleep(delay)

wn.mainloop()