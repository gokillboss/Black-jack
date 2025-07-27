import tkinter as tk

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def create_label(frame, text, **kwargs):
    label = tk.Label(frame, text=text, **kwargs)
    label.pack()
    return label
