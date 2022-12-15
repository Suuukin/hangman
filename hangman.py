import tkinter as tk
import tkinter.font as font
import wordlist
import random

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


print(State.word)


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


def update_label(label, text=None, color=None):
    label.configure(text=text, bg=color)


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
    return positions


def submit_guess(letter):
    positions = position_check(State.guess)
    button = State.buttons[letter]
    update_keyboard(button, color='grey', state='disabled')
    for position in positions:
        label = State.labels[position]
        update_label(label, text=State.guess)



def btn_op(text):
    label = State.guess_display
    if text == "BACKSPACE":
        update_label(label, text=text)
        State.guess = " "
    elif text == "ENTER":
        submit_guess(State.guess)
    else:
        update_label(label, text=text)
        State.guess = text


def button_binder(frame, text):
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

    window = tk.Tk()
    window.title("word")
    window.resizable(False, False)

    GRID_FONT = font.Font(family="Courier", size=50, weight="bold")
    KEYBOARD_FONT = font.Font(family="Courier", size=30, weight="bold")

    guess_area = tk.Frame(window, width=300, height=200, bg="honeydew2")
    guess_area.grid(row=0, column=1)


    State.guess_display = guess_display = label_maker(window)
    guess_display.grid(row=1, column=1)


    for x, letter in enumerate(State.letters):
        label = label_maker(guess_area)
        State.labels[x+1] = label
        label.grid(row=1, column=x+1, sticky="nsew")

    for row, key_row in enumerate(KEY_ROWS):
        State.keyboard_frames[row] = frame = tk.Frame(
            window, width=300, height=50, bg="honeydew2"
        )
        frame.grid(row=row + 2, column=1)
        keys = list(key_row)
        for column, key_text in enumerate(keys):
            State.buttons[key_text] = button = btn_maker(frame, key_text)
            button_binder(window, key_text)
            button.grid(row=1, column=column + 1)

    enter_btn = btn_maker(State.keyboard_frames[2], "ENTER")
    enter_btn.grid(row=1, column=9)
    button_binder(window, "ENTER")
    clear_btn = btn_maker(State.keyboard_frames[0], "CE")
    clear_btn.grid(row=1, column=11)
    button_binder(window, "BACKSPACE")
    button_binder(window, "CE")

    window.mainloop()


if __name__ == "__main__":
    main()
