import socket
import threading
import sys

def read_msg(sock_cli):
    while True:
        data = sock_cli.recv(65535)
        if len(data) ==0:
            break
        print(data)

sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_client.connect(("127.0.0.1",6666))

sock_client.send(bytes(sys.argv[1], "utf-8"))

thread_client = threading.Thread(target=read_msg, args=(sock_client,))
thread_client.start()

while True:
    dest = input("Masukkan username tujuan (ketikkan bcast untuk broadcast):")
    msg = input("Masukkan pesan:")

    if msg == "exit":
        sock_client.close()
        break
    sock_client.send(bytes("{}|{}".format(dest, msg), "utf-8"))
