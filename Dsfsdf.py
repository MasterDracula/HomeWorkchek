def coordinate_system():
    # Обозначение системы координат
    i = input("Введите номер строки: ")
    if not i.isdigit():
        print("Это не число")
        coordinate_system()
    i = int(i)
    j = input("Введите номер столбца: ")
    if not j.isdigit():
        print("Это не число")
        coordinate_system()
    j = int(j)
    if 0 <= i and j < 3:
        coordinate_list = [i, j]
        return coordinate_list
    else:
        return print("Таких координат нет =("), coordinate_system()


def draw(board):
    # Проверка на ничью
    for row in board:
        if "-" in row:
            return False
    return True


def rematch():
    # Окончание игры
    go_on = input("Хотите начать новую партию? (да/нет): ") == "да"
    if go_on:
        game()
    else:
        print("Игра окончена!")


def win(board):
    # Проверка строк
    for row in range(len(board)):
        for col in range(len(board)-1):
            if board[row][col] == "-":
                break
            if board[row][col+1] == "-" or board[row][col] != board[row][col+1]:
                break
            if board[row+1][col] == "-" or board[row][col] != board[row+1][col]:
                break
        else:
            return True
# Проверка главной диагонали
    for cell in range(len(board)-1):
        if board[cell][cell] == "-" or board[cell+1][cell+1] == "-" or board[cell][cell] != board[cell+1][cell+1]:
            break
    else:
        return True
# Проверка второстепенной диагонали
    for cell in range(len(board)-1):
        emptyCell = board[cell][len(board)-cell-1] == "-" or board[cell+1][len(board)-cell-2] == "-"
        different = board[cell][len(board)-cell-1] != board[cell+1][len(board)-cell-2]
        if emptyCell or different:
            break
    else:
        return True
    return False


board = [["-", "-", "-"],
         ["-", "-", "-"],
         ["-", "-", "-"]]


def pole():
    # Вывод игрового поля
    for d in range(3):
        print(*board[d])


def game():
    # Основная функция игры
    print("--" * 20, "\nДобро пожаловать в игру крестики нолики!\n", "--" * 20)
    pole()
    print("Перед вами поле игры. "
          "\nДля того, чтобы поставить свой символ "
          "необходимо выбрать строку и столбец."
          "\nВыбор начинается с 0 и заканчивается 2")
    while True:
        list = coordinate_system()
        i = list[0]
        j = list[1]
        if board[i][j] != "-":
            print("Клетка занятна, выберите другую")
            coordinate_system()
        turn = 0
        if turn % 2 == 0:
            symbol = "x"
        else:
            symbol = "o"
        board[i][j] = symbol
        if win(board):
            pole()
            print(f"Конец игры. Победили {symbol}")
            break
        pole()
        if draw(board):
            pole()
            print("Ничья")
            break
        turn = turn + 1
    return False, rematch()


game()
