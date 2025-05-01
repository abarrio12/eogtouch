import pygame

# Constantes
ALIGNMENT_THRESHOLD = 30  # In pixels
WAITING_FOR_ALIGMENT_THRESHOLD = 20  # In seconds
WAITING_FOR_KEYPRESS_THRESHOLD = 5  # In seconds
KEYPRESS_TIMEOUT = 3  # In seconds
ERROR_DISPLAY_TIME = 2  # Tiempo para mostrar el error antes de continuar

# TODO:  Usar esta constante para controlar si se muestra o no
# retroalimentación de la tecla presionada
SHOW_KEYPRESSED = False

GREEN_KEYS = {
    pygame.K_q,
    pygame.K_w,
    pygame.K_e,
    pygame.K_a,
    pygame.K_s,
    pygame.K_d,
    pygame.K_z,
    pygame.K_x,
    pygame.K_c,
}
BLUE_KEYS = {
    pygame.K_i,
    pygame.K_o,
    pygame.K_p,
    pygame.K_j,
    pygame.K_k,
    pygame.K_l,
    pygame.K_b,
    pygame.K_n,
    pygame.K_m,
}
