import math
import random

import pygame

from charge import Charge
from charge_visualizer import ChargeVisualizer
from main_ui import UIManager
from test_user import TestUserWindow

# Constants
INFO_PANEL_HEIGHT = 120
PANEL_BG_COLOR = (0, 0, 0)
SIMULATION_BG_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 24
TEST_BUTTON_RECT = pygame.Rect(1000, 10, 180, 40)
TEST_BUTTON_COLOR = (50, 50, 50)
TEST_BUTTON_HOVER_COLOR = (70, 70, 70)

# Mode constants
MODE_NORMAL = 0
MODE_INSERT = 1
MODE_EDIT = 2


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 900))
        pygame.display.set_caption("E-field sim")
        self.visualizer = ChargeVisualizer(self.screen)
        self.ui = UIManager(self.screen)
        self.mode = MODE_NORMAL
        self.selected_type = True  # True for positive
        self.charges = [
            Charge(400, 300 + INFO_PANEL_HEIGHT, -5),
            Charge(600, 450 + INFO_PANEL_HEIGHT, -5),
            Charge(800, 400 + INFO_PANEL_HEIGHT, -3),
            Charge(500, 600 + INFO_PANEL_HEIGHT, -3),
        ]
        self.active = None
        self.selected = None
        self.test_window = None

    def clamp(self, c):
        c.x = max(c.radius, min(self.screen.get_width() - c.radius, c.x))
        c.y = max(
            INFO_PANEL_HEIGHT + c.radius,
            min(self.screen.get_height() - c.radius, c.y),
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.test_window and self.test_window.active:
                self.test_window.handle_event(event)
                self.test_window.draw(self.screen)
                pygame.display.flip()
                continue

            if event.type == pygame.KEYDOWN:
                self._handle_key(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.active:
                    self.active.dragging = False
                    self.active = None
            elif event.type == pygame.MOUSEMOTION:
                if self.active:
                    mx, my = event.pos
                    self.active.x = mx + self.active.offset_x
                    self.active.y = my + self.active.offset_y
                    self.clamp(self.active)
        return True

    def _handle_key(self, event):
        key = event.key
        if key == pygame.K_p:
            self.selected_type = True
        elif key == pygame.K_n:
            self.selected_type = False
        elif key == pygame.K_i:
            self.mode = MODE_INSERT
        elif key == pygame.K_e:
            self.mode = MODE_EDIT
        elif key == pygame.K_ESCAPE:
            self.mode = MODE_NORMAL
            for c in self.charges:
                c.selected = False
            self.selected = None
        elif key == pygame.K_d and self.mode == MODE_EDIT and self.selected:
            self.charges.remove(self.selected)
            self.selected = None
        elif key == pygame.K_t and self.mode == MODE_EDIT and self.selected:
            self.selected.charge *= -1
            self.selected.color = (
                (255, 0, 0) if self.selected.charge > 0 else (0, 0, 255)
            )

    def _handle_click(self, pos):
        x, y = pos
        # Test button
        if self.ui.test_button_rect.collidepoint(pos):
            self._spawn_test()
            return
        # Edit mode selection
        if self.mode == MODE_EDIT:
            for c in self.charges:
                c.selected = False
            for c in self.charges:
                if (x - c.x) ** 2 + (y - c.y) ** 2 <= c.radius**2:
                    c.selected = True
                    self.selected = c
                    c.dragging = True
                    c.offset_x = c.x - x
                    c.offset_y = c.y - y
                    self.clamp(c)
                    self.active = c
                    return
        # Insert mode creation
        if self.mode == MODE_INSERT:
            new = Charge(x, y, 5 if self.selected_type else -5)
            self.clamp(new)
            new.dragging = True
            new.offset_x = 0
            new.offset_y = 0
            self.charges.append(new)
            self.active = new

    def _spawn_test(self):
        margin = 50
        tx = random.randint(margin, self.screen.get_width() - margin)
        ty = random.randint(
            INFO_PANEL_HEIGHT + margin, self.screen.get_height() - margin
        )
        ex, ey = self.visualizer.calculate_electric_field(tx, ty, self.charges)
        mag = math.hypot(ex, ey)
        self.test_window = TestUserWindow(tx, ty, mag, self.charges)

    def draw(self):
        self.screen.fill(SIMULATION_BG_COLOR)
        # field
        for x in range(
            self.visualizer.grid_spacing // 2,
            self.screen.get_width(),
            self.visualizer.grid_spacing,
        ):
            for y in range(
                INFO_PANEL_HEIGHT + self.visualizer.grid_spacing // 2,
                self.screen.get_height(),
                self.visualizer.grid_spacing,
            ):
                ex, ey = self.visualizer.calculate_electric_field(
                    x, y, self.charges
                )
                if ex or ey:
                    self.visualizer.draw_arrow(x, y, ex * 0.00005, ey * 0.00005)
        # charges
        self.visualizer.draw_charges(self.charges)
        # UI
        self.ui.draw_panel(self.mode, self.selected, self.selected_type)
        # insert preview
        if self.mode == MODE_INSERT:
            _, my = pygame.mouse.get_pos()
            if my > INFO_PANEL_HEIGHT:
                self.visualizer.draw_charge_preview(self.selected_type)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            if not (self.test_window and self.test_window.active):
                self.draw()
        pygame.quit()


if __name__ == "__main__":
    Game().run()
