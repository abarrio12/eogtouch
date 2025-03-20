# keyboard.py
import pygame

# Definir algunas constantes para el tamaño y color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Keyboard:
    def __init__(self, keyboard_image_path, arrow_image_path, width=800, height=600):
        self.keyboard_image = pygame.image.load(keyboard_image_path)
        self.keyboard_image = pygame.transform.scale(self.keyboard_image, (400, 200))  # Ajusta el tamaño
        self.keyboard_rect = self.keyboard_image.get_rect(topleft=(10, 50))
        
        self.arrow_image = pygame.image.load(arrow_image_path)
        self.arrow_image = pygame.transform.scale(self.arrow_image, (40, 40))
        self.arrow_rect = self.arrow_image.get_rect(topleft=(10, 10))
        
        self.keyboard_visible = False
        self.width = width
        self.height = height

    def update_keyboard_visibility(self):
        """Actualizar la visibilidad del teclado según la posición del cursor."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.arrow_rect.collidepoint(mouse_x, mouse_y):
            self.keyboard_visible = True
        else:
            self.keyboard_visible = False

    def render(self, screen):
        """Renderizar la flecha y el teclado en la pantalla."""
        screen.blit(self.arrow_image, self.arrow_rect)
        if self.keyboard_visible:
            screen.blit(self.keyboard_image, self.keyboard_rect)
