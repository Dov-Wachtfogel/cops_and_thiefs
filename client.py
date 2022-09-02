import socket
import keyboard

IP = '127.0.0.1'
PORT = 12345


def move(side: str, s: socket.socket):
    s.send(('MOVE ' + side).encode())
    print(s.recv(128).decode())


def status(s: socket.socket):
    s.send('STATUS'.encode())
    print(s.recv(128).decode())


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    keyboard.add_hotkey('up', move, args=('UP', s))
    keyboard.add_hotkey('down', move, args=('DOWN', s))
    keyboard.add_hotkey('right', move, args=('RIGHT', s))
    keyboard.add_hotkey('left', move, args=('LEFT', s))
    keyboard.add_hotkey('s', status, args=[s])
    keyboard.wait('esc')


if __name__ == '__main__':
    main()
