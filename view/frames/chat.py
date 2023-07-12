import time
import tkinter as tk
from tkinter import ttk
import requests

from view.frames.message_window import MessageWindow
from controller.conversation import completion_create
from controller.conversation.conversations.conversation_example import persona


timestamp = int(time.time())
messages = [{"role": "system", "content": "Hello, world", "timestamp": timestamp}]
message_labels = list()
messages_ai = [
    {
        "role": "system",
        "content": "",
    }
]


class Chat(ttk.Frame):
    def __init__(self, container, background, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.message_window = MessageWindow(self, background=background)
        self.message_window.grid(row=0, column=0, sticky="NSEW", pady=5)

        input_frame = ttk.Frame(self, style="Controls.TFrame", padding=10)
        input_frame.grid(row=1, column=0, sticky="EW")

        self.message_input = tk.Text(input_frame, height=3)
        self.message_input.pack(expand=True, fill="both", side="left", padx=(0, 10))

        message_submit = ttk.Button(
            input_frame,
            text="Send",
            style="SendButton.TButton",
            command=self.post_message_ai,
        )
        message_submit.pack()

        message_system = ttk.Button(
            input_frame,
            text="System",
            style="SystemButton.TButton",
            command=self.post_message_system_ai,
        )
        message_system.pack()
        self.message_window.update_message_widgets(messages, message_labels)

    def post_message(self):
        body = self.message_input.get("1.0", "end").strip()
        requests.post("http://167.99.63.70/message", json={"message": body})
        self.message_input.delete("1.0", "end")
        self.get_messages()

    def post_message_ai(self):
        global messages_ai
        global messages
        timestamp = int(time.time())
        content = self.message_input.get("1.0", "end").strip()
        user_message = completion_create.generate_message("user", content)
        messages_ai.append(user_message)
        messages.append({"role": "user", "content": content, "timestamp": timestamp})
        self.message_input.delete("1.0", "end")
        self.get_messages_ai()

    def post_message_system_ai(self):
        global messages_ai
        global messages
        timestamp = int(time.time())
        content = self.message_input.get("1.0", "end").strip()
        user_message = completion_create.generate_message("system", content)
        messages_ai.append(user_message)
        messages.append({"role": "system", "content": content, "timestamp": timestamp})
        self.message_input.delete("1.0", "end")
        self.get_messages_ai()

    def get_messages(self):
        global messages
        global message_labels
        messages = requests.get("http://167.99.63.70/messages").json()
        self.message_window.update_message_widgets(messages, message_labels)
        self.after(150, lambda: self.message_window.yview_moveto(1.0))

    def get_messages_ai(self):
        global messages_ai
        global messages
        global message_labels
        timestamp = int(time.time())
        response = completion_create.get_answer(messages_ai)["choices"][0]["message"]["content"]
        assistant_message = completion_create.generate_message("assistant", response)
        messages_ai.append(assistant_message)
        messages.append({"role": "assistant", "content": response, "timestamp": timestamp})
        self.message_window.update_message_widgets_ai(messages, message_labels)
        self.after(150, lambda: self.message_window.yview_moveto(1.0))
        # Save conversation
        persona["messages"] = messages_ai
        completion_create.save_conversation(persona)
