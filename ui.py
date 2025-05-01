import math

import pygame

from physics import calculate_electric_field

# UI/visual constants
INFO_PANEL_HEIGHT = 120
PANEL_BG_COLOR = (0, 0, 0)
SIMULATION_BG_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 24
TEST_BUTTON_RECT = pygame.Rect(1000, 10, 180, 40)
TEST_BUTTON_COLOR = (50, 50, 50)
TEST_BUTTON_HOVER_COLOR = (70, 70, 70)

GRID_COLOR = (50, 50, 50)  # very dark grey on black
GRID_SPACING = 50  # pixels between lines

# Mode constants
MODE_NORMAL = 0
MODE_INSERT = 1
MODE_EDIT = 2


class UI:
    def __init__(self, screen, visualizer=None):
        self.screen = screen
        self.visualizer = visualizer
        self.font = pygame.font.SysFont("Arial", FONT_SIZE)
        self.test_button_rect = TEST_BUTTON_RECT
        self.max_arrow_length = 40  # pixels
        self.arrow_color = (0, 255, 0)  # Green arrows
        self.INFO_PANEL_HEIGHT = INFO_PANEL_HEIGHT

    def draw_panel(self, mode, selected_charge, selected_type):
        # Background panel
        pygame.draw.rect(
            self.screen,
            PANEL_BG_COLOR,
            (0, 0, self.screen.get_width(), INFO_PANEL_HEIGHT),
        )

        # Mode label
        mode_text = {
            MODE_NORMAL: "Normal Mode (ESC)",
            MODE_INSERT: "Insert Mode (i)",
            MODE_EDIT: "Edit Mode (e)",
        }[mode]
        self._blit_text(mode_text, 20, 10)

        # Status label
        status = ""
        if mode == MODE_INSERT:
            status = "Placing: " + (
                "Positive (+) [p]" if selected_type else "Negative (-) [n]"
            )
        elif mode == MODE_EDIT and selected_charge:
            status = (
                f"Selected: {'+' if selected_charge.charge > 0 else '-'}"
                f"{abs(selected_charge.charge)} mC"
            )
        if status:
            self._blit_text(status, 20, 40)

        # Instructios
        instr = None
        if mode == MODE_NORMAL:
            instr = "i: Insert  |  e: Edit  |  ESC: Normal"
        elif mode == MODE_INSERT:
            instr = "Click: Place  |  p/n: Change Type  |  ESC: Exit"
        else:
            instr = "Drag: Move  |  d: Delete  |  t: Toggle  |  ESC: Exit"
        self._blit_text(instr, 20, 70)

        # Draw Test Point button
        self._draw_button(self.test_button_rect, "Test Point")

    def draw_insert_preview(self, selected_polarity):
        _, my = pygame.mouse.get_pos()
        if my > INFO_PANEL_HEIGHT:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            preview_color = (255, 0, 0) if selected_polarity else (0, 0, 255)
            pygame.draw.circle(
                self.screen, preview_color, (mouse_x, mouse_y), 15, 2
            )  # Draw outline only

    def draw_test_window(self, test_window):
        # Overlay test-window popup
        test_window.draw(self.screen)
        pygame.display.flip()

    def _draw_button(self, rect, text):
        # Draw a button with perfectly centered text
        is_hover = rect.collidepoint(pygame.mouse.get_pos())
        color = TEST_BUTTON_HOVER_COLOR if is_hover else TEST_BUTTON_COLOR
        pygame.draw.rect(self.screen, color, rect)
        label_surf = self.font.render(text, True, TEXT_COLOR)
        label_rect = label_surf.get_rect()
        # Manually center text
        label_rect.x = rect.x + (rect.width - label_rect.width) // 2
        label_rect.y = rect.y + (rect.height - label_rect.height) // 2
        self.screen.blit(label_surf, label_rect)

    def _blit_text(self, text, x, y):
        surf = self.font.render(text, True, TEXT_COLOR)
        self.screen.blit(surf, (x, y))

    def draw_grid(self):
        # first fill the backgrund
        self.screen.fill(SIMULATION_BG_COLOR)
        info_h = INFO_PANEL_HEIGHT
        sim_rect = pygame.Rect(
            0,
            info_h,
            self.screen.get_width(),
            self.screen.get_height() - info_h,
        )
        pygame.draw.rect(self.screen, SIMULATION_BG_COLOR, sim_rect)

        # draw directly with a light color
        for x in range(sim_rect.left, sim_rect.right + 1, GRID_SPACING):
            pygame.draw.line(
                self.screen, GRID_COLOR, (x, sim_rect.top), (x, sim_rect.bottom)
            )
        for y in range(sim_rect.top, sim_rect.bottom + 1, GRID_SPACING):
            pygame.draw.line(
                self.screen, GRID_COLOR, (sim_rect.left, y), (sim_rect.right, y)
            )

    def draw_field(self, charges):
        width, height = self.screen.get_size()
        for x in range(0, width, GRID_SPACING):
            for y in range(INFO_PANEL_HEIGHT, height, GRID_SPACING):
                # add half of grid spacing
                d = GRID_SPACING / 2
                ex, ey = calculate_electric_field(x + d, y + d, charges)
                self.draw_arrow(x + d, y + d, ex * 0.05, ey * 0.05)

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
