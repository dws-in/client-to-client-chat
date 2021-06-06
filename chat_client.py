import socket
import threading
import sys

BUFF_SIZE = 65535
MY_USERNAME = sys.argv[1]
friends = []

def read_msg(sock_cli):
    while True:
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break
        print(data)

def add_friend(username_cli):
    friends.append(username_cli)
    print("SUCCESS! {} have been added as your friend.".format(username_cli))

def list_friend():
    print("List of friends:")
    for friend in friends:
        print(" - {}".format(friend))

def list_user():
    sock_cli.send(bytes("user|list", "utf-8"))
    print("List of users:")
    data = sock_cli.recv(65535)
    data.replace('\'', '')
    data.replace('[', '')
    data.replace(']', '')
    data.replace(' ', '')
    print(data)


sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_cli.connect(("127.0.0.1",6666))

sock_cli.send(bytes(MY_USERNAME, "utf-8"))

thread_cli = threading.Thread(target=read_msg, args=(sock_cli,))
thread_cli.start()

while True:
    dest = input("Enter destination ('bcast' for broadcast): ")
    msg = input("Enter message: ")

    if msg == "exit":
        sock_cli.close()
        break

    if msg == "add":
        add_friend(dest)
        continue

    elif dest == "friend" and msg == "list":
        list_friend()
        continue

    elif dest == "user" and msg == "list":
        list_user()
        continue

    else:
        if dest not in friends and dest != "":
            print("WARNING! {} is not recognized as your friend.".format(dest))
            continue
        
        sock_cli.send(bytes("{}|{}".format(dest, msg), "utf-8"))

