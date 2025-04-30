import pygame

from charge import Charge
from charge_visualizer import ChargeVisualizer

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("E-field sim")

# Create visualizer
visualizer = ChargeVisualizer(screen)

# Define mode constants
MODE_NORMAL = 0
MODE_INSERT = 1
MODE_EDIT = 2
current_mode = MODE_NORMAL  # Start in normal mode

# Define constants for font
FONT_SIZE = 24
font = pygame.font.SysFont(None, FONT_SIZE)

# Create multiple charges
charges = [
    Charge(400, 300, 5),  # Positive charge
    Charge(600, 450, -5),  # Negative charge
    Charge(800, 400, 3),  # Positive charge
    Charge(500, 600, -3),  # Negative charge
]

# Track which charge is being dragged
active_charge = None

# Track selected charge
selected_charge = None

# Track selected charge type for creation
# (True for positive, False for negative)
selected_charge_type = True  # Default to positive
# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                # Press 'p' to select positive chargeWN:
                selected_charge_type = True
            elif event.key == pygame.K_n:
                # Press 'n' to select negative charge
                selected_charge_type = False

            # Mode switching
            elif event.key == pygame.K_i:
                # 'i' key for insert mode
                current_mode = MODE_INSERT
            elif event.key == pygame.K_e:
                # 'e' key for edit mode
                current_mode = MODE_EDIT
            elif event.key == pygame.K_ESCAPE:
                # Escape key for normal mode
                current_mode = MODE_NORMAL
                # Deselect all charges when entering normal mode
                for c in charges:
                    c.selected = False
                selected_charge = None
            elif event.key == pygame.K_d:
                # Delete key to remove charges
                # Only remove charges in edit mode
                if current_mode == MODE_EDIT and selected_charge:
                    charges.remove(selected_charge)
                    active_charge = None
                    selected_charge = None
            elif event.key == pygame.K_t:
                # Toggle charge polarity in edit mode
                if current_mode == MODE_EDIT and selected_charge:
                    # Toggle from positive to negative or vice versa
                    selected_charge.charge = -selected_charge.charge
                    # Update color based on new charge
                    if selected_charge.charge > 0:
                        # Red for positive
                        selected_charge.color = (255, 0, 0)
                    else:
                        # Blue for negative
                        selected_charge.color = (0, 0, 255)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                charge_clicked = False

                # Only in edit mode,
                # check if we clicked on any charge
                if current_mode == MODE_EDIT:
                    # First, deselect all charges
                    for c in charges:
                        c.selected = False

                    # Then check if we clicked on any charge
                    for c in charges:
                        dist = (mouse_x - c.x) ** 2 + (mouse_y - c.y) ** 2
                        if dist <= c.radius**2:
                            # Set the clicked charge as selected
                            c.selected = True
                            selected_charge = c

                            # Only allow dragging in edit mode
                            if current_mode == MODE_EDIT:
                                c.dragging = True
                                active_charge = c
                                # Calculate offset from center to mouse pos
                                c.offset_x = c.x - mouse_x
                                c.offset_y = c.y - mouse_y
                            charge_clicked = True
                            break

                # In insert mode, create a new charge when clicking
                if current_mode == MODE_INSERT and not charge_clicked:
                    if selected_charge_type:
                        new_charge = Charge(mouse_x, mouse_y, 5)
                    else:
                        new_charge = Charge(mouse_x, mouse_y, -5)

                    # Start dragging the new charge (only in insert mode)
                    new_charge.dragging = True
                    active_charge = new_charge
                    charges.append(new_charge)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if active_charge:
                    active_charge.dragging = False
                    active_charge = (
                        None  # Clear active charge but keep selection
                    )

        elif event.type == pygame.MOUSEMOTION:
            # Update position of dragged charge
            if active_charge:
                mouse_x, mouse_y = event.pos
                active_charge.x = mouse_x + active_charge.offset_x
                active_charge.y = mouse_y + active_charge.offset_y

    # Draw background
    screen.fill((255, 255, 255))  # White background

    # Display current mode
    mode_texts = {
        MODE_NORMAL: "Mode: Normal (Esc)",
        MODE_INSERT: "Mode: Insert (i)",
        MODE_EDIT: "Mode: Edit (e)",
    }
    mode_text = mode_texts[current_mode]
    mode_surface = font.render(mode_text, True, (0, 0, 0))
    screen.blit(mode_surface, (20, 10))

    # Display second line of information for all modes
    second_line_text = ""
    if current_mode == MODE_NORMAL:
        second_line_text = "View mode - no interaction with charges"
    elif current_mode == MODE_INSERT:
        # In insert mode, display the selected charge type
        second_line_text = (
            "Selected: Positive Charge (p)"
            if selected_charge_type
            else "Selected: Negative Charge (n)"
        )
    else:  # edit mode
        second_line_text = "Selected Charge: " + (
            "None"
            if not selected_charge
            else ("Positive" if selected_charge.charge > 0 else "Negative")
        )

    second_line_surface = font.render(second_line_text, True, (0, 0, 0))
    screen.blit(second_line_surface, (20, 40))

    # Display instructions based on mode
    if current_mode == MODE_NORMAL:
        instructions = "Press 'i' for insert mode, 'e' for edit mode"
    elif current_mode == MODE_INSERT:
        instructions = "Click anywhere to place charge. \
                        Press 'p' for positive, 'n' for negative."
    else:  # edit mode
        instructions = "Click and drag charges to move them. \
                        Press 'd' to remove selected charge, \
                        't' to toggle charge polarity"

    instruction_surface = font.render(instructions, True, (0, 0, 0))
    screen.blit(instruction_surface, (20, 70))

    # Use visualizer to draw charge preview in insert mode
    if current_mode == MODE_INSERT:
        visualizer.draw_charge_preview(selected_charge_type, active_charge)

    # Use visualizer to draw all charges
    visualizer.draw_charges(charges)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
