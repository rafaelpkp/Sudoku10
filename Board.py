from Cell import Cell
import pygame

class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.cells = [[Cell(0, i, j, screen) for j in range(9)] for i in range(9)]
        self.selected_cell = None

    def draw(self):
        # Draw grid lines
        for i in range(10):
            if i % 3 == 0:
                thickness = 4
            else:
                thickness = 1
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * 60), (self.width, i * 60), thickness)
            pygame.draw.line(self.screen, (0, 0, 0), (i * 60, 0), (i * 60, self.height), thickness)

        # Draw cell values
        for i in range(9):
            for j in range(9):
                self.cells[i][j].draw()

    def select(self, row, col):
        if self.selected_cell:
            self.cells[self.selected_cell[0]][self.selected_cell[1]].selected = False
        self.selected_cell = (row, col)
        self.cells[row][col].selected = True

    def click(self, x, y):
        if x < self.width and y < self.height:
            row = y // 60
            col = x // 60
            return (row, col)
        return None

    def clear(self):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.cells[row][col].editable:
                self.cells[row][col].set_cell_value(0)
                self.cells[row][col].set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.cells[row][col].editable:
                self.cells[row][col].set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.cells[row][col].editable:
                self.cells[row][col].set_cell_value(value)

    def reset_to_original(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].editable:
                    self.cells[i][j].set_cell_value(0)
                    self.cells[i][j].set_sketched_value(0)

    def is_full(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value == 0:
                    return False
        return True

    def update_board(self):
        pass

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value == 0:
                    return (i, j)
        return None

    def check_board(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value != self.solution[i][j]:
                    return False
        return True
