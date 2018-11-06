import tensorflow as tf
import numpy as np
from keras import models
from keras import layers
from random import randint

from snake_game import SnakeGame, SnakeUI

class SnakeAi:
    TURN_LEFT = -1
    TURN_FORWARD = 0
    TURN_RIGHT = 1

    BAD = -1
    NORMAL = 0
    GOOD = 1

    def get_direction_for_action(self, direction, action):
        if action == SnakeAi.TURN_FORWARD: return direction
        elif action == SnakeAi.TURN_LEFT: return  [direction[1], -direction[0]]
        elif action == SnakeAi.TURN_RIGHT: return [-direction[1], direction[0]]
        else: raise Exception("Unexpected action: " + str(action))    
    
    def get_food_cosangle(self, game):
        snake_vec = np.array(game.direction)
        snake_vec_len = np.linalg.norm(snake_vec)
        head_vec = np.array(game.snake[0])
        food_vec = np.array(game.food) - head_vec
        food_vec_len = np.linalg.norm(food_vec)
        return np.dot(food_vec, snake_vec)/(food_vec_len * snake_vec_len)

    def get_food_dist(self, game):
        head_vec = np.array(game.snake[0])
        food_vec = np.array(game.food) - head_vec
        food_vec_len = np.linalg.norm(food_vec)
        return food_vec_len

    def observe(self, game):
        forward = game.direction
        left = self.get_direction_for_action(forward, SnakeAi.TURN_LEFT)
        right = self.get_direction_for_action(forward, SnakeAi.TURN_RIGHT)
        cosangle = self.get_food_cosangle(game)
        return [int(game.is_obstacle(left)), int(game.is_obstacle(forward)), int(game.is_obstacle(right)), cosangle]

    def get_random_action(self):
        i = randint(-1, 1)
        if i == -1: return SnakeAi.TURN_LEFT
        elif i == 0: return SnakeAi.TURN_FORWARD
        elif i == 1: return SnakeAi.TURN_RIGHT
        else: raise Exception("Unexpected value " + str(i))

    def generate_train_data(self):
        train_data = []
        train_labels = []
        
        game = SnakeGame(20, 20)
        for _ in range(1000):
            game.start()
            for _ in range(100):
                observations = self.observe(game)
                action = self.get_random_action()
                data = [action]
                data.extend(observations)
                train_data.append(data)

                direction = self.get_direction_for_action(game.direction, action)
                score = game.score
                food_distance = self.get_food_dist(game)
                
                game.turn(direction)

                if game.game_over:
                    train_labels.append(self.BAD)
                    break
                else:
                    if game.score > score or food_distance > self.get_food_dist(game):
                        train_labels.append(self.GOOD)
                    else:
                        train_labels.append(self.NORMAL)

        return (np.array(train_data), np.array(train_labels))

    def fit(self):
        train_data, train_labels = self.generate_train_data()
        hidden = 15
        model = models.Sequential()
        model.add(layers.Dense(hidden, activation='relu', input_dim=5))
        model.add(layers.Dense(1, activation='linear', input_dim=hidden))
        model.compile(optimizer='rmsprop', loss='mean_squared_error', metrics=['accuracy'])
        model.fit(train_data, train_labels, shuffle=True, validation_split=0.1, epochs=5)
        self.model = model

    def predict(self, game):
        observations = self.observe(game)

        left = [SnakeAi.TURN_LEFT]
        left.extend(observations)
        forward = [SnakeAi.TURN_FORWARD]
        forward.extend(observations)
        right = [SnakeAi.TURN_RIGHT]
        right.extend(observations)
        
        predictions = self.model.predict(np.array([left, forward, right]))
        
        action = np.argmax(np.array(predictions)) - 1
        direction = self.get_direction_for_action(game.direction, action)        
        return direction

if __name__ == "__main__":
    ai = SnakeAi()
    ai.fit()

    ui = SnakeUI()
    game = SnakeGame(20, 20)
    game.start()
    ui.run_game_loop(game, ai)