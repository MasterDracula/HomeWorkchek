class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.board = [["O"] * size for _ in range(size)]
        self.ships = []
        self.busy = []
        self.lives = 0


def __str__(self):
    board_view = "   | " + " | ".join(str(i) for i in range(1, self.size + 1)) + " |"
    for i in range(self.size):
        row = " | ".join(self.board[i])
        board_view += f"\n {chr(ord('A') + i)} | {row} |"
        print(board_view)