import pygame
import time
import random

WIDTH, HEIGHT = 1000,1000
ROWS, COLS = 50, 50
SQUARE_SIZE = WIDTH//COLS


WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Snake:
    def __init__(self):
        self.body = [[50,50]]
        self.direction = "RIGHT"

    def change_direction_to(self, dir):
        if dir=="RIGHT" and not self.direction=="LEFT":
            self.direction = "RIGHT"
        if dir=="LEFT" and not self.direction=="RIGHT":
            self.direction = "LEFT"
        if dir=="UP" and not self.direction=="DOWN":
            self.direction = "UP"
        if dir=="DOWN" and not self.direction=="UP":
            self.direction = "DOWN"

    def move(self, foodPos):
        if self.direction == "RIGHT":
            self.body.insert(0, list([self.body[0][0] + SQUARE_SIZE, self.body[0][1]]))
        if self.direction == "LEFT":
            self.body.insert(0, list([self.body[0][0] - SQUARE_SIZE, self.body[0][1]]))
        if self.direction == "UP":
            self.body.insert(0, list([self.body[0][0], self.body[0][1] - SQUARE_SIZE]))
        if self.direction == "DOWN":
            self.body.insert(0, list([self.body[0][0], self.body[0][1] + SQUARE_SIZE]))

        if self.get_head_rect().colliderect(pygame.Rect(foodPos[0], foodPos[1], SQUARE_SIZE, SQUARE_SIZE)):
            return 1
        else:
            self.body.pop()
            return 0
    def check_collision(self):
        if self.body[0] in self.body[1:]:
            return 1
        if self.body[0][0] >= WIDTH or self.body[0][0] < 0:
            return 1
        if self.body[0][1] >= HEIGHT or self.body[0][1] < 0:
            return 1
        return 0

    def get_head_pos(self):
        return self.body[0]

    def get_body(self):
        return self.body

    def get_head_rect(self):
        return pygame.Rect(self.body[0][0], self.body[0][1], SQUARE_SIZE, SQUARE_SIZE)

class Food:
    def __init__(self):
        self.position = [random.randrange(1, ROWS//SQUARE_SIZE*SQUARE_SIZE*SQUARE_SIZE), random.randrange(1, COLS//SQUARE_SIZE*SQUARE_SIZE*SQUARE_SIZE)]
        self.isFoodOnScreen = True

    def spawn_food(self):
        if self.isFoodOnScreen == False:
            self.position = [random.randrange(2, ROWS // SQUARE_SIZE * SQUARE_SIZE * SQUARE_SIZE),
                             random.randrange(2, COLS // SQUARE_SIZE * SQUARE_SIZE * SQUARE_SIZE)]
            self.isFoodOnScreen = True
        return self.position

    def set_food_on_screen(self, b):
        self.isFoodOnScreen = b

# def game_over_message():
#     font = pygame.font.Font(None, 36)
#     text = font.render("Игра окончена. Нажмите 'g' чтобы начать заново или 'q' чтобы выйти.", 1, (255, 255, 255))
#     window.blit(text, (50, 50))
#     pygame.display.flip()

def game():

    pygame.init()

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    fps = pygame.time.Clock()

    snake = Snake()
    food = Food()

    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_UP]:
                    snake.change_direction_to("UP")
                if keys[pygame.K_DOWN]:
                    snake.change_direction_to("DOWN")
                if keys[pygame.K_LEFT]:
                    snake.change_direction_to("LEFT")
                if keys[pygame.K_RIGHT]:
                    snake.change_direction_to("RIGHT")

        foodPos = food.spawn_food()
        if (snake.move(foodPos) == 1):
            score += 1
            food.set_food_on_screen(False)

        window.fill(WHITE)
        for pos in snake.get_body():
            pygame.draw.rect(window, GREEN, pygame.Rect(pos[0], pos[1], SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(window, RED, pygame.Rect(foodPos[0], foodPos[1], SQUARE_SIZE, SQUARE_SIZE))
        if (snake.check_collision() == 1):
            font = pygame.font.Font(None, 30)
            text = font.render("Игра окончена.Нажмите 'g' чтобы начать заново или 'q' чтобы выйти.", 1,
                               (200,0,0))
            window.blit(text,(WIDTH//5, HEIGHT//2))
            pygame.display.update()
            while True:
                event = pygame.event.wait()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                    game()
                    break
                elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    pygame.quit()

        pygame.display.set_caption("Snake Game | Score : " + str(score))
        pygame.display.update()
        fps.tick(15)

if __name__ == "__main__":
    game()
