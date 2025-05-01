import pygame

# Constantes
alignment_threshold = 30  # In pixels
waiting_for_alignment_threshold = 20  # In seconds
waiting_for_keypress_threshold = 5  # In seconds
keypress_timeout = 3  # In seconds
error_display_time = 2  # Tiempo para mostrar el error antes de continuar

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
