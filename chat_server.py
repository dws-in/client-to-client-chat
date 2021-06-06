import socket
import threading

is_done = False
BUFF_SIZE = 65535

def read_msg(clients, sock_cli, addr_cli, username_cli):
    while True:
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break

        dest, msg = data.decode("utf-8")
        msg = "<{}>: {}".format(username_cli, msg)

        if dest == "bcast":
            send_broadcast(clients, msg, addr_cli)
        else:
            dest_sock_cli = clients[dest][0]
            send_msg(dest_sock_cli, msg)
        print(data)

    sock_cli.close()
    print("Connection closed", addr_cli)

def send_broadcast(clients, data, sender_addr_cli):
    for sock_cli, addr_cli, _ in clients.values():
        if not (sender_addr_cli[0] == addr_cli[0] and sender_addr_cli[1] == addr_cli[1]):
            send_msg(sock_cli, data)

def send_msg(sock_cli, data):
    sock_cli.send(bytes(data, "utf-8"))

sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_server.bind(("0.0.0.0", 6666))
sock_server.listen(5)

clients = {}

while True:
    sock_cli, addr_cli = sock_server.accept()

    username_cli = sock_cli.recv(65535).decode("utf-8")
    print(username_cli, " joined")

    thread_cli = threading.Thread(target=read_msg, args=(clients, sock_cli, addr_cli, username_cli))
    thread_cli.start()

    clients["{}".format(username_cli)] = (sock_cli, addr_cli, thread_cli)