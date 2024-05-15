from socket import AF_INET, socket, SOCK_STREAM, error as SocketError
from threading import Thread
import tkinter as tk

def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if msg:
                msg_list.insert(tk.END, msg)
        except SocketError as e:
            print("An error occurred while receiving messages:", e)
            break

def send(event=None):
    try:
        msg = my_msg.get()
        my_msg.set("")
        client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            client_socket.close()
            window.quit()
    except SocketError as e:
        print("An error occurred while sending the message:", e)
        client_socket.close()
        window.quit()

def on_closing(event=None):
    try:
        my_msg.set("{quit}")
        send()
    except SocketError as e:
        print("An error occurred while closing the window:", e)

window = tk.Tk()
window.title("Chat_Laboratory")

messages_frame = tk.Frame(window)
my_msg = tk.StringVar()
scrollbar = tk.Scrollbar(messages_frame)

msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tk.Entry(window, textvariable=my_msg)
entry_field.bind("<Return>", send)

entry_field.pack()
send_button = tk.Button(window, text="Send", command=send)
send_button.pack()

window.protocol("WM_DELETE_WINDOW", on_closing)

HOST = input('Enter the Server host: ')
PORT = input('Enter the port of the server host: ')

PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

try:
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive)
    receive_thread.start()
except SocketError as e:
    print("An error occurred while connecting to the server:", e)
    window.quit()

tk.mainloop()
