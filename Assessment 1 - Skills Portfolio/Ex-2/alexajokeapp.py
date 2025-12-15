import tkinter as tk
import random

# ------------------ Load Jokes ------------------ #
def load_jokes():
    jokes = []
    try:
        with open(r"Assessment 1 - Skills Portfolio\Ex-2\randomJokes.txt", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if "?" in line:
                    setup, punchline = line.split("?", 1)
                    jokes.append((setup + "?", punchline.strip()))
    except FileNotFoundError:
        jokes.append(("Error: randomJokes.txt not found!", "Please add the file."))
    return jokes


jokes_list = load_jokes()
current_joke = None


# ------------------ Functions ------------------ #
def tell_joke():
    global current_joke
    current_joke = random.choice(jokes_list)
    setup_label.config(text=current_joke[0])
    punchline_label.config(text="")

def show_punchline():
    if current_joke:
        punchline_label.config(text=current_joke[1])

def next_joke():
    tell_joke()


# ------------------ GUI ------------------ #
root = tk.Tk()
root.title("Joke Hub")
root.state("zoomed")   # Full screen
root.configure(bg="#0f172a")

# ------------------ Title ------------------ #
title = tk.Label(
    root,
    text="😂 Joke Hub",
    font=("Segoe UI", 36, "bold"),
    fg="#f8fafc",
    bg="#0f172a"
)
title.pack(pady=30)

subtitle = tk.Label(
    root,
    text="Because everyone needs a laugh",
    font=("Segoe UI", 16),
    fg="#94a3b8",
    bg="#0f172a"
)
subtitle.pack(pady=5)

# ------------------ Joke Card ------------------ #
card = tk.Frame(
    root,
    bg="#1e293b",
    bd=0,
    padx=40,
    pady=40
)
card.pack(pady=40)

setup_label = tk.Label(
    card,
    text="Click below to hear a joke 👇",
    font=("Segoe UI", 20, "bold"),
    fg="#f1f5f9",
    bg="#1e293b",
    wraplength=800,
    justify="center"
)
setup_label.pack(pady=20)

punchline_label = tk.Label(
    card,
    text="",
    font=("Segoe UI", 18, "italic"),
    fg="#38bdf8",
    bg="#1e293b",
    wraplength=800,
    justify="center"
)
punchline_label.pack(pady=20)

# ------------------ Buttons ------------------ #
button_frame = tk.Frame(root, bg="#0f172a")
button_frame.pack(pady=20)

btn_style = {
    "font": ("Segoe UI", 14, "bold"),
    "bg": "#38bdf8",
    "fg": "#020617",
    "width": 18,
    "bd": 0,
    "activebackground": "#0ea5e9",
    "activeforeground": "#020617"
}

tk.Button(button_frame, text="Tell Me a Joke", command=tell_joke, **btn_style).grid(row=0, column=0, padx=15)
tk.Button(button_frame, text="Show Punchline", command=show_punchline, **btn_style).grid(row=0, column=1, padx=15)
tk.Button(button_frame, text="Next Joke", command=next_joke, **btn_style).grid(row=0, column=2, padx=15)

# ------------------ Quit Button ------------------ #
tk.Button(
    root,
    text="Quit",
    font=("Segoe UI", 12, "bold"),
    bg="#ef4444",
    fg="white",
    width=12,
    bd=0,
    command=root.destroy
).pack(pady=25)

root.mainloop()

