import math, random


class SudokuGenerator:

    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.board = [[0 for i in range(row_length)] for i in range(row_length)]
        self.box_length = int(self.row_length ** (1/2))

    def get_board(self):
        return self.board
            
    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) for num in row))

    def valid_in_row(self, row, num):
        for row1 in range(len(self.board)):
            if row1 == row:
                for num1 in self.board(row1):
                    if num1 == num:
                        return False
        return True

    def valid_in_col(self, col, num):
        for row in range(len(self.board)):
            if self.board[row][col] == num:
                return False
        return True

    def valid_in_box(self, row_start, col_start, num):
        for i in range(row_start, row_start + self.box_length):
            for j in range(col_start, col_start + self.box_length):
                if self.board[i][j] == num:
                    return False
        return True

    def is_valid(self, row, col, num):
        return (self.valid_in_row(row, num) and 
                self.valid_in_col(col, num) and 
                self.valid_in_box(row - row % self.box_length, 
                                col - col % self.box_length, num))

    def fill_box(self, row_start, col_start):
        used_values = []

        while len(used_values) < 9:

            for row in range(len(self.board[row_start]), len(self.board[row_start+3])):
                for col in range(len(self.board[row][col_start]), len(self.board[row][col_start+3])):
                    used_values.append(self.board[row][col])
            
            num = random.randit(1,9)

            if self.valid_in_box(self, row_start, col_start, num) and num not in used_values:
                self.board[row][col] == num
    
    def fill_diagonal(self):
        self.fill_box(0,0)
        self.fill_box(3,3)
        self.fill_box(6,6)

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True
        
        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    def remove_cells(self):
        row = random.randint(0,9)
        col = random.randint(0,9)

        if self.board[row][col] != 0:
            self.board[row][col] == 0


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    board = sudoku.get_board()
    sudoku.remove_cells()
    board = sudoku.get_board()
    return board

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
    
        

