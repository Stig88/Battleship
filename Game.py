from Exceptions import LorenIpsumException, BoardOutException, InvalidPlacementException, DoubleTapException, OverlapShotException
from moduls import Board, Dot, Ship
from Player import User, AI
from random import randint
import time


class Game:
    def __init__(self, size=6):
        self.size = size
        user_board = self.random_board()
        ai_board = self.random_board()
        self.user_player = User(user_board, ai_board)
        self.ai_player = AI(ai_board, user_board)
        ai_board.ship_hide = True


    def random_board(self):

        rb = None
        while rb is None:
            rb = self.placement_gen()
            if len(rb.ships_online)<7:
                rb = None
            else:
                rb.reset()
                return rb

    def placement_gen(self):

        ships_sizes = [3, 2, 2, 1, 1, 1, 1]
        rb = Board(size=self.size)
        count = 0

        for ship_len in ships_sizes:
            while True:
                ship = Ship(ship_len, Dot(randint(0, self.size), randint(0, self.size)), randint(0, 1))
                try:
                    rb.add_ship(ship)
                    break
                except LorenIpsumException:
                    count += 1
                    if count == 100:
                        count = 0
                        break
                    else:
                        continue

        rb.reset()
        return rb

    def loop(self):
        hod_count = 0
        while True:
            print("****************"+"\n"+"Игровое поле юзера:"+"\n")
            print(self.user_player.p1_board.print_board() + "\n")
            print("****************"+"\n"+"Игровое поле робота:"+"\n")
            print(self.ai_player.p1_board.print_board() + "\n")

            if hod_count % 2 == 0:
                print("Ваш ход!")
                try:
                    hod = self.user_player.move()
                    time.sleep(1)
                    if hod:
                        hod_count += 1
                except LorenIpsumException as e:
                    print(e)

            else:
                print("Ход робота!")
                try:
                    hod = self.ai_player.move()
                    time.sleep(1)
                    if hod:
                        hod_count += 1
                except LorenIpsumException as e:
                    print(e)


            if self.ai_player.p1_board.kill_count == 7:
                print("ЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖ")
                print("     УРА ВЫ ПОБЕДИЛИ!")
                print("ЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖ")
                self.again()
                break

            if self.user_player.p1_board.kill_count == 7:
                print("               ЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖ")
                print("К сожалению, вы проиграли случайно стреляющему компьютеру.")
                print("               ЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖЖ")
                self.again()
                break

            hod_count += 1

    def start(self):
        self.greet()
        self.loop()

    def again(self):
        print("Заново? Введите '+', если да.")
        restart = input(": ")
        if restart=="+":
            user_board = self.random_board()
            ai_board = self.random_board()
            self.user_player = User(user_board, ai_board)
            self.ai_player = AI(ai_board, user_board)
            ai_board.ship_hide = True
            user_board.reset()
            ai_board.reset()
            self.loop()
        else:
            print("~~~~~~~~~~~~~~~~~")
            print("СПАСИБО ЗА ИГРУ!")
            print("~~~~~~~~~~~~~~~~~")

    def greet(self):
        print('''Добро пожаловать!
Поле 6х6, 4 однопалубника, 2 двухпалубника и 1 трёхпалубник. Корабли размещаются случайно, ровно как и производит выстрелы компьютер.

Гуд лак!

*по готовности, нажмите ENTER*''')
        input('')