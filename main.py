import random
import tkinter as tk

# List of words for the typing test
word_list = ["apple", "banana", "cat", "dog", "junior", "flower", "grape", "house", "borrow", "juice",
             "key", "lemon", "mouse", "notebook", "orange", "pizza", "queen", "rabbit", "sun", "table",
             "umbrella", "van", "leg", "mice", "yellow", "zebra", "airplane", "ball", "car", "duck",
             "fish", "guitar", "hat", "island", "jacket", "kite", "lamp", "monkey", "nose", "ocean",
             "pencil", "quilt", "rose", "snake", "train", "vase", "wagon", "me", "melon",
             "back", "ant", "bird", "cup", "dolphin", "egg", "skip", "hat", "jellyfish",
             "kangaroo", "bring", "moon", "owl", "penguin", "quilt", "rainbow", "you", "turtle",
             "violin", "yarn", "butterfly", "cloud", "dinosaur", "firefly", "giraffe", "chest", "where",
             "block", "lemonade", "book", "owl", "python", "rainbow", "turtle", "guitar", "yarn"]

# Initial settings
seconds = 60
first_line = []
second_line = []
words = 0
total_words = 6
space_press_count = 0
time_up = False
after_id = None
current_word_index = 0
end = 0


# Function to format and display words in the Tkinter window
def format():
    words_label.delete(1.0, tk.END)  # Clear previous text
    formatted_first_words = " ".join(first_line)
    formatted_second_words = " ".join(second_line)
    words_label.insert(tk.END, f"{formatted_first_words}\n")
    words_label.insert(tk.END, formatted_second_words)


# Function to generate and display random words
def display_random_words():
    global first_line
    global second_line
    first_line = random.sample(word_list, total_words)
    second_line = random.sample(word_list, total_words)
    format()


# Function to update the timer label
def update_label():
    global seconds
    global time_up
    if seconds > 0 and not time_up:
        time.config(text=f"Time: {seconds}")
        seconds -= 1
        global after_id
        after_id = screen.after(1000, update_label)
    else:
        time.config(text="Time's up!")
        time_up = True


# Function to handle click event on the entry field
def on_entry_click(event):
    if not time_up:
        entry_var.set("")
        entry.config(fg="black")
        update_label()


# Function to handle key press event
def on_key_press(event):
    global space_press_count
    global current_word_index
    global end
    key = event.char
    if not time_up:
        if key == ' ' or key == '\r':
            compare_words()
            entered_words = entry_var.get().strip().split()

            # Check if there are any entered words
            if entered_words and entered_words[-1] != "":
                entry_var.set("")
                space_press_count += 1

                if space_press_count % 6 == 0:
                    swap_lines()
                    space_press_count = 0
                    current_word_index = 0
                    end = 0


# Function to compare entered words with the correct words
def compare_words():
    global first_line
    global words
    global current_word_index
    global end

    entered_words = entry_var.get().strip().split()

    if not entered_words:
        # Avoid empty lines or spaces
        return

    entered_word = entered_words[-1]

    if current_word_index < len(first_line):
        if first_line[current_word_index] == entered_word:
            words += 1
            word.config(text=f"Words: {words}")

            # Change the color of the entered word to green
            start_index = words_label.index(f"1.{end}")
            end += len(first_line[current_word_index]) + 1
            end_index = f"{start_index}+{len(first_line[current_word_index])}c"
            words_label.tag_add("correct", start_index, end_index)
            words_label.tag_configure("correct", foreground="green")

        else:
            # Change the color of the entered word to red
            start_index = words_label.index(f"1.{end}")
            end += len(first_line[current_word_index]) + 1
            end_index = f"{start_index}+{len(first_line[current_word_index])}c"
            words_label.tag_add("incorrect", start_index, end_index)
            words_label.tag_configure("incorrect", foreground="red")

        current_word_index += 1


# Function to swap the lines of words
def swap_lines():
    global first_line
    global second_line
    first_line, second_line = second_line, random.sample(word_list, 6)
    print("Lines swapped.")
    format()


# Function to restart the typing test
def restart():
    global seconds
    global time_up
    global first_line
    global second_line
    global words
    global space_press_count
    global after_id
    global current_word_index
    global end

    # Restore initial settings
    end = 0
    seconds = 60
    time_up = False
    first_line = []
    second_line = []
    words = 0
    space_press_count = 0
    current_word_index = 0

    # Update labels
    time.config(text=f"Time: {seconds}")
    word.config(text=f"Words: {words}")

    # Clear entry field
    entry_var.set("")
    entry.config(fg="black", state=tk.NORMAL)  # Add this line

    screen.after_cancel(after_id)

    # Restart word generation
    display_random_words()

    # Restart time countdown
    update_label()


# Create the main window
screen = tk.Tk()
screen.minsize(500, 400)
screen.title("Typing Speed Test")

# Labels for time and words
time = tk.Label(screen, text="Time: 60 ", font=("Helvetica", 16))
time.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

word = tk.Label(screen, text="Words: 0", font=("Helvetica", 16))
word.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

# Text widget to display words
words_label = tk.Text(screen, wrap=tk.WORD, font=("Helvetica", 14), height=2, width=40)
words_label.grid(row=1, column=0, pady=(90, 10), padx=(90, 0))

# Entry widget for typing
entry_var = tk.StringVar()
entry_var.set("Type your text here")

entry = tk.Entry(screen, textvariable=entry_var)
entry.grid(row=2, column=0, pady=(0, 10), padx=(90, 0))
entry.bind("<FocusIn>", on_entry_click)
entry.bind("<Key>", on_key_press)

# Button to restart the test
restart_button = tk.Button(screen, text="Restart", command=restart)
restart_button.grid(row=3, column=0, pady=(30, 10), padx=(80, 0))

# Initial display of random words
display_random_words()

# Start the main event loop
screen.mainloop()