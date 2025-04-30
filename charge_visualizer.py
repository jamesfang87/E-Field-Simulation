import math

import pygame


class ChargeVisualizer:
    def __init__(self, screen):
        self.screen = screen
        self.grid_spacing = 50  # pixels between arrows
        self.max_arrow_length = 40  # pixels
        self.arrow_color = (0, 255, 0)  # Green arrows

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

    def calculate_electric_field(self, x, y, charges):
        k = 8.988e9  # N·m²/C² (scaled down for visualization)
        total_ex = 0
        total_ey = 0

        for charge in charges:
            q = charge.charge
            dx = x - charge.x
            dy = y - charge.y
            r_sq = dx**2 + dy**2

            if r_sq == 0:
                continue  # avoid division by zero

            r = math.sqrt(r_sq)
            e_mag = k * abs(q) / r_sq
            direction = 1 if q > 0 else -1
            total_ex += direction * e_mag * dx / r
            total_ey += direction * e_mag * dy / r

        return total_ex, total_ey

    def calculate_voltage(self, x, y, charges):
        k = 8.988e9  # Coulomb's constant
        total_voltage = 0
        for charge in charges:
            q = charge.charge
            r = math.dist([x, y], [charge.x, charge.y])
            if r > 0:  # Avoid division by zero
                total_voltage += k * q / r
        return total_voltage

    def draw_arrow(self, x, y, dx, dy):
        # Cap the arrow length
        length = math.hypot(dx, dy)
        if length > self.max_arrow_length:
            scale = self.max_arrow_length / length
            dx *= scale
            dy *= scale

        # Arrow shaft
        end_x = x + dx
        end_y = y + dy
        pygame.draw.line(
            self.screen, self.arrow_color, (x, y), (end_x, end_y), 2
        )

        # Arrow head
        arrow_size = 6
        angle = math.atan2(dy, dx)
        p1 = (
            end_x - arrow_size * math.cos(angle - math.pi / 6),
            end_y - arrow_size * math.sin(angle - math.pi / 6),
        )
        p2 = (
            end_x - arrow_size * math.cos(angle + math.pi / 6),
            end_y - arrow_size * math.sin(angle + math.pi / 6),
        )
        pygame.draw.polygon(
            self.screen, self.arrow_color, [(end_x, end_y), p1, p2]
        )
