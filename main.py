import pygame
import random
import time

WIDTH = 720
LENGTH = WIDTH
CELL_SIZE = 72
CELLS_ROW = WIDTH // CELL_SIZE
CELLS_COLUMN = LENGTH // CELL_SIZE
FONT = "Courier New"
COLOR = (0, 255, 120)
SNAKE_COLOR = (0, 0, 255)
SNAKE_HEAD_COLOR = (50, 50, 150)
SNAKE_BORDER_COLOR = (100, 100, 255)
APPLE_COLOR = (255, 0, 0)
APPLE_BORDER_COLOR = (255, 100, 100)
SPEED = CELL_SIZE  
MOVE_INTERVAL = 500  # Milliseconds 

class Snake:
    def __init__(self) -> None:
        self.size = CELL_SIZE
        self.color = SNAKE_COLOR
        self.head_color = SNAKE_HEAD_COLOR
        self.body = [pygame.Rect(0, 0, CELL_SIZE, CELL_SIZE)]
        self.direction = "D"
        self.grow_next_move = False  
        
    def update_position(self):
        head = self.body[0].copy()
        if self.direction == "D":
            head.x += CELL_SIZE
        elif self.direction == "W":
            head.y -= CELL_SIZE
        elif self.direction == "S":
            head.y += CELL_SIZE
        elif self.direction == "A":
            head.x -= CELL_SIZE
        
        self.body.insert(0, head)
        
        if not self.grow_next_move:
            self.body.pop()
        else:
            self.grow_next_move = False
        
    def grow(self):
        self.grow_next_move = True


class Apple:
    def __init__(self, snake) -> None:
        self.size = CELL_SIZE
        self.color = APPLE_COLOR
        self.body = pygame.Rect(0, 0, CELL_SIZE, CELL_SIZE)
        self.change_pos(snake)
    
    def change_pos(self, snake):
        while True:
            self.body.x = random.randint(0, CELLS_ROW - 1) * CELL_SIZE
            self.body.y = random.randint(0, CELLS_COLUMN - 1) * CELL_SIZE
            if not any(segment.colliderect(self.body) for segment in snake.body):
                break

    def get_eaten(self, snake):
        self.change_pos(snake)

class Screen:
    def __init__(self) -> None:
        self.display = pygame.display.set_mode((WIDTH, LENGTH))
        pygame.display.set_caption("Snake Game")
        self.font = pygame.font.SysFont(FONT, 36)
        
    def draw(self):
        self.display.fill(COLOR)

    def draw_snake(self, snake):
        for segment in snake.body:
            if segment == snake.body[0]:
                pygame.draw.rect(self.display, SNAKE_HEAD_COLOR, segment)
                pygame.draw.rect(self.display, SNAKE_BORDER_COLOR, segment, 5, 1)
            else:
                pygame.draw.rect(self.display, snake.color, segment)
                pygame.draw.rect(self.display, SNAKE_BORDER_COLOR, segment, 5, 1)

    def draw_apple(self, apple):
        pygame.draw.rect(self.display, apple.color, apple.body)
        pygame.draw.rect(self.display, APPLE_BORDER_COLOR, apple.body, 5, 1)

    def show_game_over(self):
        game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, LENGTH // 2))
        self.display.blit(game_over_text, text_rect)

def loop():
    screen = Screen()
    snake = Snake()
    apple = Apple(snake)
    playing = True
    game_over = False

    clock = pygame.time.Clock()
    last_move_time = pygame.time.get_ticks()

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        if not game_over:
            #TODO solve the issue where it changes directions 2 times before changing squares
            key = pygame.key.get_pressed()  # Atualiza o estado das teclas
            if key[pygame.K_d] and snake.direction != "A":
                snake.direction = "D"
            elif key[pygame.K_w] and snake.direction != "S":
                snake.direction = "W"
            elif key[pygame.K_s] and snake.direction != "W":
                snake.direction = "S"
            elif key[pygame.K_a] and snake.direction != "D":
                snake.direction = "A"

            current_time = pygame.time.get_ticks()
            if current_time - last_move_time > MOVE_INTERVAL:
                snake.update_position()
                last_move_time = current_time

            # Verifica se a cobra saiu dos limites da tela
            if snake.body[0].left < 0 or snake.body[0].right >= WIDTH or snake.body[0].top < 0 or snake.body[0].bottom >= LENGTH:
                game_over = True
                game_over_start_time = time.time()

            # Verifica se a cobra comeu a maçã
            if snake.body[0].colliderect(apple.body):
                apple.get_eaten(snake)
                snake.grow()

        screen.draw()
        screen.draw_snake(snake)
        screen.draw_apple(apple)
        
        if game_over:
            screen.show_game_over()
            if time.time() - game_over_start_time > 5:  # Aguarde 5 segundos antes de fechar
                playing = False

        pygame.display.update() 
        clock.tick(60)  

def start_game():
    pygame.init()

def end_game():
    pygame.quit()

def main():
    start_game()
    loop()
    end_game()

if __name__ == "__main__":
    main()
