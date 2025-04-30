import pygame

from charge import Charge
from charge_visualizer import ChargeVisualizer

# Initialize Pygame
pygame.init()

# Constants
INFO_PANEL_HEIGHT = 120
PANEL_BG_COLOR = (0, 0, 0)
SIMULATION_BG_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 24

# Set up the game window
screen = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("E-field sim")

# Create visualizer
visualizer = ChargeVisualizer(screen)

# Define mode constants
MODE_NORMAL = 0
MODE_INSERT = 1
MODE_EDIT = 2
current_mode = MODE_NORMAL

# Font setup
font = pygame.font.SysFont("Arial", FONT_SIZE)

# Create charges
charges = [
    Charge(400, 300 + INFO_PANEL_HEIGHT, -5),
    Charge(600, 450 + INFO_PANEL_HEIGHT, -5),
    Charge(800, 400 + INFO_PANEL_HEIGHT, -3),
    Charge(500, 600 + INFO_PANEL_HEIGHT, -3),
]

# State variables
active_charge = None
selected_charge = None
selected_charge_type = True


def clamp_charge_position(charge):
    """Keep charges in simulation area"""
    charge.x = max(charge.radius, min(1200 - charge.radius, charge.x))
    charge.y = max(
        INFO_PANEL_HEIGHT + charge.radius, min(900 - charge.radius, charge.y)
    )


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
                                clamp_charge_position(c)
                            charge_clicked = True
                            break

                # In insert mode, create a new charge when clicking
                if current_mode == MODE_INSERT and not charge_clicked:
                    if selected_charge_type:
                        new_charge = Charge(mouse_x, mouse_y, 5)
                    else:
                        new_charge = Charge(mouse_x, mouse_y, -5)

                    clamp_charge_position(new_charge)

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
                clamp_charge_position(active_charge)

            # Drawing
    screen.fill(SIMULATION_BG_COLOR)  # Main background
    pygame.draw.rect(
        screen, PANEL_BG_COLOR, (0, 0, 1200, INFO_PANEL_HEIGHT)
    )  # Info panel

    # Draw electric field
    for x in range(visualizer.grid_spacing // 2, 1200, visualizer.grid_spacing):
        for y in range(
            INFO_PANEL_HEIGHT + visualizer.grid_spacing // 2,
            900,
            visualizer.grid_spacing,
        ):
            ex, ey = visualizer.calculate_electric_field(x, y, charges)
            if ex != 0 or ey != 0:
                visualizer.draw_arrow(x, y, ex * 0.0005, ey * 0.0005)

    # Draw charges
    visualizer.draw_charges(charges)

    # Panel information
    # Mode display
    mode_text = {
        MODE_NORMAL: "Normal Mode (ESC)",
        MODE_INSERT: "Insert Mode (i)",
        MODE_EDIT: "Edit Mode (e)",
    }[current_mode]
    screen.blit(font.render(mode_text, True, TEXT_COLOR), (20, 10))

    # Charge status
    status_text = ""
    if current_mode == MODE_INSERT:
        status_text = "Placing: " + (
            "Positive (+) [p]" if selected_charge_type else "Negative (-) [n]"
        )
    elif current_mode == MODE_EDIT and selected_charge:
        status_text = f"Selected: {'+' if selected_charge.charge > 0 else '-'}"
        status_text += f"{abs(selected_charge.charge)} nC"
    screen.blit(font.render(status_text, True, TEXT_COLOR), (20, 40))

    # Instructions
    instructions = []
    if current_mode == MODE_NORMAL:
        instructions = ["i: Insert Mode  |  e: Edit Mode  |  ESC: Normal Mode"]
    elif current_mode == MODE_INSERT:
        instructions = [
            "Click: Place Charge  |  p/n: Change Type  |  ESC: Exit Insert"
        ]
    elif current_mode == MODE_EDIT:
        instructions = [
            "Drag: Move  |  d: Delete  |  t: Toggle  |  ESC: Exit Edit"
        ]

    # Render instructions
    y_pos = 70
    for line in instructions:
        text_surface = font.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (20, y_pos))
        y_pos += FONT_SIZE + 2

    # Charge preview in insert mode
    if current_mode == MODE_INSERT:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y > INFO_PANEL_HEIGHT:
            visualizer.draw_charge_preview(selected_charge_type)

    pygame.display.flip()

pygame.quit()
