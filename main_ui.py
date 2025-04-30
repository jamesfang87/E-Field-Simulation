import pygame

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


class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", FONT_SIZE)
        self.test_button_rect = TEST_BUTTON_RECT

    def draw_panel(self, mode, selected_charge, selected_type):
        # Background
        pygame.draw.rect(
            self.screen,
            PANEL_BG_COLOR,
            (0, 0, self.screen.get_width(), INFO_PANEL_HEIGHT),
        )
        # Mode text
        mode_text = {
            MODE_NORMAL: "Normal Mode (ESC)",
            MODE_INSERT: "Insert Mode (i)",
            MODE_EDIT: "Edit Mode (e)",
        }[mode]
        self._blit_text(mode_text, 20, 10)

        # Status text
        status_text = ""
        if mode == MODE_INSERT:
            status_text = "Placing: " + (
                "Positive (+) [p]" if selected_type else "Negative (-) [n]"
            )
        elif mode == MODE_EDIT and selected_charge:
            status_text = f"Selected: {'+' if selected_charge.charge > 0 else '-'}{abs(selected_charge.charge)} nC"
        if status_text:
            self._blit_text(status_text, 20, 40)

        # Instructions
        instructions = []
        if mode == MODE_NORMAL:
            instructions = [
                "i: Insert Mode  |  e: Edit Mode  |  ESC: Normal Mode"
            ]
        elif mode == MODE_INSERT:
            instructions = [
                "Click: Place Charge  |  p/n: Change Type  |  ESC: Exit Insert"
            ]
        elif mode == MODE_EDIT:
            instructions = [
                "Drag: Move  |  d: Delete  |  t: Toggle  |  ESC: Exit Edit"
            ]
        y = 70
        for line in instructions:
            self._blit_text(line, 20, y)
            y += FONT_SIZE + 2

        # Test button
        color = (
            TEST_BUTTON_HOVER_COLOR
            if self.test_button_rect.collidepoint(pygame.mouse.get_pos())
            else TEST_BUTTON_COLOR
        )
        pygame.draw.rect(self.screen, color, self.test_button_rect)
        txt_surf = self.font.render("Test Point", True, TEXT_COLOR)
        self.screen.blit(
            txt_surf,
            (
                self.test_button_rect.centerx - txt_surf.get_width() // 2,
                self.test_button_rect.centery - txt_surf.get_height() // 2,
            ),
        )

    def _blit_text(self, text, x, y):
        surf = self.font.render(text, True, TEXT_COLOR)
        self.screen.blit(surf, (x, y))
