import math

import pygame


class ChargeVisualizer:
    def __init__(self, screen):
        self.screen = screen

    def draw_charges(self, charges):
        """Draw all charges in the simulation"""
        for charge in charges:
            charge.draw(self.screen)

    def draw_charge_preview(self, selected_charge_type, active_charge=None):
        """Draw a preview of the charge at the mouse position if in insert mode"""
        if not active_charge:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            preview_color = (255, 0, 0) if selected_charge_type else (0, 0, 255)
            pygame.draw.circle(
                self.screen, preview_color, (mouse_x, mouse_y), 15, 2
            )  # Draw outline only
