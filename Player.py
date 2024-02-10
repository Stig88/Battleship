from Exceptions import LorenIpsumException
from random import randint
from moduls import Dot
import time

class Player:
    def __init__(self, p1_board, p2_board):
        self.p1_board = p1_board
        self.p2_board = p2_board

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                aim = self.ask()
                hod = self.p2_board.shot(aim)
                return hod
            except LorenIpsumException as e:
                print(e)

class AI(Player):
    def ask(self):
        random_xy = Dot(randint(0, 5), randint(0, 5))
        print(f"Залп компьютера по точке ({random_xy.x+1} {random_xy.y+1})")
        time.sleep(2)
        return random_xy

class User(Player):
    def ask(self):
        while True:
            xy = input('''Введите координаты в формате "строка"-"пробел"-"столбец": ''').split()

            if len(xy) != 2:
                print("Перепроверьте формат ввода")
                continue

            x = xy[0]
            y = xy[1]
            if not (x.isdigit()) or not (y.isdigit()):
                print("Введите, пожалуйста, числа! ")
                continue

            x = int(x)
            y = int(y)
            return Dot(x - 1, y - 1)