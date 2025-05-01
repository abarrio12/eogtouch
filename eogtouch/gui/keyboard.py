import pygame


class Keyboard:
    def render_intro(self, screen, width, height):
        # Limpia la pantalla con fondo blanco
        screen.fill((255, 255, 255))

        # Nota: Todas las figuras y fuentes se escalan según el tamaño de la pantalla y se posicionan segun porcentajes

        # Fuente escalada según el tamaño de pantalla
        title_font = pygame.font.SysFont("Comic Sans MS", int(0.08 * height), bold=True)
        subtitle_font = pygame.font.SysFont("Comic Sans MS", int(0.04 * height))
        start_font = pygame.font.SysFont("Comic Sans MS", int(0.045 * height))

        # Dibuja el título centrado al 10% de la altura
        title = title_font.render("EOG Game Touch v1.0", True, (0, 0, 0))
        screen.blit(title, title.get_rect(center=(width // 2, int(0.10 * height))))

        # Subtítulos explicativos escalonados debajo del título
        intro_lines = [
            "Siga la figura con la mirada y cuando esta",
            "cambie de color presione una de las teclas",
            "que coincidan con este",
        ]
        for i, line in enumerate(intro_lines):
            text = subtitle_font.render(line, True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=(width // 2, int((0.20 + i * 0.04) * height))))

        # Barra gris que contiene el mensaje de espacio
        bar_width = int(0.6 * width)
        bar_height = int(0.06 * height)
        bar_x = (width - bar_width) // 2
        bar_y = int(0.33 * height)
        pygame.draw.rect(screen, (150, 150, 150), (bar_x, bar_y, bar_width, bar_height), border_radius=10)

        # Texto del mensaje de inicio sobre la barra gris
        message = start_font.render("Presione ESPACIO para iniciar", True, (255, 255, 255))
        screen.blit(message, message.get_rect(center=(width // 2, bar_y + bar_height // 2)))

        # Tamaños de las teclas variables según el tamaño de pantalla
        key_size = int(0.08 * height)
        padding = int(0.015 * height)
        font_size = int(0.035 * height)

        # Desplazamientos por fila (para escalonado tipo QWERTY -> teclado real)
        left_offsets = [0, int(0.03 * width), int(0.06 * width)]
        right_offsets = [int(0.06 * width), int(0.03 * width), 0]

        # Ancho total de las teclas por bloque (3 teclas + padding)
        block_width = 3 * (key_size + padding) - padding
        total_width = block_width * 2 + int(0.05 * width)  # Ambos bloques + separación central
        start_x_centered = (width - total_width) // 2  # Punto inicial centrado

        # Desplazamos los bloques lateralmente para evitar solapamiento (una tecla de separación extra)
        left_start_x = start_x_centered - key_size
        right_start_x = start_x_centered + block_width + int(0.05 * width) + key_size

        # Posición vertical de inicio del teclado
        start_y = int(0.45 * height)

        # Dibujamos el bloque izquierdo del teclado (teclas verdes)
        self.draw_keys(
            screen,
            [["Q", "W", "E"], ["A", "S", "D"], ["Z", "X", "C"]],
            start_x=left_start_x,
            start_y=start_y,
            color=(0, 153, 0),
            row_offsets=left_offsets,
            key_size=key_size,
            padding=padding,
            font_size=font_size,
        )

        # Dibujamos el bloque derecho del teclado (teclas azules)
        self.draw_keys(
            screen,
            [["I", "O", "P"], ["J", "K", "L"], ["B", "N", "M"]],
            start_x=right_start_x,
            start_y=start_y,
            color=(0, 102, 204),
            row_offsets=right_offsets,
            key_size=key_size,
            padding=padding,
            font_size=font_size,
        )

        # Calculamos el borde inferior del teclado
        teclado_height = 3 * (key_size + padding) - padding
        teclado_bottom = start_y + teclado_height

        # Posición de la barra espaciadora justo debajo del teclado
        spacebar_width = int(0.3 * width)
        spacebar_height = int(0.07 * height)
        spacebar_x = (width - spacebar_width) // 2
        spacebar_y = teclado_bottom + padding  # asi la ponemos pegada al teclado

        # Dibujamos la barra espaciadora centrada
        self.draw_spacebar(
            screen,
            start_x=spacebar_x,
            y=spacebar_y,
            width=spacebar_width,
            height=spacebar_height,
            color=(100, 100, 100),
        )

    def draw_keys(self, screen, keys, start_x, start_y, color, row_offsets, key_size, padding, font_size):
        # Dibuja las teclas dadas en forma de matriz, respetando offsets y escalado
        font = pygame.font.SysFont("Comic Sans MS", font_size)

        for row_idx, row in enumerate(keys):
            offset = row_offsets[row_idx]  # Desplazamiento horizontal por fila
            for col_idx, key in enumerate(row):
                x = start_x + offset + col_idx * (key_size + padding)
                y = start_y + row_idx * (key_size + padding)
                # Dibuja tecla
                pygame.draw.rect(screen, color, (x, y, key_size, key_size), 3, border_radius=8)
                # Dibuja texto centrado
                text = font.render(key, True, color)
                screen.blit(text, text.get_rect(center=(x + key_size / 2, y + key_size / 2)))

    def draw_spacebar(self, screen, start_x, y, width, height, color):
        # Dibuja una barra espaciadora gris con texto blanco
        pygame.draw.rect(screen, color, (start_x, y, width, height), border_radius=12)
        font = pygame.font.SysFont("Comic Sans MS", int(height * 0.4))
        text = font.render("ESPACIO", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(start_x + width // 2, y + height // 2)))
