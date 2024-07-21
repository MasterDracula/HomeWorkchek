class Dot:
    # Класс точки
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    # Класс кораблей
    def __init__(self, lenth, bow, direction):
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
    def __init__(self, size = 6, shipslist = 7, hid=False, aliveship=None):
        self.size = size
        self.shipslist = shipslist
        self.hid = hid
        self.aliveship = aliveship

    def shot(self, dot):
        if dot not in





class BoardOutException(Exception):
    pass
    # исключение ошибки, когда координаты за пределами доски

class BoardUsedException(Exception):
    pass
    # исключение ошибки, когда координаты используются