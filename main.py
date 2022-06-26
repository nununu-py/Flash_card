import csv
import random
import pandas
from tkinter import *
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
translate_in_en = ""

# --------------------------MY FUNCTION------------------------------

df = pandas.read_csv("data/french_words.csv")
data_records = df.to_dict(orient="records")


def next_word():
    global current_card, wait_for_flip, translate_in_en
    window.after_cancel(wait_for_flip)

    current_card = random.choice(data_records)

    france_word = current_card["French"]
    translate_in_en = current_card["English"]

    canvas.itemconfig(background_img, image=front_background)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=f"{france_word}", fill="black")

    wait_for_flip = window.after(3000, func=flip_card)

    data_records.remove(current_card)
    print(len(data_records))


def flip_card():
    global current_card, translate_in_en

    translate_in_en = current_card["English"]
    canvas.itemconfig(background_img, image=flip_background)
    canvas.itemconfig(title, text="Translate in English", fill="white")
    canvas.itemconfig(word, text=f"{translate_in_en}", fill="white")


def unknown_words():
    try:
        with open("data/word_to_learn.csv") as file:
            pandas.read_csv(file)
    except FileNotFoundError:
        with open("data/word_to_learn.csv", "w", newline="") as file:
            add_data = csv.writer(file)
            add_data.writerow(["Word in French", "Translate in English"])
    else:
        with open("data/word_to_learn.csv", "r+", newline="") as file:
            existing_data = csv.reader(file)
            new_data = [current_card["French"], current_card["English"]]
            if new_data not in existing_data:
                add_data = csv.writer(file)
                add_data.writerow(new_data)


# Window
window = Tk()
window.title("Flash Card App")
window.configure(background=f"{BACKGROUND_COLOR}", pady=35, padx=35)

# Front Canvas
front_background = PhotoImage(file="images/card_front.png")
flip_background = PhotoImage(file="images/card_back.png")
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
background_img = canvas.create_image(410, 270, image=front_background)

title = canvas.create_text(400, 100, text="Title", font=("Helvetica", 20, "italic"))
word = canvas.create_text(400, 260, text="Word", font=("Arial", 40, "bold"))
wait_for_flip = window.after(3000, func=flip_card)
next_word()
canvas.grid(row=0, column=0, columnspan=2, pady=20)

# Back Canvas

# Button
x_mark_img = PhotoImage(file="images/wrong.png")
x_button = Button(image=x_mark_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=unknown_words)
x_button.grid(row=1, column=0)

check_mark_img = PhotoImage(file="images/right.png")
check_mark_button = Button(image=check_mark_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_word)
check_mark_button.grid(row=1, column=1)

window.mainloop()
