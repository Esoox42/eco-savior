import pygame
from config import *
from grid import Grid
from player import Player
from ui import render_ui
from enum import Enum
from infrastructure import EnergyPlant, WasteFactory, House

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Eco-Savior")
clock = pygame.time.Clock()

grid = Grid(GRID_SIZE)
player = Player()

font = pygame.font.Font(None, 18)

class MenuState(Enum):
    NONE = 0
    BUILD = 1
    DELETE = 2

def handle_click(x, y, grid, player):
    global menu_state, selected_cell
    if menu_state == MenuState.NONE:
        infrastructure = grid.cells.get((x, y))
        if infrastructure:
            menu_state = MenuState.DELETE
            selected_cell = (x, y)
        else:
            menu_state = MenuState.BUILD
            selected_cell = (x, y)

def handle_menu_click(pos, grid, player):
    global menu_state, selected_cell
    if menu_state == MenuState.BUILD:
        # Check which button was clicked
        if button_energy.collidepoint(pos):
            if player.spend_money(EnergyPlant().cost):
                grid.build(selected_cell[0], selected_cell[1], EnergyPlant())
        elif button_waste.collidepoint(pos):
            if player.spend_money(WasteFactory().cost):
                grid.build(selected_cell[0], selected_cell[1], WasteFactory())
        elif button_house.collidepoint(pos):
            if player.spend_money(House().cost):
                grid.build(selected_cell[0], selected_cell[1], House())
        menu_state = MenuState.NONE
    elif menu_state == MenuState.DELETE:
        if button_delete.collidepoint(pos):
            infrastructure = grid.cells.get(selected_cell)
            if infrastructure:
                player.gain_money(infrastructure.cost)
                del grid.cells[selected_cell]
        menu_state = MenuState.NONE

# Initialize menu state and buttons
menu_state = MenuState.NONE
selected_cell = None
button_energy = pygame.Rect(WINDOW_WIDTH // 2 - 160, WINDOW_HEIGHT - MENU_BAR_HEIGHT + 10, 100, 30)
button_waste = pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT - MENU_BAR_HEIGHT + 10, 100, 30)
button_house = pygame.Rect(WINDOW_WIDTH // 2 + 60, WINDOW_HEIGHT - MENU_BAR_HEIGHT + 10, 100, 30)
button_delete = pygame.Rect(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT - MENU_BAR_HEIGHT + 10, 100, 30)

# Cache text renders at initialization
button_texts = {
    'energy': font.render("Energy", True, (0, 0, 0)),
    'waste': font.render("Waste", True, (0, 0, 0)),
    'house': font.render("House", True, (0, 0, 0)),
    'delete': font.render("Delete", True, (0, 0, 0))
}

# Add after pygame.init()
start_time = pygame.time.get_ticks()

def draw_tooltip(screen, text, pos, font):
    # Split text into lines and render each line separately
    lines = text.split('\n')
    line_surfaces = [font.render(line, True, (255, 255, 255)) for line in lines]
    
    # Calculate total height and maximum width
    total_height = sum(surface.get_height() for surface in line_surfaces)
    max_width = max(surface.get_width() for surface in line_surfaces)
    
    # Create tooltip rectangle
    tooltip_rect = pygame.Rect(pos[0], pos[1] - total_height - 10, max_width, total_height)
    
    # Ensure tooltip stays within screen bounds
    if tooltip_rect.right > WINDOW_WIDTH:
        tooltip_rect.right = WINDOW_WIDTH - 5
    if tooltip_rect.top < 0:
        tooltip_rect.top = pos[1] + 40
    
    # Draw tooltip background
    pygame.draw.rect(screen, (60, 60, 60), tooltip_rect.inflate(10, 10))
    pygame.draw.rect(screen, (100, 100, 100), tooltip_rect.inflate(10, 10), 2)
    
    # Draw each line
    current_y = tooltip_rect.y
    for surface in line_surfaces:
        screen.blit(surface, (tooltip_rect.x, current_y))
        current_y += surface.get_height()

def get_infrastructure_info(infra_type):
    if infra_type == "energy":
        plant = EnergyPlant()
        return f"Build Energy Plant - Cost: ${plant.cost}\nEnergy: {plant.energy_usage}\nWaste: +{plant.waste_production}"
    elif infra_type == "waste":
        factory = WasteFactory()
        return f"Build Waste Factory - Cost: ${factory.cost}\nEnergy: +{factory.energy_usage}\nWaste: {factory.waste_production}"
    elif infra_type == "house":
        house = House()
        return f"Build House - Cost: ${house.cost}\nEnergy: +{house.energy_usage}\nWaste: +{house.waste_production}"
    return ""

def get_delete_info(infrastructure):
    return f"Delete {infrastructure.name}\nRefund: ${infrastructure.cost}"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if menu_state == MenuState.NONE:
                # Adjust for grid offset when calculating grid coordinates
                grid_x = (mouse_pos[0] - GRID_OFFSET_X) // CELL_SIZE
                grid_y = (mouse_pos[1] - GRID_OFFSET_Y) // CELL_SIZE
                if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                    handle_click(grid_x, grid_y, grid, player)
            else:
                # Handle menu clicks
                handle_menu_click(mouse_pos, grid, player)

    screen.fill((0, 0, 0))
    grid.render(screen)
    game_time = (pygame.time.get_ticks() - start_time) // 1000  # Convert to seconds
    render_ui(screen, player, game_time, font)

    # Render menu buttons based on state
    if menu_state == MenuState.BUILD:
        pygame.draw.rect(screen, (0, 255, 0), button_energy)
        pygame.draw.rect(screen, (0, 255, 0), button_waste)
        pygame.draw.rect(screen, (0, 255, 0), button_house)
        screen.blit(button_texts['energy'], (button_energy.x + 10, button_energy.y + 5))
        screen.blit(button_texts['waste'], (button_waste.x + 10, button_waste.y + 5))
        screen.blit(button_texts['house'], (button_house.x + 10, button_house.y + 5))

        # Check for hover and show tooltips
        mouse_pos = pygame.mouse.get_pos()
        if button_energy.collidepoint(mouse_pos):
            draw_tooltip(screen, get_infrastructure_info("energy"), mouse_pos, font)
        elif button_waste.collidepoint(mouse_pos):
            draw_tooltip(screen, get_infrastructure_info("waste"), mouse_pos, font)
        elif button_house.collidepoint(mouse_pos):
            draw_tooltip(screen, get_infrastructure_info("house"), mouse_pos, font)
    elif menu_state == MenuState.DELETE:
        pygame.draw.rect(screen, (255, 0, 0), button_delete)
        screen.blit(button_texts['delete'], (button_delete.x + 10, button_delete.y + 5))
        
        # Show delete tooltip on hover
        mouse_pos = pygame.mouse.get_pos()
        if button_delete.collidepoint(mouse_pos):
            infrastructure = grid.cells.get(selected_cell)
            if infrastructure:
                draw_tooltip(screen, get_delete_info(infrastructure), mouse_pos, font)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()