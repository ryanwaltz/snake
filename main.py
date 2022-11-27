import time
import random
import math
import pygame


class Apple:
    def __init__(self, x=False, y=False):
        possible_squares = []
        self.color = (255, 0, 0)  # red
        self.position = None
        if x is False:
            for square in squares:
                if square.type == "unoccupied":
                    possible_squares.append([square.x, square.y])
            self.position = random.choice(possible_squares)
        else:
            self.position = [x*20, y*20]
        for square in squares:
            if self.position == [square.x, square.y]:
                square.type = "occupied"
                square.specific_type = 2
                square.color = self.color
                self.square = square
                break

    def delete(self):
        apples.remove(self)


class Square:
    def __init__(self, x, y, color=(0,0,0), block_type="unoccupied", specific_type=0):  # 0 = unoccupied, 1 = snake, 2 = apple, 3 = block, 4 = snakehead
        self.x = x
        self.y = y
        self.size = 20
        self.color = color  # black and unoccupied
        self.type = block_type
        self.specific_type = specific_type

    def draw(self):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.size, self.size))


class RandomBlock:

    def __init__(self):
        possible_squares = []
        self.color = (255, 255, 255)  # white
        self.position = None
        for square in squares:
            if square.type == "unoccupied":
                possible_squares.append([square.x, square.y])
        self.position = random.choice(possible_squares)
        for square in squares:
            if self.position == [square.x, square.y]:
                square.type = "occupied"
                square.specific_type = 3
                square.color = self.color
                self.square = square
                break

    def delete(self):
        blocks.remove(self)


class Snake:
    def __init__(self, key_left=pygame.K_LEFT, key_right=pygame.K_RIGHT, key_up=pygame.K_UP, key_down=pygame.K_DOWN, x=4, y=7, color=(0, 255, 0)):
        self.current_square = [x, y]
        self.touching_squares = [
            [x, y],
            [x-1, y],
            [x-2, y],
        ]
        self.score = len(self.touching_squares)-3
        self.key_left = key_left
        self.key_right = key_right
        self.key_up = key_up
        self.key_down = key_down
        self.direction = "right"
        self.color = color
        self.length = len(self.touching_squares)
        for square in self.touching_squares:
            for square2 in squares:
                if square[0]*20 == square2.x and square[1]*20 == square2.y:
                    square2.type = "occupied"
                    square2.specific_type = 1
                    square2.color = self.color

    def move(self, keys):
        if keys[self.key_left] and self.direction != "right":
            self.direction = "left"
        elif keys[self.key_right] and self.direction != "left":
            self.direction = "right"
        elif keys[self.key_up] and self.direction != "down":
            self.direction = "up"
        elif keys[self.key_down] and self.direction != "up":
            self.direction = "down"
        if self.direction == "left":
            self.current_square[0] -= 1
        elif self.direction == "right":
            self.current_square[0] += 1
        elif self.direction == "up":
            self.current_square[1] -= 1
        elif self.direction == "down":
            self.current_square[1] += 1
        self.touching_squares.pop(-1)
        self.touching_squares.insert(0, self.current_square.copy())
        for square in squares:
            for touching_square in self.touching_squares:
                if square.x == touching_square[0]*20 and square.y == touching_square[1]*20:
                    if square.color == (255, 0, 0):
                        self.add_link()
                        blocks.append(RandomBlock())
                        for apple in apples:
                            if apple.position == [square.x, square.y]:
                                apple.delete()

                    if square.color == (255, 255, 255):
                        self.delete()
                    square.color = self.color
                    square.type = "occupied"
                    square.specific_type = 1
                    if touching_square == self.current_square:
                        square.specific_type = 4

        for square in squares:
            if square.color == self.color:
                if [square.x/20, square.y/20] in self.touching_squares:
                    for enemysnake in enemysnakes:
                        if [square.x/20, square.y/20] in enemysnake.touching_squares:
                            self.touching_squares.pop(-1)
                            self.touching_squares.pop(-1)
                            self.touching_squares.pop(-1)
                            if len(self.touching_squares) < 1:
                                self.delete()
                            enemysnake.delete()
                            break
                else:
                    square.color = (0, 0, 0)
                    square.type = "unoccupied"
                    square.specific_type = 0

    def check(self):
        try:
            self.score = len(self.touching_squares)-3
            if 0 <= self.current_square[0] <= 29 and 0 <= self.current_square[1] <= 29:
                pass
            else:
                self.delete()
            if self.touching_squares.count(self.touching_squares[0]) > 1:
                self.delete()
            try:
                temp_list = snakes.copy()
                temp_list.remove(self)
            except ValueError:
                return
            for snake in temp_list:
                if self.touching_squares.count(snake.touching_squares[0]) > 0:
                    snake.delete()
        except IndexError:
            self.delete()
            print("you lost")
            exit()
        except ValueError:
            self.delete()
            print("you lost")
            exit()

    def delete(self):
        try:
            global run
            snakes.remove(self)
            for square in squares:
                if [square.x/20, square.y/20] in self.touching_squares:
                    square.color = (0, 0, 0)
                    square.type = "unoccupied"
                    square.specific_type = 0
            if len(snakes) == 0:
                run = not run
        except ValueError or IndexError:
            print("You lost")
            exit()

    def add_link(self):
        self.touching_squares.append(self.touching_squares[-1].copy())


class Enemy_Snake:
    def __init__(self, x, y, color=(254, 0, 0)):
        self.current_square = [x, y]
        self.touching_squares = [
            [x, y],
        ]
        self.color = color
        self.length = len(self.touching_squares)
        self.direction = "right"

    def move(self):
        possible_pursuits = []
        possible_distances = []
        for snake in snakes:
            for square in snake.touching_squares:
                appender = [square[0], square[1]]
                possible_pursuits.append(appender)
        for pursuit in possible_pursuits:
            distance = math.sqrt((self.current_square[0] - pursuit[0])**2 + (self.current_square[1] - pursuit[1])**2)
            possible_distances.append(distance)
        itemindex = possible_distances.index(min(possible_distances))
        square = possible_pursuits[itemindex]
        distance_x = square[0] - self.current_square[0]
        distance_y = square[1] - self.current_square[1]
        if abs(distance_x) > abs(distance_y):
            if distance_x > 0:
                self.direction = "right"
            else:
                self.direction = "left"
        else:
            if distance_y > 0:
                self.direction = "down"
            else:
                self.direction = "up"
        if self.direction == "left":
            self.current_square[0] -= 1
        elif self.direction == "right":
            self.current_square[0] += 1
        elif self.direction == "up":
            self.current_square[1] -= 1
        elif self.direction == "down":
            self.current_square[1] += 1
        self.touching_squares.pop(-1)
        self.touching_squares.insert(0, self.current_square.copy())
        for square in squares:
            for touching_square in self.touching_squares:
                if square.x == touching_square[0]*20 and square.y == touching_square[1]*20:
                    if square.color == (255, 255, 255):
                        self.delete()
                    square.color = self.color
                    square.type = "occupied"
                    square.specific_type = 1

        for square in squares:
            if square.color == self.color:
                if [square.x/20, square.y/20] in self.touching_squares:
                    pass
                else:
                    square.color = (0, 0, 0)
                    square.type = "unoccupied"
                    square.specific_type = 0

    def delete(self):
        for square in squares:
            if [square.x/20, square.y/20] in self.touching_squares:
                square.color = (0, 0, 0)
                square.type = "unoccupied"
                square.specific_type = 0
        enemysnakes.remove(self)


def game_to_matrix():
    matrix = []
    for i in range(30):
        matrix.append([])
        for j in range(30):
            matrix[i].append(0)
    for square in squares:
        matrix[int(square.y/20)].insert(int(square.x/20), square.specific_type)


def main():
    global snakes, apples, blocks, squares, enemysnakes, font, run, window


    pygame.init()

    screen = pygame.display.set_mode((600, 600))

    window = pygame.Surface((600,600))

    snakes = []
    apples = []
    blocks = []
    squares = []
    enemysnakes = []

    run = True
    for i in range(0, 30):
        for j in range(0, 30):
            squares.append(Square(i*20, j*20))
    for i in range(0, 1): apples.append(Apple())
    snakes.append(Snake())
    enemysnakes.append(Enemy_Snake(20, 10, color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
    now = time.time()
    interval = 0.0625
    enemy_now = time.time()
    enemy_interval = 0.0625*3
    pause = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.K_ESCAPE:
                print("pausing")
                time.sleep(0.5)
                while pause:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                            pygame.quit()
                        elif event.type == pygame.K_ESCAPE:
                            pause = False
                pause = True
        keys = pygame.key.get_pressed()
        if len(apples) < 1:
            apples.append(Apple())
        if time.time() - now > interval:
            for snake in snakes:
                snake.move(keys)
                snake.check()

            now = time.time()
        if time.time() - enemy_now > enemy_interval:
            for enemy in enemysnakes:
                enemy.move()
            enemy_now = time.time()
            if len(enemysnakes) < 3:
                enemysnakes.append(Enemy_Snake(random.randint(0, 29), random.randint(0, 29), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
            if random.randint(0, 10) == 5:
                enemysnakes[random.randint(0, len(enemysnakes)-1)].delete()
                enemysnakes.append(Enemy_Snake(random.randint(0, 29), random.randint(0, 29), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))
        for square in squares:
            square.draw()
        screen.blit(window, (0, 0))
        pygame.display.update()
        game_to_matrix()


if "__main__" == __name__:
    main()
