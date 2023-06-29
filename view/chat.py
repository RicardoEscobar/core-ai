"""This module creates the GUI for the chatbot."""
import tkinter as tk
from tkinter import ttk


try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    pass

def send_text(chat_history: tk.Text, user_input: ttk.Entry, user_color: str = "red"):
    """Sends text from input text widget to chat history."""
    user_input_text = user_input.get()

    # Create a tag that specifies the color.
    chat_history.tag_config(user_color, foreground=user_color)

    # if the user_input_text is empty, return
    if not user_input_text:
        return

    # Clear the user_input widget.
    user_input.delete(0, tk.END)

    # Insert the user_input_text into the chat_history widget.
    chat_history.insert(tk.END, "User:\n", "red")
    chat_history.insert(tk.END, user_input_text + "\n")

def create_gui():
    """Creates the GUI."""
    root = tk.Tk()
    root.title("Chatbot")

    # Configure the row and column weights of the root window's grid manager.
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # Create a custom style for the main_frame widget.
    style = ttk.Style()
    style.configure("Blue.TFrame", background="blue")

    # Create the main_frame widget with the custom style.
    main_frame = ttk.Frame(root, padding=10, style="Blue.TFrame")

    # Configure the row and column weights of the main_frame widget's grid manager.
    main_frame.rowconfigure(0, weight=1)
    main_frame.columnconfigure(0, weight=1)

    # Chatlog frame
    chatlog_frame = ttk.Frame(main_frame)

    # Configure the row and column weights of the chatlog_frame widget's grid manager.
    chatlog_frame.rowconfigure(0, weight=1)
    chatlog_frame.columnconfigure(0, weight=1)

    # User input frame
    user_input_frame = ttk.Frame(main_frame)

    # Configure the row and column weights of the user_input_frame widget's grid manager.
    user_input_frame.rowconfigure(0, weight=0)
    user_input_frame.columnconfigure(0, weight=1)

    # Text widget that contains the chat history.
    chat_history = tk.Text(chatlog_frame, height=20, width=50)

    # Scrollbar for the chat history.
    chat_history_scrollbar = ttk.Scrollbar(
        chatlog_frame, orient="vertical", command=chat_history.yview
    )
    chat_history["yscrollcommand"] = chat_history_scrollbar.set

    # Entry widget for the user's input.
    user_input = ttk.Entry(user_input_frame, width=50)

    # Bind the <Return> event to the user_input widget.
    user_input.bind("<Return>", lambda event: send_text(chat_history, user_input))

    # Button to send the user's input.
    send_button = ttk.Button(user_input_frame, text="Send", command=lambda: send_text(chat_history, user_input))

    # Grid the main_frame widget with the sticky option set to "nsew".
    main_frame.grid(row=0, column=0, sticky="nsew")
    chatlog_frame.grid(row=0, column=0, sticky="nsew")
    user_input_frame.grid(row=1, column=0, sticky="nsew")

    # Grid the chat_history widget with the sticky option set to "nsew".
    chat_history.grid(row=0, column=0, sticky="nsew")

    # Grid the chat_history_scrollbar widget with the sticky option set to "ns".
    chat_history_scrollbar.grid(row=0, column=1, sticky="ns")

    # Grid the user_input widget with the sticky option set to "ew".
    user_input.grid(row=1, column=0, sticky="ew")

    # Grid the send_button widget with the sticky option set to "ew".
    send_button.grid(row=1, column=1, sticky="e")

    # Focus the user_input widget.
    user_input.focus()

    # Run the mainloop
    root.mainloop()

def main():
    """The main function."""
    create_gui()

if __name__ == "__main__":
    main()