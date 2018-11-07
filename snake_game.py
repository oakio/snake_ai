import curses
from random import randint

class SnakeGame:
    UP = [0, -1]
    DOWN = [0, 1]
    LEFT = [-1, 0]
    RIGHT =[1, 0]

    def __init__(self, board_width, board_height, snake_len):
        self.board_width = board_width
        self.board_height = board_height
        self.snake_len = snake_len
    
    def start(self):
        self.score = 0
        self.game_over = False
        self.init_snake()
        self.init_food()

    def init_snake(self):
        self.snake = []
        self.direction = SnakeGame.UP
        for h in range(self.snake_len):
            self.snake.append([int(self.board_width/2), int(self.board_height/2) + h])

    def init_food(self): 
        food = []
        while food == []:
            food = [randint(0, self.board_width - 1), randint(0, self.board_height - 1)]
            if food in self.snake:
                food = []
        self.food = food

    def is_obstacle(self, direction):
        head = self.snake[0]
        x = head[0] + direction[0]
        y = head[1] + direction[1]
        if x < 0 or self.board_width <= x or y < 0 or self.board_height <= y:
            return True    

        move_to = [x, y]
        if move_to == self.food:
            return False
        
        return move_to in self.snake[1:-1]

    def turn(self, direction):
        if self.game_over:
            raise Exception("Game over")

        if self.is_obstacle(direction):
            self.game_over = True
            return
        
        head = self.snake[0]        
        x = head[0] + direction[0]
        y = head[1] + direction[1]
        move_to = [x, y]
            
        self.snake.insert(0, move_to)

        if move_to == self.food:
            self.score += 1
            self.init_food()
        else:
            self.snake.pop()
        
        self.direction = direction

class SnakeUI:
    def get_direction(self, key, game):
        direction = game.direction
        if key == -1: return direction
        elif key == curses.KEY_LEFT and direction != SnakeGame.RIGHT: return SnakeGame.LEFT
        elif key == curses.KEY_RIGHT and direction != SnakeGame.LEFT: return SnakeGame.RIGHT
        elif key == curses.KEY_UP and direction != SnakeGame.DOWN: return SnakeGame.UP
        elif key == curses.KEY_DOWN and direction != SnakeGame.UP: return SnakeGame.DOWN
        return direction

    def run_game_loop(self, game, ai):
        curses.initscr()
        win = curses.newwin(game.board_height + 2, game.board_width + 2, 0, 0)
        curses.curs_set(0)
        win.nodelay(True)
        win.timeout(200)
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
                game.game_over = True
            else:
                direction = self.get_direction(key, game) if ai == None else ai.predict(game)
                game.turn(direction)

        win.nodelay(False)    
        win.addstr(0, 2, "Game over: " + str(game.score))
        win.getch()
        curses.endwin()

if __name__ == "__main__":
    ui = SnakeUI()
    game = SnakeGame(20, 20, 5)
    game.start()
    ui.run_game_loop(game, None)