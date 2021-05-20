import pygame


class Mario:
    __mario_image = pygame.image.load('pic/mario.png')

    def __init__(self, x):
        self.x = x

    def get_image(self):
        return self.__mario_image


robot = Mario(1)


def redraw_window(window, state):
    window.fill((89, 17, 17))

    pygame.display.update()


def start(init_state, moves):

    pygame.init()
    clock = pygame.time.Clock()

    window = pygame.display.set_mode((120 * init_state.shape[1], 120 * init_state.shape[0]))

    pygame.display.set_caption("Mario")
    pygame.display.set_icon(robot.get_image())

    pygame.time.delay(2500)
    pygame.quit()
