from Exceptions import BoardOutException, InvalidPlacementException, OverlapShotException, DoubleTapException

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    Type = {'1': 'Однопалубник', '2': 'Двухпалубник', '3': 'Трёхпалубник'}

    def __init__(self, ship_len, nose, direct):
        self.ship_len = ship_len
        self.life = ship_len
        self.nose = nose
        self.direct = direct

    @property
    def dots(self):
        _dots = []
        x = self.nose.x
        y = self.nose.y

        for i in range(self.ship_len):
            if self.direct:
                _dots.append(Dot(x, y+i))
            else:
                _dots.append(Dot(x+i, y))

        return _dots

    def shot(self, _shot):
        return _shot in self.dots

class Board:
    board_empty = 'O'
    board_ship = '■'
    board_killed = 'X'
    board_miss = 'T'
    board_contour = '*'

    def __init__(self, size, ship_hide=False):
        self.size = size
        self.ship_hide = ship_hide
        self.ships_online = []
        self.fields = [[self.board_empty] * self.size for _ in range(self.size)]
        self.fields_drawn = []
        self.kill_count = 0


    def add_ship(self, added_ship):
        for dot in added_ship.dots:
            if self.out(dot):
                raise BoardOutException
            elif dot in self.fields_drawn:
                raise InvalidPlacementException

        for dot in added_ship.dots:
            self.fields[dot.x][dot.y] = self.board_ship
            self.fields_drawn.append(dot)

        self.ships_online.append(added_ship)

        self.contour(added_ship)

    def contour(self, contoured_ship, dead=False):
        contour_coords = [[0,-1], [0, 1], [-1, 0], [1, 0], [-1, -1], [-1, 1], [1, -1], [1, 1]]

        for dot in contoured_ship.dots:
            for coord_x, coord_y in contour_coords:
                krasim = Dot(dot.x + coord_x, dot.y + coord_y)
                if not self.out(krasim) and krasim not in self.fields_drawn:
                    if dead:
                        self.fields[krasim.x][krasim.y] = self.board_contour
                    self.fields_drawn.append(krasim)

    def print_board(self):
        pole = '  '

        for i in range(1, self.size + 1):
            pole += f'{i}|'

        for i, j in enumerate(self.fields):
            pole += f'\n{i + 1}|' + '|'.join(j) + '|'

        if self.ship_hide:
            for i in pole:
                if i == self.board_ship:
                    pole = pole.replace(i, self.board_empty)

        return pole

    def out(self, check_dot):
        return not (0 <= check_dot.x < self.size and 0 <= check_dot.y < self.size)

    def shot(self, _shot):

        if self.out(_shot):
            raise BoardOutException

        if _shot in self.fields_drawn:
            if self.fields[_shot.x][_shot.y] == self.board_contour:
                raise OverlapShotException
            else:
                raise DoubleTapException

        for ship in self.ships_online:
            if _shot in ship.dots:
                self.fields[_shot.x][_shot.y] = self.board_killed
                self.fields_drawn.append(_shot)
                ship.life -= 1
                if ship.life == 0:
                    self.contour(ship, dead=True)
                    print(f'{Ship.Type[str(ship.ship_len)]} потоплен!')
                    self.kill_count +=1
                    return True
                else:
                    print('Корабль ранен!')
                    return True

        self.fields_drawn.append(_shot)
        self.fields[_shot.x][_shot.y] = self.board_miss
        print('Мимо!')
        return False

    def reset(self):
        self.fields_drawn = []
