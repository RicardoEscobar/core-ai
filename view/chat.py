"""This module creates the GUI for the chatbot."""

# Add root directory to path, to fix imports
if __name__ == "__main__":
    from sys import path
    from pathlib import Path
    root = Path(__file__).parent.parent
    path.append(str(root))

import tkinter as tk
from tkinter import ttk

from controller.conversation.completion_create import generate_message, get_answer, save_conversation
from controller.conversation.conversations.conversation_example import persona

# Fix blurry text on Windows
try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    pass


def send_text(
    chat_history: tk.Text, user_name: str, text: str, user_color: str = "red"
):
    """Sends text from input text widget to chat history."""

    # Create a tag that specifies the color.
    chat_history.tag_config(user_color, foreground=user_color)

    # if the user_input_text is empty, return
    if not text:
        return

    # Insert the user_input_text into the chat_history widget.
    chat_history.insert(tk.END, f"{user_name}:\n", user_color)
    chat_history.insert(tk.END, f"{text}\n\n")


def send_command(
    user_input_text: tk.Entry,
    chat_history: tk.Text,
    user_name: str,
    user_color: str = "red",
):
    """Gets the user input from the input text widget and sends it to the chat history widget."""

    # Get the user input text from the input text widget.
    text = user_input_text.get().strip()

    # Clears the user input text from the input text widget.
    user_input_text.delete(0, tk.END)

    # Send the user input text to the chat history widget.
    send_text(chat_history, user_name, text, user_color)

    # Save the response to the persona["messages"] list
    messages_list = persona["messages"]
    messages_list.append(generate_message("user", text))
    response = get_answer(messages_list)['choices'][0]['message']['content']
    messages_list.append(generate_message("assistant", response))
    persona["messages"] = messages_list

    # If selected_voice is None, then use the default voice
    save_conversation(persona)

    # Send the response to the chat history widget.
    send_text(chat_history, "Assistant", response, "blue")

    # Scroll the chat history to the bottom.
    chat_history.see(tk.END)


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
    main_frame = ttk.Frame(root, padding=10)

    # Configure the row and column weights of the main_frame widget's grid manager.
    main_frame.rowconfigure(0, weight=1)
    main_frame.columnconfigure(0, weight=1)

    # Chatlog frame
    chatlog_frame = ttk.Frame(main_frame, padding=10)

    # Configure the row and column weights of the chatlog_frame widget's grid manager.
    chatlog_frame.rowconfigure(0, weight=1)
    chatlog_frame.columnconfigure(0, weight=1)

    # User input frame
    user_input_frame = ttk.Frame(main_frame, padding=10)

    # Configure the row and column weights of the user_input_frame widget's grid manager.
    user_input_frame.rowconfigure(0, weight=0)
    user_input_frame.columnconfigure(0, weight=1)

    # Text widget that contains the chat history.
    chat_history = tk.Text(chatlog_frame, height=20, width=50, wrap='word')

    # Scrollbar for the chat history.
    chat_history_scrollbar = ttk.Scrollbar(
        chatlog_frame, orient="vertical", command=chat_history.yview
    )
    chat_history["yscrollcommand"] = chat_history_scrollbar.set

    # Entry widget for the user's input.
    user_input = ttk.Entry(user_input_frame, width=50)

    # Bind the <Return> event to the user_input widget.
    user_input.bind(
        "<Return>", lambda event: send_command(user_input, chat_history, "User", "red")
    )

    # Button to send the user's input.
    send_button = ttk.Button(
        user_input_frame,
        text="Send",
        command=lambda: send_command(user_input, chat_history, "User", "red"),
    )

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
