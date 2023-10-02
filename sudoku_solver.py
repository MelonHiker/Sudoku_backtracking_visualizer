import pygame
pygame.init()

DELAY = 100

WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Backtracking Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
INDIAN_RED = (205, 92, 92)
WHITE_GRAY = (220, 220, 220)
BLACK = (0, 0, 0)
SEA_GREEN = (84, 255, 159)

class Sudoku:
    def __init__(self, width, height, board):
        self.width = width
        self.height = height
        self.solved = False

        self.board = [[Cube(width / 9, height / 9) for _ in range(9)] for _ in range(9)]
        self.rows = [[False for _ in range(10)] for _ in range(9)]
        self.cols = [[False for _ in range(10)] for _ in range(9)]
        self.boxes = [[False for _ in range(10)] for _ in range(9)]
        self.spaces = []
        for i in range(9):
            for j in range(9):
                if (board[i][j].isnumeric() == False):
                    self.spaces.append((i, j))
                    continue
                
                num = int(board[i][j])
                if (num < 1 or num > 9):
                    continue

                self.board[i][j].num = num
                self.board[i][j].color = WHITE_GRAY
                self.rows[i][num] = True
                self.cols[j][num] = True
                self.boxes[(i//3)*3 + j//3][num] = True
    
    def draw(self):
        WIN.fill(WHITE)
        for i in range(9):
            for j in range(9):
                self.board[i][j].draw(j * (self.width / 9), i * (self.height / 9))

        for i in range(1, 9):
            thick = 2 if i % 3 else 4
            pygame.draw.line(WIN, BLACK, (0, i * (self.height / 9)), (self.width, i * (self.height / 9)), thick)
            pygame.draw.line(WIN, BLACK, ((i * (self.width / 9)), 0), (i * (self.width / 9), self.height), thick)

        pygame.display.update()

    def fill_num(self, i, j, num, color):
        self.board[i][j].num = num
        self.board[i][j].color = color
        self.rows[i][num] = True
        self.cols[j][num] = True
        self.boxes[(i//3)*3 + j//3][num] = True

    def clear_num(self, i, j):
        num = self.board[i][j].num
        self.board[i][j].num = None
        self.board[i][j].color = None
        self.rows[i][num] = False
        self.cols[j][num] = False
        self.boxes[(i//3)*3 + j//3][num] = False

    def complete(self):
        for i in range(9):
            for j in range(9):
                self.board[i][j].color = SEA_GREEN
        self.solved = True
        self.draw()

    def solver(self, pos=0):
        pygame.event.pump()
        
        if pos == len(self.spaces):
            self.complete()
            return True
        
        i, j = self.spaces[pos]
        for num in range(1, 10):
            if (self.rows[i][num] or self.cols[j][num] or self.boxes[(i//3)*3 + j//3][num]):
                continue

            self.fill_num(i, j, num, BLUE)
            self.draw()
            
            if wait_for(DELAY) or self.solver(pos + 1):
                return True
            
            self.board[i][j].color = INDIAN_RED
            self.draw()

            if wait_for(DELAY):
                return True
            
            self.clear_num(i, j)

        return False


class Cube:
    def __init__(self, width, height, num=None, color=None):
        self.width = width
        self.height = height
        self.num = num
        self.color = color

    def draw(self, x, y):
        if self.num and self.color:
            cube_rect = pygame.Rect(x, y, self.width + 2, self.height + 2)
            pygame.draw.rect(WIN, self.color, cube_rect)
            
            font = pygame.font.SysFont("comicsans", int(min(self.width, self.height)*0.6))
            text = font.render(str(self.num), True, BLACK)
            WIN.blit(text, (x + self.width / 3, y + self.height / 14))


def wait_for(milliseconds):
    cur_time = pygame.time.get_ticks()
    finish_time = cur_time + milliseconds

    while cur_time < finish_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        pygame.time.wait(milliseconds // 10)    
        cur_time = pygame.time.get_ticks()


def main():
    board = [
    ["7","4","5","6",".","2","3","8","."],
    ["2","1",".","9","5","8","6","7","."],
    [".",".","9",".",".",".","1","5","."],
    [".",".",".","2",".","1",".","9","7"],
    [".","7",".",".","3","5",".",".","6"],
    [".",".","4",".",".",".",".","2","."],
    ["3","2",".",".",".",".",".","6","."],
    ["4",".","6",".","2","9",".",".","."],
    [".",".",".","3",".",".",".",".","5"]
    ]

    while True:
        sudoku = Sudoku(WIDTH, HEIGHT, board)
        sudoku.solver()
        if (sudoku.solved == False):
            break

        pygame.time.wait(1000)

    pygame.quit()


if __name__ == "__main__":
    main()