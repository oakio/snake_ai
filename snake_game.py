import curses
from random import randint

class SnakeGame:
    UP = [0, -1]
    DOWN = [0, 1]
    LEFT = [-1, 0]
    RIGHT =[1, 0]

    def __init__(self, board_width, board_height):
        self.board_width = board_width
        self.board_height = board_height
    
    def start(self):
        self.score = 0
        self.game_over = False
        self.init_snake()
        self.init_food()

    def init_snake(self):
        self.snake = []
        self.direction = [0, -1]
        for h in range(3):
            self.snake.append([int(self.board_width/2), int(self.board_height/2) + h])

    def init_food(self): 
        food = []
        while food == []:
            food = [randint(0, self.board_width - 1), randint(0, self.board_height - 1)]
            if food in self.snake:
                food = []
        self.food = food

    def turn(self, direction):
        if self.game_over:
            raise Exception("Game over")

        head = self.snake[0]        
        x = head[0] + direction[0]
        y = head[1] + direction[1]
        move_to = [x, y]

        if x < 0 or self.board_width <= x or y < 0 or self.board_height <= y or move_to in self.snake[1:-1]:
            self.game_over = True
            return
            
        self.snake.insert(0, move_to)

        if move_to == self.food:
            self.score += 1
            self.init_food()
        else:
            self.snake.pop()
        
        self.direction = direction

def get_direction(key):        
    if key == curses.KEY_LEFT and game.direction != game.RIGHT: return game.LEFT
    elif key == curses.KEY_RIGHT and game.direction != game.LEFT: return game.RIGHT
    elif key == curses.KEY_UP and game.direction != game.DOWN: return game.UP
    elif key == curses.KEY_DOWN and game.direction != game.UP: return game.DOWN
    return game.direction

def run_game_loop(game):
    curses.initscr()
    win = curses.newwin(game.board_height + 2, game.board_width + 2, 0, 0)
    curses.curs_set(0)
    win.nodelay(True)
    win.timeout(300)
    win.keypad(True)

    while game.game_over == False:
        win.clear()
        win.border(0)
        win.addstr(0, 2, "Score: " + str(game.score))
        win.addch(game.food[1] + 1, game.food[0] + 1, '$')
        for i, point in enumerate(game.snake):
            win.addch(point[1] + 1, point[0] + 1, '@' if i == 0 else "+")
        
        key = win.getch()
    
        if key == ord('q'):
            break
        elif key == -1:
            game.turn(game.direction)
        else:        
            action = get_direction(key)    
            game.turn(action)

    win.nodelay(False)    
    win.addstr(0, 2, "Game over: " + str(game.score))
    win.getch()
    curses.endwin()

if __name__ == "__main__":
    game = SnakeGame(20, 20)
    game.start()
    run_game_loop(game)