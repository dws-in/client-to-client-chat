import socket
import threading
import sys

BUFF_SIZE = 65535
friends = []

def read_msg(sock_cli):
    while True:
        data = sock_cli.recv(65535)
        if len(data) ==0:
            break
        print(data)

def add_friend(username_cli):
    friends.append(username_cli)
    print("SUCCESS! {} have been added as your friend.".format(username_cli))

def list_friend():
    print("List of friends:")
    for friend in friends:
        print(" - {}".format(friend))


sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_cli.connect(("127.0.0.1",6666))

sock_cli.send(bytes(sys.argv[1], "utf-8"))

thread_cli = threading.Thread(target=read_msg, args=(sock_cli,))
thread_cli.start()

while True:
    dest = input("Enter destination ('bcast' for broadcast):")
    msg = input("Enter message:")

    if msg == "exit":
        sock_cli.close()
        break

    if msg == "add":
        add_friend(dest)
        continue

    if msg == "list":
        list_friend()
        continue

    else:
        if dest not in friends:
            print("WARNING! {} is not recognized as your friend.".format(dest))
            continue
        
        sock_cli.send(bytes("{}|{}".format(dest, msg), "utf-8"))
