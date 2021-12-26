import os
import random
import sys
from collections import defaultdict, deque
from copy import deepcopy
import pygame as pg

SIZE = WIDTH, HEIGHT = 800, 600  # the width and height of our screen
BACKGROUND_COLOR = pg.Color('white')  # The background colod of our window
FPS = 24  # Frames per second


class Solution:
    def __init__(self, data, modified=False, do_splitlines=True, split_char=None):
        if do_splitlines:
            data = data.splitlines()
        if split_char:
            data = [row.split(split_char) for row in data] if do_splitlines else data.split(split_char)
        self.data = data
        self.modified = modified

    def solve(self, nr=None):
        pg.init()
        # getting the screen of the specified size
        screen = pg.display.set_mode(SIZE)
        font = pg.font.SysFont('OpenSans', 72)
        # getting the pg clock for handling fps
        clock = pg.time.Clock()

        h = len(self.data)
        w = len(self.data[0])
        CELL_WIDTH = WIDTH / w
        CELL_HEIGHT = HEIGHT / h
        self.data = [list(row) for row in self.data]
        print('--INITIAL--')
        state = self.data
        self.dump(state)
        finished = False
        i = 1
        while True:
            moving = False

            # getting the events
            for event in pg.event.get():
                # if the event is quit means we clicked on the close window button
                if event.type == pg.QUIT:
                    # quit the game
                    pg.quit()
                    sys.exit(0)

            clock.tick(FPS)
            # filling the screen with background color
            screen.fill(BACKGROUND_COLOR)

            if not finished:
                new_state = [['.'] * w for _ in range(h)]
                for y in range(h):
                    for x in range(w):
                        c = state[y][x]
                        if c == '>':
                            if state[y][(x + 1) % w] == '.':
                                new_state[y][(x + 1) % w] = '>'
                                moving = True
                            else:
                                new_state[y][x] = '>'
                for y in range(h):
                    for x in range(w):
                        c = state[y][x]
                        if c == 'v':
                            if state[(y+1) % h][x] != 'v' and new_state[(y+1) % h][x] == '.':
                                new_state[(y+1) % h][x] = 'v'
                                moving = True
                            else:
                                new_state[y][x] = 'v'
                state = new_state



            for y in range(h):
                for x in range(w):
                    if state[y][x] == '>':
                        pg.draw.polygon(screen, pg.Color('red'), [[x*CELL_WIDTH, y*CELL_HEIGHT], [(x+1)*CELL_WIDTH, y*CELL_HEIGHT+(CELL_HEIGHT/2)], [x * CELL_WIDTH, (y+1)*CELL_HEIGHT]])
                    if state[y][x] == 'v':
                        pg.draw.polygon(screen, pg.Color('blue'), [[x*CELL_WIDTH, y*CELL_HEIGHT], [(x+1)*CELL_WIDTH, y*CELL_HEIGHT], [x * CELL_WIDTH + CELL_WIDTH / 2, (y+1)*CELL_HEIGHT]])
            text = font.render(f"{i}", False, pg.Color('black'))
            screen.blit(text, (WIDTH // 2 - (text.get_width() // 2), 5, text.get_width(), 30))

            if moving:
                i += 1
            else:
                finished = True

            pg.display.flip()



    def dump(self, grid, i=None):
        if i is not None:
            print(f"After step {i}")
        for row in grid:
            print(''.join(row))
        print()


if __name__ == '__main__':
    script = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if '-' in script:
        script = script.split('-')[0]

    DEV = True
    PART2 = False
    SPLIT_LINES = True
    SPLIT_CHAR = None

    with open(f'{script}{"-dev" if DEV else ""}.txt') as f:
        s = Solution(f.read().strip(), PART2, SPLIT_LINES, SPLIT_CHAR)
        print(s.solve())
