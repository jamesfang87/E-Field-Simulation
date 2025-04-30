import pygame


class TestUserWindow:
    def __init__(self, x, y, correct_answer, charges, ui_manager=None):
        self.rect = pygame.Rect(200, 100, 800, 500)
        self.active = True
        self.input_text = ""
        self.correct_answer = correct_answer
        self.font = pygame.font.SysFont("Arial", 28)
        self.message = ""
        self.test_point = (x, y)
        self.charges = charges
        # Buttons
        self.close_button = pygame.Rect(self.rect.right - 40, self.rect.y + 10, 30, 30)
        self.submit_button = pygame.Rect(self.rect.centerx - 50, self.rect.bottom - 80, 100, 40)
        self.ui = ui_manager  # optional UIManager for centered draw

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.active = False
            elif event.key == pygame.K_RETURN:
                self.check_answer()
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.submit_button.collidepoint(event.pos):
                self.check_answer()
            elif self.close_button.collidepoint(event.pos):
                self.active = False

    def check_answer(self):
        try:
            user_answer = float(self.input_text)
            margin = 0.05
            lower = self.correct_answer * (1 - margin)
            upper = self.correct_answer * (1 + margin)

            if lower <= user_answer <= upper:
                self.message = "Correct! Well done!"
            else:
                self.message = f"Incorrect. Answer: {self.correct_answer:.2e}"
        except ValueError:
            self.message = "Invalid input. Enter a number."

    def draw(self, screen):
        # Background
        pygame.draw.rect(screen, (40, 40, 40), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 3)

        # Close button
        if self.ui:
            self.ui.draw_button(self.close_button, "X")
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.close_button)
            txt = self.font.render("X", True, (255, 255, 255))
            txt_rect = txt.get_rect(center=self.close_button.center)
            screen.blit(txt, txt_rect)

        # Content
        y = self.rect.y + 20
        coord = f"Calculate the field at: ({self.test_point[0]}, {self.test_point[1]})"
        screen.blit(self.font.render(coord, True, (255, 255, 255)), (self.rect.x + 20, y))
        y += 40
        header = "Charges in Simulation:"
        screen.blit(self.font.render(header, True, (255, 255, 255)), (self.rect.x + 20, y))
        y += 40
        for i, c in enumerate(self.charges):
            info = f"Charge {i+1}: ({c.x}, {c.y}): {'+' if c.charge > 0 else '-'}{abs(c.charge)} nC"
            screen.blit(self.font.render(info, True, (255, 255, 255)), (self.rect.x + 40, y))
            y += 35

        # Input field
        y += 20
        input_rect = pygame.Rect(self.rect.x + 50, y, 700, 40)
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)
        screen.blit(
            self.font.render(self.input_text, True, (255, 255, 255)),
            (input_rect.x + 5, input_rect.y + 5),
        )
        y += 60

        # Submit button
        if self.ui:
            self.ui.draw_button(self.submit_button, "Submit")
        else:
            pygame.draw.rect(screen, (0, 150, 0), self.submit_button)
            txt = self.font.render("Submit", True, (255, 255, 255))
            txt_rect = txt.get_rect(center=self.submit_button.center)
            screen.blit(txt, txt_rect)
        y += 60

        # Message
        if self.message:
            color = (0, 255, 0) if "Correct" in self.message else (255, 0, 0)
            screen.blit(self.font.render(self.message, True, color), (self.rect.x + 20, y))
