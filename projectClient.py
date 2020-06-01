import socket


def main():
    # Creating connection with new server
    server = socket.socket()
    server.bind(("0.0.0.0", 5000))
    server.listen(5)
    while True:
        try:
            s, addr = server.accept()
            data = s.recv(1024).decode()
            s.send(data.encode())
        except:
            continue


if __name__ == '__main__':
    main()
