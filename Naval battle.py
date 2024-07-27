import random


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
        self.board = [["| |"] * size for _ in range(size)]
        self.shipsunk = 0
        self.shipalive = 7

    class BoardOutException(Exception):
        pass
        # исключение ошибки, когда координаты за пределами доски

    class BoardUsedException(Exception):
        pass
        # исключение ошибки, когда координаты используются

    def boardout(self, dot):
        return not ((0 <= dot.x < self.size) and (0 <= dot.y < self.size))

    def add_ship(self, ship):
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
                    self.shipsunk += 1
                    self.shipalive -= 1
                    print(f"Корабль уничтожен. Осталось {self.shipalive} кораблей")
                    return False
                else:
                    return True, "Вижу дым на горизонте! Попадание!"
        self.board[dot.x][dot.y] = "●"
        return False, "Было близко, но мы промахнулись!"

    def show_board(self):
