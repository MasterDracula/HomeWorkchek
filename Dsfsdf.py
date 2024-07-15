def start():
    # приветствие и занкомство
    print("--" * 20, "\nДобро пожаловать в игру крестики нолики!\n", "--" * 20,
          "\nДля начала давайте познакомимся")
    First_player = input("Первый игрок введите ваше имя: ")
    print(F"Привет {First_player}! \nДавайте теперь узнаем,"
          F"как зовут вашего оппонента?")
    Second_player = input("Введите Ваше имя: ")
    print(F"Привет {Second_player}!"
          F"{First_player} играет крестиками, а {Second_player} играет ноликами!")
    return game()


def coordinate_system():
    # Обозначение системы координат
    i = int(input("Введите номер строки: "))
    j = int(input("Введите номер столбца: "))
    if 0 <= i and j < 3:
        coordinate_list = [i, j]
        return coordinate_list
    else:
        return print("Таких координат нет =("), coordinate_system()


def draw(map):
    # Проверка на ничью
    for row in map:
        if "-" in row:
            return True
    return print("Ничья"), game_over()


def game_over():
    # Окончание игры
    go_on = False
    go_on = input("Хотите начать новую партию? (да/нет): ") == "да"
    while go_on:
        game()
    else:
        print("Игра окончена!")


def win(map):
    # Проверка строк
    for row in range(len(map)):
        for col in range(len(map)-1):
            if map[row][col] == "-" or map[row][col+1] == "-" or map[row][col] != map[row][col+1]:
                break
        else:
            return True
# Проверка столбцов
    for col in range(len(map)):
        for row in range(len(map)-1):
            if map[row][col] == "-" or map[row+1][col] == "-" or map[row][col] != map[row+1][col]:
                break
        else:
            return True
# Проверка главной диагонали
    for cell in range(len(map)-1):
        if map[cell][cell] == "-" or map[cell+1][cell+1] == "-" or map[cell][cell] != map[cell+1][cell+1]:
            break
    else:
        return True
# Проверка второстепенной диагонали
    for cell in range(len(map)-1):
        emptyCell = map[cell][len(map)-cell-1] == "-" or map[cell+1][len(map)-cell-2] == "-"
        different = map[cell][len(map)-cell-1] != map[cell+1][len(map)-cell-2]
        if emptyCell or different:
            break
    else:
        return True
    return False


def game():
    # Основная функция игры
    go_on = True
    map = [["-", "-", "-"],
           ["-", "-", "-"],
           ["-", "-", "-"]
           ]

    def pole():
        # Вывод игрового поля
        for i in range(3):
            print(*map[i])
    pole()
    print("Перед вами поле игры. "
          "\nДля того, чтобы поставить свой символ "
          "необходимо выбрать строку и столбец."
          "\nВыбор начинается с 0 и заканчивается 2")
    while go_on:
        list = coordinate_system()
        i = list[0]
        j = list[1]
        if map[i][j] != "-":
            print("Клетка занятна, выберите другую")
            coordinate_system()
        turn = 0
        if turn % 2 == 0:
            symbol = "x"
            turn += 1
        else:
            symbol = "o"
            turn += 1
        map[i][j] = symbol
        if win(map):
            pole()
            print(f"Конец игры. Победили {symbol}")
            break
        pole()
        draw(map)
    return game_over()


start()
