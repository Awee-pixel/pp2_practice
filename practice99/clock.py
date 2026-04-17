import pygame
import datetime

class MickeyClock:
    def __init__(self, center_x, center_y):
        self.center = (center_x, center_y)
        
        # 1. Загружаем фон (убедитесь, что название файла точно совпадает)
        self.bg_img = pygame.image.load("images/mickeyclock.jpeg").convert()
        
        # Опционально: если ваш фон не 800x800, можно подогнать его под размер окна
        # self.bg_img = pygame.transform.scale(self.bg_img, (800, 800))
        
        # 2. Загружаем руки (замените названия на те, что используете вы)
        self.left_hand_img = pygame.image.load("images/left_hand.png").convert_alpha()
        self.right_hand_img = pygame.image.load("images/right_hand.png").convert_alpha()

    def draw(self, screen):
        # Получаем время
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second

        # Вычисляем углы
        sec_angle = -(seconds * 6)
        min_angle = -(minutes * 6)

        # 3. ОТРИСОВКА ФОНА (раньше она была закомментирована)
        bg_rect = self.bg_img.get_rect(center=self.center)
        screen.blit(self.bg_img, bg_rect)

        # 4. Отрисовка рук
        self._rotate_and_draw(screen, self.right_hand_img, min_angle) # Минуты
        self._rotate_and_draw(screen, self.left_hand_img, sec_angle)  # Секунды

    def _rotate_and_draw(self, screen, image, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=self.center)
        screen.blit(rotated_image, new_rect)