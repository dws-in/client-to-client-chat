import socket
import threading
import sys
import pickle
import os

BUFF_SIZE = 65535
MY_USERNAME = sys.argv[1]
friends = []

def read_msg(sock_cli, stop):
    while True:
        if stop():
            break
        data = sock_cli.recv(65535)

        # Pickle data
        if pickle.loads(data):
            data = pickle.loads(data)

        # String data
        else:
            data = data.decode("utf-8")
            print(data)
            
        if len(data) == 0:
            break

sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_cli.connect(("127.0.0.1",6666))

sock_cli.send(bytes(MY_USERNAME, "utf-8"))

stop_threads = False
thread_cli = threading.Thread(target=read_msg, args=(sock_cli, lambda : stop_threads, ))
thread_cli.start()

# Add bcast as initial friend
friends.append("bcast")

while True:
    try:
        msg = input("Message: ")
        dest = input("Destination: ")

        # Exit
        if msg == "exit":
            sock_cli.close()
            break

        # Add friend
        elif msg == "add":
            friends.append(dest)
            print("SUCCESS! {} has been added as your friend.".format(dest))
            continue

        elif msg == "list":
            # Get friends list
            if dest == "friends":
                print(friends)

            # Get users list
            elif dest == "bcast":
                sock_cli.send(bytes("{}|{}".format(dest, msg), "utf-8"))

            else:
                print("FAILED! Wrong destination.")
            continue

        # Send file
        elif msg == "file":
            file = input("File: ")
            file_path = os.path.join(os.getcwd(),file)
            pickle_path = os.path.join(os.getcwd(),"input.pkl")

            print(file_path)
            with open(file_path, 'wb') as f:
                payload = pickle.dumps(f)
                data = bytes("{}|{}|".format(dest, msg), 'utf-8')
                data = b"".join([data, payload])
                print(data)
                # sock_cli.send(data)
            continue

        else:
            if dest not in friends and dest != "":
                print("WARNING! {} is not recognized as your friend.".format(dest))
                continue
            
            sock_cli.send(bytes("{}|{}".format(dest, msg), "utf-8"))

    except KeyboardInterrupt:
        # Stop thread
        stop_threads = True
        thread_cli.join()

        # Close connection
        if sock_cli:
            sock_cli.close()
        break

