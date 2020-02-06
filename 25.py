import pygame
import sys
import random


class Menu:
    def __init__(self, punkts=[12, 140, "Punkt", (20, 20, 20), (20, 20, 255), 0]):
        self.punkts = punkts

    def draw(self, poverhnost, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        # Создание самого меню
        done = True
        font_menu = pygame.font.Font(None, 80)
        punkt = 0
        while done:
            # Фон для меню
            fon = 'snake.jpg'
            game.play_surface.blit(pygame.image.load(fon), (0, 0))
            mp = pygame.mouse.get_pos()

            for i in self.punkts:
                if mp[0] > i[0] and mp[0] < i[0] + 155 and mp[1] > i[1] and mp[1] < i[1] + 50:
                    punkt = i[5]

            self.draw(game.play_surface, font_menu, punkt)
            # Цикл по ивентам для клавиш меню
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit()
                    if event.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if event.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                    if event.key == pygame.K_RETURN:
                        if punkt == 0:
                            done = False
                        elif punkt == 1:
                            exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    print(punkt)
                    if punkt == 0:
                        done = False
                    elif punkt == 1:
                        exit()

            pygame.display.flip()


class Game:
    def __init__(self):
        # задаем размеры экрана
        self.screen_width = 700
        self.screen_height = 400

        # необходимые цвета
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.brown = pygame.Color(165, 42, 42)
        self.white = pygame.Color(255, 255, 255)

        # Frame per second controller
        # будет задавать количество кадров в секунду
        self.fps_controller = pygame.time.Clock()

        # переменная для оторбражения результата
        # (сколько еды съели)
        self.score = 0

    def init_and_check_for_errors(self):
        # Начальная функция для инициализации и проверки как запуска pygame
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()
        else:
            print('Ok')

    def set_surface_and_title(self):
        # Задаем surface(поверхность, на которой все будет рисоваться) и устанавливаем загаловок окна
        self.play_surface = pygame.display.set_mode((
            self.screen_width, self.screen_height))
        pygame.display.set_caption('The best Snake ever')

    def event_loop(self, change_to):
        # Функция для отслеживания нажатий клавиш игроком

        # запускаем цикл по ивентам
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    change_to = "RIGHT"
                elif event.key == ord('d'):
                    change_to = "RIGHT"

                elif event.key == pygame.K_LEFT:
                    change_to = "LEFT"
                elif event.key == ord('a'):
                    change_to = "LEFT"

                elif event.key == pygame.K_UP:
                    change_to = "UP"
                elif event.key == ord('w'):
                    change_to = "UP"

                elif event.key == pygame.K_DOWN:
                    change_to = "DOWN"
                elif event.key == ord('s'):
                    change_to = "DOWN"

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # выход из игры на крестик
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        return change_to

    def refresh_screen(self):
        # обновление экрана и задание фпс
        pygame.display.flip()
        game.fps_controller.tick(20)

    def show_score(self, choice=1):
        # Отображение результата
        sur_font = pygame.font.SysFont('elephant', 30)
        sur_surf = sur_font.render(
            'Score: {0}'.format(self.score), True, self.white)
        sur_rect = sur_surf.get_rect()
        # дефолтный случай, результат отображается слева сверху
        if choice == 1:
            sur_rect.midtop = (60, 18)
        # при протигрыше отображаем результат по центру
        else:
            sur_rect.midtop = (350, 250)
        # рисуем прямоугольник поверх surface
        self.play_surface.blit(sur_surf, sur_rect)

    def game_over(self):
        # Функция для вывода надписи Game Over и результатов, в случае выхода из игры
        stop = True
        go_font = pygame.font.SysFont('britannic bold', 90)
        go_surf = go_font.render('Game over', True, self.red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 130)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(0)
        pygame.display.flip()
        while stop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


class Snake:
    def __init__(self, snake_color):
        # позиция головы и тела змеи
        self.snake_head_pos = [0, 250]  # [x, y]
        # начальное тело змеи состоит из трех сегментов
        # голова змеи - первый элемент, хвост - последний
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.snake_color = snake_color
        # дефолтное направление змеи (вправо)
        self.direction = "RIGHT"
        # куда будет меняться напрвление движения змеи
        # при нажатии соответствующих клавиш
        self.change_to = self.direction

    def validate_direction_and_change(self):
        # Изменение направления движения змеи (если оно не прямо противоположно текущему)
        if any((
                self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
        # Изменение положение головы змеи
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 10
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 10
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 10
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 10

    def snake_body_mechanism(self, score, food_pos, screen_width, screen_height):
        # если вставлять просто snake_head_pos, то на всех трех позициях в snake_body
        # окажется один и тот же список с одинаковыми координатами и мы будем управлять змеей из одного квадрата
        self.snake_body.insert(0, list(self.snake_head_pos))
        # если съели еду
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            # Задаётся рандомно новое положение еды и увеличивется score на один
            food_pos = [random.randrange(1, screen_width / 10) * 10,
                        random.randrange(1, screen_height / 10) * 10]
            score += 1
        else:
            # если не нашли еду, то убираем последний сегмент (без этого змея будет постоянно расти)
            self.snake_body.pop()
        return score, food_pos

    def draw_snake(self, play_surface, surface_color):
        # Отображение всех сегментов змеи и заливка фона
        play_surface.fill((0, 0, 0))
        for pos in self.snake_body:
            pygame.draw.rect(play_surface, self.snake_color, pygame.Rect(
                    pos[0], pos[1], 10, 10))

    def check_for_boundaries(self, game_over, screen_width, screen_height):
        # Проверка на столкновение с рамками
        if any((
            self.snake_head_pos[0] > screen_width - 10
            or self.snake_head_pos[0] < 0,
            self.snake_head_pos[1] > screen_height - 10
            or self.snake_head_pos[1] < 0
        )):
            game_over()
        # проверка на то, что первый элемент(голова) врезался в другой элемент
        for block in self.snake_body[1:]:
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                game_over()


class Food:
    def __init__(self, food_color, screen_width, screen_height):
        self.food_color = food_color
        self.food_size_x = 10
        self.food_size_y = 10
        self.food_pos = [random.randrange(1, screen_width / 10) * 10,
                         random.randrange(1, screen_height / 10) * 10]

    def draw_food(self, play_surface):
        # Отображение еды
        pygame.draw.rect(
            play_surface, self.food_color, pygame.Rect(
                self.food_pos[0], self.food_pos[1],
                self.food_size_x, self.food_size_y))


game = Game()

snake = Snake(game.green)

food = Food(game.brown, game.screen_width, game.screen_height)

game.init_and_check_for_errors()
game.set_surface_and_title()

punkts = [(270, 130, 'Play', (251, 206, 177), (30, 255, 30), 0),
          (240, 220, 'Escape', (251, 206, 177), (30, 255, 30), 1)]
mymenu = Menu(punkts)
mymenu.menu()

while True:
    snake.change_to = game.event_loop(snake.change_to)

    snake.validate_direction_and_change()
    snake.change_head_position()
    game.score, food.food_pos = snake.snake_body_mechanism(
        game.score, food.food_pos, game.screen_width, game.screen_height)
    snake.draw_snake(game.play_surface, game.white)

    food.draw_food(game.play_surface)

    snake.check_for_boundaries(
        game.game_over, game.screen_width, game.screen_height)

    game.show_score()
    game.refresh_screen()
