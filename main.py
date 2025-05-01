import math
import random

import pygame

from charge import Charge
from charge_visualizer import ChargeVisualizer
from physics import calculate_electric_field
from test_user_win import TestUserWindow
from ui_manager import UIManager

# Mode constants
MODE_NORMAL = 0
MODE_INSERT = 1
MODE_EDIT = 2

NUM_CHARGES = 4


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 820))
        pygame.display.set_caption("E-field sim")

        # Core components
        self.visualizer = ChargeVisualizer(self.screen)
        self.ui = UIManager(self.screen)

        # Simulation state
        self.mode = MODE_NORMAL
        self.selected_polarity = True  # True = positive

        self.charges = []
        for _ in range(NUM_CHARGES):
            # Use a random distribution to gen positions of charges
            x = round(random.gauss(600, 150), 2)
            y = round(random.gauss(400, 150), 2)
            # randomly choose +5 or -5
            q = 5 if random.choice((True, False)) else -5
            self.charges.append(Charge(x, y, q))
        self.active_charge = None
        self.selected_charge = None
        self.test_window = None

    def _clamp(self, charge):
        charge.x = max(
            charge.radius,
            min(self.screen.get_width() - charge.radius, charge.x),
        )
        charge.y = max(
            self.ui.INFO_PANEL_HEIGHT + charge.radius,
            min(self.screen.get_height() - charge.radius, charge.y),
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Test window interaction delegated to UI
            if self.test_window and self.test_window.active:
                self.test_window.handle_event(event)
                self.ui.draw_test_window(self.test_window)
                continue

            if event.type == pygame.KEYDOWN:
                self._handle_key(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_mouse_down(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.active_charge:
                    self.active_charge.dragging = False
                    self.active_charge = None
            elif event.type == pygame.MOUSEMOTION and self.active_charge:
                mx, my = event.pos
                self.active_charge.x = mx + self.active_charge.offset_x
                self.active_charge.y = my + self.active_charge.offset_y
                self._clamp(self.active_charge)

        return True

    def _handle_key(self, event):
        k = event.key
        if k == pygame.K_p:
            self.selected_polarity = True
        elif k == pygame.K_n:
            self.selected_polarity = False
        elif k == pygame.K_i:
            self.mode = MODE_INSERT
        elif k == pygame.K_e:
            self.mode = MODE_EDIT
        elif k == pygame.K_ESCAPE:
            self.mode = MODE_NORMAL
            for c in self.charges:
                c.selected = False
            self.selected_charge = None
        elif k == pygame.K_d and self.mode == MODE_EDIT and self.selected_charge:
            self.charges.remove(self.selected_charge)
            self.selected_charge = None
        elif k == pygame.K_t and self.mode == MODE_EDIT and self.selected_charge:
            self.selected_charge.charge *= -1
            self.selected_charge.color = (
                (255, 0, 0) if self.selected_charge.charge > 0 else (0, 0, 255)
            )

    def _handle_mouse_down(self, pos):
        x, y = pos
        # Test button
        if self.ui.test_button_rect.collidepoint(pos):
            self._spawn_test_point()
            return

        # Edit mode: select & drag
        if self.mode == MODE_EDIT:
            for c in self.charges:
                c.selected = False
            for c in self.charges:
                if (x - c.x) ** 2 + (y - c.y) ** 2 <= c.radius**2:
                    c.selected = True
                    self.selected_charge = c
                    c.dragging = True
                    c.offset_x = c.x - x
                    c.offset_y = c.y - y
                    self._clamp(c)
                    self.active_charge = c
                    return

        # Insert mode: create new charge
        if self.mode == MODE_INSERT:
            new = Charge(x, y, 5 if self.selected_polarity else -5)
            self._clamp(new)
            new.dragging = True
            new.offset_x = 0
            new.offset_y = 0
            self.charges.append(new)
            self.active_charge = new

    def _spawn_test_point(self):
        m = 50
        tx = random.randint(m, self.screen.get_width() - m)
        ty = random.randint(self.ui.INFO_PANEL_HEIGHT + m, self.screen.get_height() - m)
        ex, ey = calculate_electric_field(tx, ty, self.charges)
        mag = math.hypot(ex, ey)
        self.test_window = TestUserWindow(tx, ty, mag, self.charges)

    def draw(self):
        # First draw the grid
        self.ui.draw_grid()

        # Draw the field arrows and charges
        self.ui.draw_field(self.charges)
        self.visualizer.draw_charges(self.charges)

        # Delegate all UI drawing
        self.ui.draw_panel(self.mode, self.selected_charge, self.selected_polarity)
        self.ui.draw_insert_preview(self.mode, self.selected_polarity)

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            running = self.handle_events()
            if not (self.test_window and self.test_window.active):
                self.draw()
            clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    Game().run()
