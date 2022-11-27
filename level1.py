import time
import random
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import serial


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


class Key:

    def __init__(self, x, y, list_of_squares, color):
        self.position = [x*20, y*20]
        self.color = color
        self.list_of_squares = list_of_squares
        for square in squares:
            if self.position == [square.x, square.y]:
                square.type = "occupied"
                square.specific_type = 8
                square.color = self.color
                self.square = square
                break

    def delete(self):
        keys.remove(self)

    def open(self):
        for square in self.list_of_squares:
            squares.append(square)
        self.delete()


class EndLevel:
    def __init__(self, x, y, required_length, color=(0, 0, 0)):
        self.position = [x*20, y*20]
        self.color = color
        self.required_length = required_length
        for square in squares:
            if self.position == [square.x, square.y]:
                square.type = "occupied"
                square.specific_type = 9
                square.color = self.color
                self.square = square
                break

    def open(self, snake):
        if len(snake.touching_squares) >= self.required_length:
            print("You win!")
            snake.delete()
        else:
            print("You need more length to win!")

    def recheck(self):
        for square in squares:
            if self.position == [square.x, square.y]:
                square.type = "occupied"
                square.specific_type = 9
                square.color = self.color
                self.square = square
                break


class Teleporter:

    def __init__(self, x, y, x_dest, y_dest, color=(125, 125, 125), secondary_color=(125,125,125)):
        self.position = [x*20, y*20]
        self.color = color
        self.secondary_color = secondary_color
        self.x_dest = x_dest
        self.y_dest = y_dest
        for square in squares:
            if self.position == [square.x, square.y]:
                square.type = "occupied"
                square.specific_type = 6
                square.color = self.color
                self.primary_square = square
            elif self.x_dest == square.x/20 and self.y_dest == square.y/20:
                square.type = "occupied"
                square.specific_type = 7
                square.color = self.secondary_color
                self.destination_square = square

    def delete(self):
        teleporters.remove(self)


class Square:
    def __init__(self, x, y, color=(0,0,0), block_type="unoccupied", specific_type=0):  # 0 = unoccupied, 1 = snake, 2 = apple, 3 = block, 4 = snakehead
        self.x = x
        self.y = y
        self.size = 20
        self.color = color  # black and unoccupied
        self.type = block_type
        self.specific_type = specific_type

    def draw(self, x_offset=0, y_offset=0):
        x = self.x + x_offset
        y = self.y + y_offset
        if 0 <= x < 600 and 0 <= y < 600:
            if self.color != (255, 255, 255):
                pygame.draw.rect(window, self.color, [x, y, self.size, self.size])


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
    def __init__(self, key_left=pygame.K_LEFT, key_right=pygame.K_RIGHT, key_up=pygame.K_UP, key_down=pygame.K_DOWN, x=15, y=15, color=(0, 255, 0), joystick=False):
        self.current_square = [x, y]
        self.touching_squares = [
            [x, y],
            [x-1, y],
            [x-2, y],
        ]
        self.joystick=False

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

    def move(self, key_presses):
        if key_presses[self.key_left] and self.direction != "right":
            self.direction = "left"
        elif key_presses[self.key_right] and self.direction != "left":
            self.direction = "right"
        elif key_presses[self.key_up] and self.direction != "down":
            self.direction = "up"
        elif key_presses[self.key_down] and self.direction != "up":
            self.direction = "down"
        if self.joystick:
            self.joystick.read(self)
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
        for teleporter in teleporters:
            if teleporter.position == [self.current_square[0]*20, self.current_square[1]*20]:
                self.current_square = [teleporter.x_dest, teleporter.y_dest]

        for endlevel in endlevels:
            if endlevel.position == [self.current_square[0]*20, self.current_square[1]*20]:
                endlevel.open(self)

        for key in keys:
            if key.position == [self.current_square[0]*20, self.current_square[1]*20]:
                key.open()

        for square in squares:
            if square.color == self.color:
                if [square.x/20, square.y/20] in self.touching_squares:
                    """for enemysnake in enemysnakes:
                        if [square.x/20, square.y/20] in enemysnake.touching_squares:
                            self.touching_squares.pop(-1)
                            self.touching_squares.pop(-1)
                            self.touching_squares.pop(-1)
                            if len(self.touching_squares) < 1:
                                self.delete()
                            enemysnake.delete()
                            break"""
                else:
                    square.color = (0, 0, 0)
                    square.type = "unoccupied"
                    square.specific_type = 0

    def check(self):
        self.score = len(self.touching_squares)-3
        delete = True
        for square in squares:
            if square.x/20 == self.current_square[0] and square.y/20 == self.current_square[1]:
                delete = False
                break
        if delete:
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

    def delete(self):
        global run
        snakes.remove(self)
        for square in squares:
            if [square.x/20, square.y/20] in self.touching_squares:
                square.color = (0, 0, 0)
                square.type = "unoccupied"
                square.specific_type = 0
        if len(snakes) == 0:
            run = not run

    def add_link(self):
        self.touching_squares.append(self.touching_squares[-1].copy())


"""class Joystick:
    def __init__(self, ser=serial.Serial("/dev/cu.usbmodem1414101", 9600)):
        self.ser = ser
        self.ser.read_all()

    def read(self, object):

        all_lines = self.ser.readlines()
        line = all_lines[-1]
        lines = line.decode().strip().split(" ")
        print(lines)
        try:
            if int(lines[0]) < 50:
                object.direction = "down"
                print("down")
            elif int(lines[0]) > 950:
                object.direction = "up"
                print("up")
            if int(lines[1]) < 50:
                object.direction = "left"
                print("left")
            elif int(lines[1]) > 950:
                object.direction = "right"
                print("right")
        except IndexError:
            pass"""


def list_of_squares():
    pass


def main():
    global snakes, apples, blocks, squares, enemysnakes, font, run, window, teleporters, keys, endlevels
    keys = []
    pygame.init()

    gold = (255, 255, 0)
    blue = (0, 0, 255)

    screen = pygame.display.set_mode((600, 600))

    """window = pygame.Surface((600, 600))

    snakes = []
    apples = []
    blocks = []
    squares = []
    teleporters = []
    keys = []"""

    run = True
    for i in range(0, 30):
        for j in range(0, 30):
            squares.append(Square(i*20, j*20))

    for i in range(35, 50):
        for j in range(0, 30):
            squares.append(Square(i*20, j*20))
    for i in range(5, 25):
        for j in range(0, 80):
            squares.append(Square(i*20, -j*20))
    for i in range(0, 1): apples.append(Apple())
    teleporters.append(Teleporter(45, 15, 10, 10))
    teleporters.append(Teleporter(5, 5, 40, 20))
    list_of_squares = []
    for i in range(5, 25):
        for j in range(30, 60):
            list_of_squares.append(Square(i*20, j*20))
    keys.append(Key(45, 10, list_of_squares, blue))
    snakes.append(Snake())
    endlevels.append(EndLevel(10, 35, 5, gold))
    now = time.time()
    interval = 0.0625
    pause = True
    x_offset = 0
    y_offset = 0
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
        key_presses = pygame.key.get_pressed()
        if len(apples) < 1:
            apples.append(Apple())
        if time.time() - now > interval:
            for snake in snakes:
                snake.move(key_presses)
                snake.check()
            for teleporter in teleporters:
                teleporter.primary_square.color = teleporter.color
                teleporter.primary_square.type = "occupied"
                teleporter.primary_square.specific_type = 6
                teleporter.destination_square.color = teleporter.secondary_color
                teleporter.destination_square.type = "occupied"
                teleporter.destination_square.specific_type = 7
            for key in keys:
                key.square.color = key.color
                key.square.type = "occupied"
                key.square.specific_type = 8
            for endlevel in endlevels:
                try:
                    endlevel.square.color = endlevel.color
                    endlevel.square.type = "occupied"
                    endlevel.square.specific_type = 9
                except AttributeError:
                    endlevel.recheck()
            now = time.time()

        try:
            x_offset = 15*20 - snakes[0].current_square[0]*20
            y_offset = 15*20 - snakes[0].current_square[1]*20
        except IndexError: pass

        window.fill((255, 255, 255))
        for square in squares:
            square.draw(x_offset=x_offset, y_offset=y_offset)
        screen.blit(window, (0, 0))
        pygame.display.update()


if "__main__" == __name__:
    snakes, apples, blocks, squares, enemysnakes, font, run, window, teleporters, keys, endlevels = [], [], [], [], [], [], True, pygame.Surface((600, 600)), [], [], []
    main()
