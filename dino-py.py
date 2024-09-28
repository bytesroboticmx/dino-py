import curses
import random
import time

class Dino:
    TIMER_RANGE = 4

    def __init__(self, screen):
        self.screen = screen
        self.timer = 0
        self.bush_pos = -10
        self.jumping = False
        self.jump_timer = 0

    def start(self):
        while True:
            self.timer = 0 if self.timer >= self.TIMER_RANGE else self.timer + 1

            key = self.screen.getch()

            if key == ord('q'):
                break

            self.draw()
            self.screen.refresh()
            time.sleep(0.06)  # 60 ms delay

    def jump(self):
        self.jumping = True
        self.jump_timer = int(self.TIMER_RANGE * 2.4)

    def draw(self):
        self.screen.clear()
        self.draw_terrain()
        self.draw_bush()
        self.draw_dino()

    def draw_terrain(self):
        height, width = self.screen.getmaxyx()
        for i in range(width):
            self.screen.addstr(height - 1, i, '█')

    def draw_bush(self):
        height, width = self.screen.getmaxyx()

        self.bush_pos -= 3

        if self.bush_pos <= -5:
            self.bush_pos = width + random.randint(0, width)

        if self.bush_pos <= width - 5:
            y = height - 1
            try:
                self.screen.addstr(y - 4, self.bush_pos, "▄█ █▄")
                self.screen.addstr(y - 3, self.bush_pos, "██ ██")
                self.screen.addstr(y - 2, self.bush_pos + 1, "███")
                self.screen.addstr(y - 1, self.bush_pos + 1, "███")
            except curses.error:
                pass

    def draw_dino(self):
        height, _ = self.screen.getmaxyx()
        pos_y = height - 12
        pos_x = 5

        if self.jumping:
            pos_y -= 4
            self.jump_timer -= 1

            if self.jump_timer <= 0:
                self.jumping = False

        # Draw the dinosaur's body
        dino_art = [
            "         ▄███████▄",
            "         ██▄██████",
            "         █████████",
            "         ██████▄▄ ",
            "        ██████   ",
            " ▌     ███████▄▄▄",
            " ██▄  ████████  █",
            "  ████████████   ",
            "   █████████     ",
        ]

        for i, line in enumerate(dino_art):
            self.screen.addstr(pos_y + i, pos_x, line)

        # Legs movement
        if self.jumping:
            self.screen.addstr(pos_y + len(dino_art), pos_x, "   ██▄   ██▄")
        else:
            if self.timer < (self.TIMER_RANGE // 2):
                self.screen.addstr(pos_y + len(dino_art), pos_x, "   ██    ██▄")
                self.screen.addstr(pos_y + len(dino_art) + 1, pos_x, "   █▄▄")
            else:
                self.screen.addstr(pos_y + len(dino_art), pos_x, "    ██▄ ██")
                self.screen.addstr(pos_y + len(dino_art) + 1, pos_x, "         █▄▄")

        if 10 < self.bush_pos < 23 and not self.jumping:
            self.jump()


def main(stdscr):
    # Clear screen
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(60)  # Set timeout for getch()

    dino = Dino(stdscr)
    dino.start()


if __name__ == "__main__":
    curses.wrapper(main)
