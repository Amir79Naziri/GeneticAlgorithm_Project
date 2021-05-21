import pygame


class Mario:
    __mario_image = pygame.transform.scale(pygame.image.load('pic/mario.png'), (100, 200))
    __mario_jump_image = pygame.transform.scale(pygame.image.load('pic/mario-jump.png'), (100, 200))

    def __init__(self):
        self.state = 'Normal'
        self.position = 0
        self.real_position = 0

    def get_image(self):
        if self.state == 'Normal' or self.state == 'Dock':
            return self.__mario_image
        else:
            return self.__mario_jump_image


mario = Mario()
ground_image = pygame.image.load('pic/ground.png')
goomba_image = pygame.image.load('pic/goomba.png')
lakitu_image = pygame.image.load('pic/lakitu.png')
mushroom_image = pygame.image.load('pic/mushroom.png')
flag_image = pygame.image.load('pic/flagpole.png')

ground_png = pygame.transform.scale(ground_image, (100, 100))
goomba_png = pygame.transform.scale(goomba_image, (100, 100))
dead_goomba_png = pygame.transform.scale(goomba_image, (100, 30))
lakitu_png = pygame.transform.scale(lakitu_image, (100, 100))
mushroom_png = pygame.transform.scale(mushroom_image, (100, 100))
flag_png = pygame.transform.scale(flag_image, (100, 300))


def update_map(move, level):
    global mario
    if len(level) > 14:
        if mario.position < 7:
            mario.position += 1
    else:
        mario.position += 1
    mario.real_position += 1
    if move == '0':
        mario.state = 'Normal'
    elif move == '1':
        mario.state = 'Jump'
    else:
        mario.state = 'Dock'

    if level[mario.real_position] == 'M':
        new_level = level[:mario.real_position] + '_' + level[mario.real_position + 1:]
    elif level[mario.real_position] == 'G' and mario.state != 'Jump':
        new_level = level[:mario.real_position] + 'g' + level[mario.real_position + 1:]
    else:
        new_level = level
    return new_level


def redraw_window(window, sample_slot):
    global ground_image
    global mario
    window.fill((108, 136, 255))
    counter = 0
    for part in sample_slot:
        window.blit(ground_png, (counter * 100, 300))
        if part == 'G':
            window.blit(goomba_png, (counter * 100, 200))
        elif part == 'g':
            window.blit(dead_goomba_png, (counter * 100, 270))
        elif part == 'L':
            window.blit(lakitu_png, (counter * 100, 100))
        elif part == 'M':
            window.blit(mushroom_png, (counter * 100, 200))
        elif part == 'F':
            window.blit(flag_png, (counter * 100, 0))
        if counter == mario.position:
            if mario.state == 'Normal':
                window.blit(mario.get_image(), (counter * 100, 100))
            elif mario.state == 'Dock':
                mario_dock = pygame.transform.scale(mario.get_image(), (100, 100))
                window.blit(mario_dock, (counter * 100, 200))
            else:
                window.blit(mario.get_image(), (counter * 100, 0))
        counter += 1

    pygame.display.update()


def start(level, sample):

    pygame.init()
    clock = pygame.time.Clock()
    if len(level) > 14:
        window = pygame.display.set_mode((1400, 400))
    else:
        window = pygame.display.set_mode((len(level) * 100, 400))

    pygame.display.set_caption("Mario")
    pygame.display.set_icon(mario.get_image())

    pos = 0
    length = len(level)
    while pos < length:
        clock.tick(27)
        if length > 14:
            if pos < 7:
                redraw_window(window, level[0:14])
            else:
                redraw_window(window, level[pos - 7: pos + 7])
        else:
            redraw_window(window, level)
        level = update_map(sample[pos], level)
        pygame.time.delay(450)
        pos += 1

    pygame.quit()


if __name__ == '__main__':
    test_level = "___M____MGM________M_M______M____L___G____M____L__G__GM__L____ML__G___G___L___G__G___M__L___G____M__F"
    test_sample = '0000000010000000000000000000000020010000000000200101000020000020100010000200010100000002001000000001'
    start(test_level, test_sample)
