import pygame



#draw a mesh in rectangle Lx, Rx, Uy, Dy with num_x of lines and num_y of lines on win
def draw_mesh(win, Lx, Uy, Rx, Dy, len_x, len_y):
    if Lx >= Rx or Uy >= Dy:
        print("error input")



    num_x = int((Rx - Lx) / len_x)
    num_y = int((Dy - Uy) / len_y)
    for i in range(1, num_x + 1):
        pygame.draw.line(win, (0, 0, 0), (Lx + len_x * i, Uy), (Lx + len_x * i, Dy), 1)
    for i in range(1, num_y + 1):
        pygame.draw.line(win, (0, 0, 0), (Lx, Uy + len_y * i), (Rx, Uy + len_y * i))



