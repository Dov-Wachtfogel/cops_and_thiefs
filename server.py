import socket
from map_class import game_map

map_path = 'game_maps/randomwalls.bin'
PORT = 12345
s = socket.socket()
s.bind(('', PORT))
s.listen(5)
while True:
    c, addr = s.accept()
    play = True
    map = game_map(map_path)
    while play:
        command = c.recv(128).decode()
        if command == 'STATUS':
            c.send(map.status().encode())
        else:
            side = command[5:]
            try:
                ans = map.move_player(side)
            except:
                pass
            else:
                c.send(ans.encode())

