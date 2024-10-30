# socket library - low-level networking interface, networking functionality
# threading library - allows eahc client to run on its own thread for
# simultaneous communication
# tkinter library - to set up GUI

import socket
import threading
import tkinter as tk
from tkinter import scrolledtext #ability to scroll through messages

# GUI setup
def gui_setup():
    window = tk.Tk()
    window.title("Chat Client")

    # Chat window
    chat_box = scrolledtext.ScrolledText(window, state='disabled') # can't edit text
    chat_box.pack(padx=10, pady=10) # layout

    # Message input
    input_box = tk.Entry(window, width=50)
    input_box.pack(padx=10, pady=10)

    # Function to send messages
    def send_message():
        message = input_box.get()

        if message.lower() == "quit":
            client.send("quit".encode('utf-8'))
            client.close()
            window.quit()  # Close the tkinter window
        else:
            client.send(message.encode('utf-8'))
            input_box.delete(0, tk.END)

    # Send button
    send_button = tk.Button(window, text="Send", command=send_message)
    send_button.pack(pady=10)

    return window, chat_box

# Function to receive messages
def receive_messages(chat_box):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            chat_box.config(state='normal')
            chat_box.insert(tk.END, message + '\n')
            chat_box.config(state='disabled')
        except:
            print("An error occurred!")
            client.close()
            break

# Client setup
server_host = '10.94.102.3'  # Localhost for testing
server_port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates TCP/IP socket
client.connect((server_host, server_port))

# Ask for nickname
nickname = input("Choose your nickname: ")
client.send(nickname.encode('utf-8'))

# Start GUI
window, chat_box = gui_setup()

# Start thread to receive messages
receive_thread = threading.Thread(target=receive_messages, args=(chat_box,))
receive_thread.start()

# Start Tkinter main loop
window.mainloop()
