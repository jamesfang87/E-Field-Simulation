import pygame


class TestUserWindow:
    def __init__(self, x, y, correct_answer, charges):
        self.rect = pygame.Rect(200, 100, 800, 500)  # Larger window
        self.active = True
        self.input_text = ""
        self.correct_answer = correct_answer
        self.font = pygame.font.SysFont("Arial", 28)
        self.message = ""
        self.test_point = (x, y)
        self.charges = charges  # Store charges reference
        self.close_button = pygame.Rect(
            self.rect.right - 40, self.rect.y + 10, 30, 30
        )

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.submit_button.collidepoint(event.pos):
                self.check_answer()
            elif self.close_button.collidepoint(event.pos):
                self.active = False

    def check_answer(self):
        try:
            user_answer = float(self.input_text)
            margin = 0.05  # 5% margin
            lower = self.correct_answer * (1 - margin)
            upper = self.correct_answer * (1 + margin)

            if lower <= user_answer <= upper:
                self.message = "Correct! Well done!"
            else:
                self.message = f"Incorrect. Answer: {self.correct_answer:.2e}"
        except ValueError:
            self.message = "Invalid input. Enter a number."

    def draw(self, screen):
        # Window background
        pygame.draw.rect(screen, (40, 40, 40), self.rect)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 3)

        # Close button (X)
        pygame.draw.rect(screen, (255, 0, 0), self.close_button)
        close_text = self.font.render("X", True, (255, 255, 255))
        screen.blit(
            close_text, (self.close_button.x + 8, self.close_button.y + 2)
        )

        # Content layout
        y_pos = self.rect.y + 20

        # Test point coordinates
        coord_text = self.font.render(
            f"Test Point: ({self.test_point[0]}, {self.test_point[1]})",
            True,
            (255, 255, 255),
        )
        screen.blit(coord_text, (self.rect.x + 20, y_pos))
        y_pos += 40

        # Charge information header
        header_text = self.font.render(
            "Charges in Simulation:", True, (255, 255, 255)
        )
        screen.blit(header_text, (self.rect.x + 20, y_pos))
        y_pos += 40

        # List all charges
        for i, charge in enumerate(self.charges):
            charge_text = self.font.render(
                f"Charge {i+1}: ({charge.x}, {charge.y}) - "
                f"{'+' if charge.charge > 0 else '-'}{abs(charge.charge)} nC",
                True,
                (255, 255, 255),
            )
            screen.blit(charge_text, (self.rect.x + 40, y_pos))
            y_pos += 35

        # Input field
        y_pos += 20
        input_rect = pygame.Rect(self.rect.x + 50, y_pos, 700, 40)
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)
        text_surface = self.font.render(self.input_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        y_pos += 60

        # Submit button
        self.submit_button = pygame.Rect(self.rect.centerx - 50, y_pos, 100, 40)
        pygame.draw.rect(screen, (0, 150, 0), self.submit_button)
        submit_text = self.font.render("Submit", True, (255, 255, 255))
        screen.blit(
            submit_text, (self.submit_button.x + 10, self.submit_button.y + 5)
        )
        y_pos += 60

        # Message display
        if self.message:
            msg_color = (
                (0, 255, 0) if "Correct" in self.message else (255, 0, 0)
            )
            message_surface = self.font.render(self.message, True, msg_color)
            screen.blit(message_surface, (self.rect.x + 20, y_pos))
