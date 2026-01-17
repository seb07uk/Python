import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from datetime import datetime
import os

root = tk.Tk()
root.title("Notatnik Eksporter v1.0")
root.geometry("800x600")

text_area = tk.Text(root, wrap="word", undo=True)
text_area.pack(expand=True, fill="both")

status_bar = tk.Label(root, text="Znaki: 0", anchor="e")
status_bar.pack(fill="x")

def update_char_count(event=None, file_size=None):
    content = text_area.get(1.0, tk.END).strip()
    lines = content.count("\n") + 1 if content else 0
    chars = len(content)
    size_info = f" | Size: {file_size} bytes" if file_size is not None else ""
    status_bar.config(text=f"Characters: {chars} | Lines: {lines}{size_info}")

text_area.bind("<KeyRelease>", update_char_count)

def apply_theme(theme):
    if theme == "light":
        text_area.config(bg="white", fg="black", insertbackground="black")
        status_bar.config(bg="lightgray", fg="black")
    elif theme == "dark":
        text_area.config(bg="#1e1e1e", fg="#dcdcdc", insertbackground="#dcdcdc")
        status_bar.config(bg="#2e2e2e", fg="#dcdcdc")
    elif theme == "neutral":
        text_area.config(bg="#f0f0f0", fg="#333333", insertbackground="#333333")
        status_bar.config(bg="#d0d0d0", fg="#333333")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, content)
                file_size = os.path.getsize(file_path)
                update_char_count(file_size=file_size)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot open file:\n{e}")

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                              filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")])
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text_area.get(1.0, tk.END))
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można zapisać pliku:\n{e}")

def preview_export():
    preview_window = Toplevel(root)
    preview_window.title("Podgląd eksportu")
    preview_window.geometry("600x400")
    preview_text = tk.Text(preview_window, wrap="word")
    preview_text.pack(expand=True, fill="both")
    preview_text.insert(tk.END, text_area.get(1.0, tk.END))
    preview_text.config(state="disabled")

def add_header(extension, content):
    if extension == "py":
        return "# -*- coding: utf-8 -*-\n" + content
    elif extension == "ps1":
        return "# PowerShell script\n" + content
    elif extension == "bat":
        return "REM Batch script\n" + content
    elif extension == "vbs":
        return "''' VBScript file '''\n" + content
    elif extension == "reg":
        return "Windows Registry Editor Version 5.00\n\n" + content
    else:
        return content

def export_to(extension):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    default_name = f"eksport_{now}.{extension}"
    file_path = filedialog.asksaveasfilename(
        initialfile=default_name,
        defaultextension=f".{extension}",
        filetypes=[(f"Plik .{extension}", f"*.{extension}")]
    )
    if file_path:
        content = text_area.get(1.0, tk.END).strip()
        try:
            if extension == "html":
                content = f"<html><body><pre>{content}</pre></body></html>"
            elif extension == "md":
                content = f"```\n{content}\n```"
            elif extension == "rtf":
                content = r"{\rtf1\ansi\deff0\n" + content.replace("\n", r"\line ") + "}"
            else:
                content = add_header(extension, content)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            messagebox.showinfo("Sukces", f"Zapisano jako {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można eksportować:\n{e}")

def export_all_formats():
    folder = filedialog.askdirectory(title="Wybierz folder do eksportu")
    if not folder:
        return
    content = text_area.get(1.0, tk.END).strip()
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    formats = {
        "txt": content,
        "doc": content,
        "bat": add_header("bat", content),
        "vbs": add_header("vbs", content),
        "ps1": add_header("ps1", content),
        "py": add_header("py", content),
        "reg": add_header("reg", content),
        "html": f"<html><body><pre>{content}</pre></body></html>",
        "md": f"```\n{content}\n```",
        "rtf": r"{\rtf1\ansi\deff0\n" + content.replace("\n", r"\line ") + "}"
    }
    try:
        for ext, data in formats.items():
            file_path = os.path.join(folder, f"eksport_{now}.{ext}")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(data)
        messagebox.showinfo("Sukces", f"Zapisano wszystkie formaty w:\n{folder}")
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie można zapisać plików:\n{e}")

def clear_text():
    if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz wyczyścić cały tekst?"):
        text_area.delete(1.0, tk.END)
        update_char_count()

menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Otwórz", command=open_file)
file_menu.add_command(label="Zapisz", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Wyjście", command=root.quit)
menu_bar.add_cascade(label="Plik", menu=file_menu)

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Cofnij", command=text_area.edit_undo)
edit_menu.add_command(label="Ponów", command=text_area.edit_redo)
edit_menu.add_separator()
edit_menu.add_command(label="Wyczyść", command=clear_text)
menu_bar.add_cascade(label="Edycja", menu=edit_menu)

export_menu = tk.Menu(menu_bar, tearoff=0)
export_menu.add_command(label="Podgląd eksportu", command=preview_export)
export_menu.add_command(label="Zapisz do wszystkich formatów", command=export_all_formats)
for ext in ["txt", "doc", "bat", "vbs", "ps1", "py", "reg", "html", "md", "rtf"]:
    export_menu.add_command(label=f"Eksportuj do {ext.upper()}", command=lambda e=ext: export_to(e))
menu_bar.add_cascade(label="Eksport", menu=export_menu)

theme_menu = tk.Menu(menu_bar, tearoff=0)
theme_menu.add_command(label="Domyślny (jasny)", command=lambda: apply_theme("light"))
theme_menu.add_command(label="Tryb nocny", command=lambda: apply_theme("dark"))
theme_menu.add_command(label="Neutralny", command=lambda: apply_theme("neutral"))
menu_bar.add_cascade(label="Motyw", menu=theme_menu)


# ⌨️ Skróty klawiszowe
root.bind("<Control-o>", lambda e: open_file())
root.bind("<Control-s>", lambda e: save_file())
root.bind("<Control-E>", lambda e: preview_export())
root.bind("<Control-e>", lambda e: preview_export())
root.bind("<Control-Shift-E>", lambda e: export_all_formats())
root.bind("<Control-Shift-e>", lambda e: export_all_formats())
root.bind("<Control-Shift-X>", lambda e: clear_text())
root.bind("<Control-1>", lambda e: apply_theme("light"))
root.bind("<Control-2>", lambda e: apply_theme("dark"))
root.bind("<Control-3>", lambda e: apply_theme("neutral"))

def show_about():
    messagebox.showinfo("O programie", "polsoft.ITS London\n\nNotepad Exporter v1.0\nz historią, eksportem i zmienną Ans\n\nCopyright 2025© Sebastian Januchowski")


root.config(menu=menu_bar)
apply_theme("light")
root.mainloop()