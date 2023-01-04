import tkinter as tk
import tkinter.font as font
import wordlist
import random
import os
from PIL import ImageTk, Image


# flake8: noqa


class State:
    labels = {}  # {point, label}
    buttons = {}  # {key_text, button}
    word = random.choice(wordlist.wordlist)
    letters = list(word)
    keyboard_frames = {}
    current_x = 1
    guess = ""
    game_over = False
    guess_display = None
    incorrect_guesses = 0
    hangman_images = {}
    hangman_label = None


print(State.word)


def image_loader(name):
    image_dir = os.path.join(IMAGE_PATH, name)
    print(image_dir)
    return ImageTk.PhotoImage(file=image_dir)


def image_selector(image_number):
    image = State.hangman_images[image_number]
    label = State.hangman_label
    update_label(label, image=image)


def label_maker(frame):
    """Function to creates the labels in the 5*6 grid."""
    return tk.Label(
        frame,
        text=" ",
        font=GRID_FONT,
        borderwidth=3,
        padx=20,
        pady=10,
        relief="groove",
    )


def btn_maker(frame, text):
    """Function to create the buttons for the keyboard."""
    return tk.Button(frame, text=text, font=KEYBOARD_FONT, command=lambda: btn_op(text))


def update_label(label, text=None, color=None, image=None):
    label.configure(text=text, bg=color, image=image)


def update_keyboard(button, color=None, state=None):
    if button["bg"] != "green":
        button.configure(bg=color, state=state)


def position_check(guess_letter):
    """Checks for what positions the letter is in the word.
    Then returns all the positions that the letter is in."""
    positions = []  # list to store positions for each 'char' in 'word'
    for i, location in enumerate(State.letters):
        if State.letters[i] == guess_letter:
            positions.append(i + 1)
    if positions == []:
        return None
    else:
        return positions


def submit_guess(letter):
    """Checks if the letter guessed is in the word and
    if so fills the slots in the word where the letter is.
    If not in the word draws more of the hangman."""
    if State.incorrect_guesses >= 6:
        State.game_over = True
        print(State.game_over)
        return

    button = State.buttons[letter]
    positions = position_check(State.guess)

    if positions is None:
        State.incorrect_guesses += 1
        update_keyboard(button, color="grey", state="disabled")
        image_selector(State.incorrect_guesses)
        return

    for position in positions:
        label = State.labels[position]
        update_label(label, text=State.guess)
        update_keyboard(button, color="lime", state="disabled")


def btn_op(text):
    """Updates the label for normal keyboard,
    or does specific function for special buttons."""
    if not State.game_over:
        label = State.guess_display

        if text == "BACKSPACE":
            State.guess = " "
            update_label(label, text=" ")

        elif text == "ENTER":
            submit_guess(State.guess)

        else:
            State.guess = text
            update_label(label, text=text)


def button_binder(frame, text):
    """Binds a specific keyboard key to a button in the gui."""
    if text == "ENTER":
        frame.bind("<Return>", lambda event: btn_op(text))
    elif text == "BACKSPACE":
        frame.bind("<BackSpace>", lambda event: btn_op(text))
    else:
        frame.bind(str(text), lambda event: btn_op(text))


KEY_ROWS = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]


def main():
    global GRID_FONT
    global KEYBOARD_FONT
    global SCRIPT_DIR
    global IMAGE_PATH 
    window = tk.Tk()
    window.title("Hangman")
    window.resizable(False, False)

    GRID_FONT = font.Font(family="Courier", size=30, weight="bold")
    KEYBOARD_FONT = font.Font(family="Courier", size=25, weight="bold")
    SCRIPT_DIR = os.path.dirname(__file__)
    IMAGE_PATH = os.path.join(SCRIPT_DIR, "hangman_pictures")

    IMAGE_NAMES = [
        "gallow.png",
        "head.png",
        "body.png",
        "arm1.png",
        "arm2.png",
        "leg1.png",
        "leg2.png",
    ]

    for i, name in enumerate(IMAGE_NAMES):
        State.hangman_images[i] = image_loader(name)

    State.hangman_label = tk.Label(
        window, image=State.hangman_images[State.incorrect_guesses]
    )

    State.hangman_label.grid(row=0, column=1)   

    State.guess_display = guess_display = label_maker(window)
    guess_display.grid(row=2, column=1)


    guess_area = tk.Frame(window, width=300, height=200, bg="honeydew2")
    guess_area.grid(row=1, column=1)


    for x, letter in enumerate(State.letters):
        label = label_maker(guess_area)
        State.labels[x + 1] = label
        label.grid(row=1, column=x + 1, sticky="nsew")

    for row, key_row in enumerate(KEY_ROWS):
        State.keyboard_frames[row] = frame = tk.Frame(
            window, width=300, height=50, bg="honeydew2"
        )
        frame.grid(row=row + 3, column=1)
        keys = list(key_row)
        for column, key_text in enumerate(keys):
            State.buttons[key_text] = button = btn_maker(frame, key_text)
            button_binder(window, key_text)
            button.grid(row=1, column=column + 1)

    enter_btn = btn_maker(State.keyboard_frames[2], "ENTER")
    enter_btn.grid(row=1, column=9)
    button_binder(window, "ENTER")
    button_binder(window, "BACKSPACE")

    window.mainloop()


if __name__ == "__main__":
    main()
