import pygame
import math

ROWS = 10
WIDTH = 600
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hop Draw")
GAP_SIZE = 1
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BD_COL = (150, 50, 100)

class Board:
    def __init__(self, size, WIDTH):
        self.grid = [[-1 for _ in range (size)] for _ in range (size)]
        self.size = size
        self.cell_size = WIDTH//size
        self.cnt_saves = 0
        self.nspace = 2

    def get_pos(self, pos):
        y, x = pos
        row = y // self.cell_size
        col = x // self.cell_size
        return col, row

    def make_black(self, pos):
        row, col = self.get_pos(pos)
        self.grid[row][col] = 1

    def make_white(self, pos):
        row, col = self.get_pos(pos)
        self.grid[row][col] = -1

    def redraw(self, win):
        #background
        pygame.draw.rect(win, BD_COL, (0, 0, WIDTH, HEIGHT))
        #grid
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[y][x] == 1:
                    pygame.draw.rect(win, BLACK, (x*self.cell_size + GAP_SIZE, y*self.cell_size  + GAP_SIZE, self.cell_size - 2 * GAP_SIZE, self.cell_size - 2 * GAP_SIZE))
                else:
                    pygame.draw.rect(win, WHITE,
                                     (x * self.cell_size + GAP_SIZE, y * self.cell_size  + GAP_SIZE, self.cell_size - 2 * GAP_SIZE, self.cell_size - 2 * GAP_SIZE))
        pygame.display.update()

    def reset(self):
        for x in range(self.size):
            for y in range(self.size):
                self.grid[x][y] = -1

    @staticmethod
    def num_space(num):
        if 0 <= num <= 9:
            return " " + str(num)
        return str(num)

    def save_board(self):
        s = "["
        e = "]"
        delim = ", "

        with open('patterns.txt', 'a') as f:
            # string = f"Pat{self.cnt_saves} = " + s + "\n"
            string = f"patterns.append(" + s + "\n"
            self.cnt_saves += 1
            for row in self.grid:
                string += "\t" + s
                for i, elem in enumerate(row):
                    string += self.num_space(elem)
                    if i < len(row) - 1:
                        string += delim
                    else:
                        string += e + ",\n"
            string += e + ")\n\n"
            f.write(string)



def main(WIN, WIDTH):

    board = Board(ROWS, WIDTH)
    clock = pygame.time.Clock()

    run = True

    while run:
        clock.tick(75)
        board.redraw(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: #LEFT
                pos = pygame.mouse.get_pos()
                board.make_black(pos)
            elif pygame.mouse.get_pressed()[2]: #RIGHT
                pos = pygame.mouse.get_pos()
                board.make_white(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    board.save_board()

                if event.key == pygame.K_r:
                    board.reset()

    pygame.quit()


if __name__ == "__main__":
    main(WIN, WIDTH)
