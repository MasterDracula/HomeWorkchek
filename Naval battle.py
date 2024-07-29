from random import randint
import time

print('-'*20, '\nДобро пожаловать в игру Морской бой!\n', '-'*20)
time.sleep(2)
print('Пользователь играет с Компьютером - и ходит Первым!'
      'вводим через пробел 2 координаты:'
      '- номер строки и номер столбца.')


class Dot:
    # Класс точки
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    # Класс кораблей
    def __init__(self, lenth, bow, rotation):
        self.lenth = lenth
        self.bow = bow
        self.rotation = rotation
        self.hp = lenth

    @property
    def dots(self):
        # Возвращение точек, которые занимает корабль
        ship_dots = []
        for i in range(self.lenth):
            dot_x = self.bow_x + i * direction[0]
            dot_y = self.bow_y + i * direction[1]
            ship_dots.append(Dot(dot_x, dot_y))
        return ship_dots


class Board:
    # Создание доски и определение её свойств
    def __init__(self, size=6, hid=False):
        self.size = size
        self.hid = hid
        self.busy = []
        self.board = [["."] * size for _ in range(size)]
        self.shipsunk = 0
        self.shipalive = 7

    class BoardOutException(Exception):
        pass
        # исключение ошибки, когда координаты за пределами доски

    class BoardUsedException(Exception):
        pass
        # исключение ошибки, когда координаты используются

    class BoardWrongShipException(BoardException):
        pass

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
        self.lives += ship.length
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
        elif dot in self.busy:
            raise BoardUsedException()
        self.busy.append(dot)
        for ship in self.ships:
            if dot in ship.dots:
                ship.hp -= 1
                self.board[dot.x][dot.y] = "x"
                if ship.hp == 0:
                    self.hp -= ship.length
                    self.contour(ship, verb=True)
                    time.sleep(2)
                    self.shipsunk += 1
                    self.shipalive -= 1
                    print(f"Корабль уничтожен. Осталось {self.shipalive} кораблей")
                    return False
                else:
                    time.sleep(2)
                    f"Вижу дым на горизонте! Попадание!"
                    return True
        self.board[dot.x][dot.y] = "●"
        time.sleep(2)
        return False, "Было близко, но мы промахнулись!"

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
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def game(self):
        # основной игровой цикл
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
                print('Ход Пользователя - введите Ряд и Столбец через пробел')
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

            if self.ai.board.count == 7:
                print('-' * 20)
                time.sleep(2)
                print('Пользователь Выиграл!')
                break

            if self.us.board.count == 7:
                print('-' * 20)
                time.sleep(2)
                print('Компьютер Выиграл!')
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
        time.sleep(3)
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
