import math

import pygame


class Charge:
    # Default charge magnitudes
    DEFAULT_POSITIVE_CHARGE = 5
    DEFAULT_NEGATIVE_CHARGE = -5

    def __init__(self, x, y, charge):
        self.charge = charge
        self.x = x
        self.y = y

        # visulation info
        self.radius = 15
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False
        self.selected = False  # Track if charge is selected

        if charge > 0:
            self.color = (255, 0, 0)
        else:
            self.color = (0, 0, 255)

    def get_charge(self):
        return self.charge

    def get_pos(self):
        return self.x, self.y

    def get_dist(self, x, y):
        return math.dist([self.x, self.y], [x, y])

    def draw(self, screen):
        """Draw the charge with selection indicator if selected"""
        pos = (int(self.x), int(self.y))

        # Draw the charge circle
        pygame.draw.circle(screen, self.color, pos, self.radius)

        # Draw selection indicator if selected
        if self.selected:
            # Draw a circle around the charge to indicate selection
            selection_color = (0, 255, 0)  # Green selection ring
            pygame.draw.circle(
                screen, selection_color, pos, self.radius + 5, 2
            )  # 2 pixel width outline
