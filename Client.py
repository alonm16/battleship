import socket
FORMAT = 'utf-8'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

while True:
    msg = s.recv(2048).decode(FORMAT)
    if len(msg) <= 0:
        continue
    header, msg = msg[0], msg[1:]
    print(msg)
    if header == '1':
        to_send = input()
        s.send(bytes(to_send, FORMAT))


