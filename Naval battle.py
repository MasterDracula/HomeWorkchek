from random import randint
import time


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    pass
    # исключение ошибки, когда координаты за пределами доски


class BoardUsedException(BoardException):
    pass
    # исключение ошибки, когда координаты используются


class BoardWrongShipException(BoardException):
    pass


class Dot:
    # Класс точки
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    # Класс кораблей
    def __init__(self, bow, lenth, rotation):
        self.bow = bow
        self.lenth = lenth
        self.rotation = rotation
        self.hp = lenth

    @property
    def dots(self):
        # Возвращение точек, которые занимает корабль
        ship_dots = []
        for i in range(self.lenth):
            bow.x = self.bow_x
            bow.y = self.bow_y

            if self.rotation == 0:
                bow.x += 1

            if self.rotation == 1:
                bow.y += 1
            ship_dots.append(Dot(bow.x, bow.y))
        return ship_dots


class Board:
    # Создание доски и определение её свойств
    def __init__(self, size=6, hid=False):
        self.size = size
        self.hid = hid
        self.busy = []
        self.board = [["."] * size for _ in range(size)]
        self.shipalive = 0

    def boardout(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def add_ship(self, ship):
        # Добавление корабля на карту
        for dot in ship.dots:
            if self.boardout(dot) or dot in self.busy:
                raise BoardOutException()
        for dot in ship.dots:
            self.board[dot.x][dot.y] = "■"
            self.busy.append(dot)
        self.ships.append(ship)
        self.shipalive += 1
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        for dot in ship.dots:
            for dx, dy in near:
                cont = Dot(dot.x + dx, dot.y + dy)
                if not (self.out(cont)) and cont not in self.busy:
                    if verb:
                        self.board[cont.x][cont.y] = "*"
                    self.busy.append(cont)

    def shot(self, dot):
        # Выстрел в корабль
        if self.boardout(dot):
            raise BoardOutException()

        if dot in self.busy:
            raise BoardUsedException()

        self.busy.append(dot)

        for ship in self.ships:
            if dot in ship.dots:
                ship.hp -= 1
                self.board[dot.x][dot.y] = "x"
                if ship.hp == 0:
                    self.contour(ship, verb=True)
                    time.sleep(2)
                    self.shipalive -= 1
                    f"Корабль уничтожен. Осталось {self.shipalive} кораблей"
                    return False
                else:
                    time.sleep(2)
                    f"Вижу дым на горизонте! Попадание!"
                    return True
        self.board[dot.x][dot.y] = "●"
        time.sleep(2)
        print("Было близко, но мы промахнулись!")
        return False

    def show_board(self):
        # Создание границ поля, для ориентирования на нем
        front_board = ""
        front_board += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            front_board += f"\n{chr(ord('A') + i)} | " + " | ".join(row) + " |"


class Main:
    # установка основных параметров самой игры

    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        # расстановка кораблей на поле - случайним методом
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts_random = 0
        for lenth in lens:
            while True:
                attempts_random += 1
                if attempts_random > 500:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), lenth, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException():
                    pass
        board.begin()
        return board

    def game(self):
        # основной игровой цикл
        print('-' * 20, '\nДобро пожаловать в игру Морской бой!\n', '-' * 20)
        time.sleep(2)
        print('Капитан вражеский флот на горизонте!'
              'Нам необходимы 2 координаты (через пробел) для выстрела:'
              '- номер строки и номер столбца! Скорее капитан.')
        num = 0
        while True:
            print('-' * 20)
            print('Доска Пользователя:')
            time.sleep(2)
            print(self.us.board)
            print('-' * 20)
            print('Доска Компьютера:')
            time.sleep(2)
            print(self.ai.board)
            time.sleep(2)
            if num % 2 == 0:
                print('-' * 20)
                time.sleep(1)
                print('Капитан, куда стрелять? (введите Ряд и Столбец через пробел): ')
                time.sleep(2)
                repeat = self.us.move()
            else:
                print('-' * 20)
                time.sleep(1)
                print('Ход Компьютера:  ')
                time.sleep(2)
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.shipalive == 0:
                print('-' * 20)
                time.sleep(2)
                print('Капитан, мы выйграли!')
                break

            if self.us.board.shipalive == 0:
                print('-' * 20)
                time.sleep(2)
                print('Наш флота потопили, мы проиграли!')
                break
            num += 1

    def start(self):
        self.game()


class Player:
    # основные взаимодействия Пользователя и Компьютера (противника)
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    # дочерний класс - Игрок ИИ
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        time.sleep(2)
        print(f'Компьютер пошёл так: {d.x + 1} {d.y + 1}')
        return d


class User(Player):
    # дочерний класс - Игрок Пользователь
    def ask(self):
        while True:
            cords = input('Ваш ход: ').split()

            if len(cords) != 2:
                print(' Внимание! Введите ИМЕННО 2 координаты! ')
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isalpha()):
                print(' Таких координат нет =( ')
                continue

            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


m = Main()
m.start()
