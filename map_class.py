import random


class game_map:
    def __init__(self, file_path):
        f = open(file_path, 'rb')
        m = f.read()
        f.close()
        map_len = int(m[0])
        self.map_table = [[int(c) for c in m[n:n + map_len]] for n in range(1, len(m), map_len)]
        self.t_loc, self.c_loc, self.x_loc = self._random_free_loc(), self._random_free_loc(), self._random_free_loc()
        self.running = True

    def _random_free_loc(self):
        x, y = random.randint(0, len(self.map_table) - 1), random.randint(0, len(self.map_table[0]) - 1)
        if not self.free_loc([x, y]):
            return self._random_free_loc()
        return [x, y]

    def move_player(self, side):
        if not self.running:
            return None
        wall = False
        if side == 'UP':
            if self.free_loc([self.t_loc[0] - 1, self.t_loc[1]]):
                self.t_loc[0] -= 1
            else:
                wall = True
        if side == 'DOWN':
            if self.free_loc([self.t_loc[0] + 1, self.t_loc[1]]):
                self.t_loc[0] += 1
            else:
                wall = True
        if side == 'RIGHT':
            if self.free_loc([self.t_loc[0], self.t_loc[1] + 1]):
                self.t_loc[1] += 1
            else:
                wall = True
        if side == 'LEFT':
            if self.free_loc([self.t_loc[0], self.t_loc[1] - 1]):
                self.t_loc[1] -= 1
            else:
                wall = True
        if self.t_loc == self.x_loc:
            self.running = False
            return 'WON'
        if self.t_loc == self.c_loc:
            self.running = False
            return 'LOSE'
        self._move_cop()
        if self.t_loc == self.c_loc:
            self.running = False
            return 'LOSE'
        if wall:
            return 'WALL'
        return 'OK'

    def free_loc(self, loc):
        if loc[0] < 0 or loc[0] > len(self.map_table) or loc[1] < 0 or loc[1] > len(self.map_table[0]):
            return False
        if self.map_table[loc[0]][loc[1]] != 0:
            return False
        return True

    def _move_cop(self):
        a, b = random.randint(-1, 1), random.randint(-1, 1)
        if (a == 0 and b == 0) or not self.free_loc([self.c_loc[0] + a, self.c_loc[1] + b]):
            self._move_cop()
        else:
            self.c_loc = [self.c_loc[0] + a, self.c_loc[1] + b]

    def __str__(self):
        str_table = [[str(a).replace('0', ' ').replace('1', '*') for a in r] for r in self.map_table]
        str_table[self.c_loc[0]][self.c_loc[1]] = 'C'
        str_table[self.t_loc[0]][self.t_loc[1]] = 'T'
        str_table[self.x_loc[0]][self.x_loc[1]] = 'X'
        txt = ''
        for r in str_table:
            for l in r:
                txt += l
            txt += '\n'
        return txt[:-1:]

    def status(self):
        print(self)
        if self._near(self.t_loc, self.c_loc):
            return 'COP NEAR'
        if self._near(self.t_loc, self.x_loc):
            return 'TREASURE NEAR'
        return 'GAME ON'

    @staticmethod
    def _near(loc1, loc2):
        if loc1[0] == loc2[0] and abs(loc1[1] - loc2[1]) == 1:
            return True
        if loc1[1] == loc2[1] and abs(loc1[0] - loc2[0]) == 1:
            return True
        return False
