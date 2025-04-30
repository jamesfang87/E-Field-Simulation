import pygame

# UI/visual constants
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
    def __init__(self, screen, visualizer=None):
        self.screen = screen
        self.visualizer = visualizer
        self.font = pygame.font.SysFont("Arial", FONT_SIZE)
        # Expose constants
        self.INFO_PANEL_HEIGHT = INFO_PANEL_HEIGHT
        self.SIMULATION_BG_COLOR = SIMULATION_BG_COLOR
        self.test_button_rect = TEST_BUTTON_RECT

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
            status = "Placing: " + ("Positive (+) [p]" if selected_type else "Negative (-) [n]")
        elif mode == MODE_EDIT and selected_charge:
            status = (
                f"Selected: {'+' if selected_charge.charge > 0 else '-'}"
                f"{abs(selected_charge.charge)} nC"
            )
        if status:
            self._blit_text(status, 20, 40)

        # Instructions
        if mode == MODE_NORMAL:
            instr = ["i: Insert  |  e: Edit  |  ESC: Normal"]
        elif mode == MODE_INSERT:
            instr = ["Click: Place  |  p/n: Change Type  |  ESC: Exit"]
        else:
            instr = ["Drag: Move  |  d: Delete  |  t: Toggle  |  ESC: Exit"]
        y = 70
        for line in instr:
            self._blit_text(line, 20, y)
            y += FONT_SIZE + 2

        # Draw Test Point button
        self.draw_button(self.test_button_rect, "Test Point")

    def draw_insert_preview(self, mode, selected_type):
        # Preview new charge icon in insert mode
        if mode != MODE_INSERT or not self.visualizer:
            return
        _, my = pygame.mouse.get_pos()
        if my > INFO_PANEL_HEIGHT:
            self.visualizer.draw_charge_preview(selected_type)

    def draw_test_window(self, test_window):
        # Overlay test-window popup
        test_window.draw(self.screen)
        pygame.display.flip()

    def draw_button(self, rect, text):
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
