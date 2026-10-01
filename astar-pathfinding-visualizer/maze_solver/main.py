import pygame
from graph import Graph
from maze import generate_maze
from constants import WIDTH, HEIGHT, ROWS, COLUMNS, PADDING, NODE_SIZE
from a_star import a_star
from buttons import Button

pygame.init()

BACKGROUND = (0x00, 0x17, 0x1F)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze solver")
WINDOW.fill(BACKGROUND)

FONT = pygame.font.SysFont("arial", 35)
TEXT_COLOR = (255, 255, 255)
SMALL_FONT = pygame.font.SysFont("verdana", 19)

def draw_heading():
    text_surface = FONT.render("Shortest PathFinder using A* Algorithm", True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, PADDING // 3))
    WINDOW.blit(text_surface, text_rect)

def draw_legend():
    start_color = (0, 255, 0)
    end_color = (255, 40, 0)
    reset_color = (255, 40, 0)
    search_color = (0, 168, 232)
    demo_color = (0, 192, 65)

    square_size = NODE_SIZE // 1.2
    rect_width = NODE_SIZE * 1.9
    rect_height = NODE_SIZE * 0.79

    x = PADDING *2
    y = HEIGHT - NODE_SIZE *2.4

    pygame.draw.rect(WINDOW, start_color, (x, y, square_size, square_size))
    start_text = SMALL_FONT.render(" Starting Point", True, TEXT_COLOR)
    WINDOW.blit(start_text, (x + square_size + 5, y - 2))
    x += 170  

    x+= 20

    pygame.draw.rect(WINDOW, end_color, (x, y, square_size, square_size))
    end_text = SMALL_FONT.render(" End Point", True, TEXT_COLOR)
    WINDOW.blit(end_text, (x + square_size + 5, y - 2))
    x += 160  

    pygame.draw.rect(WINDOW, reset_color, (x, y, rect_width, rect_height))
    reset_text = SMALL_FONT.render(" Reset", True, TEXT_COLOR)
    WINDOW.blit(reset_text, (x + rect_width + 5, y - 2))
    x += 150

    x+=5

    pygame.draw.rect(WINDOW, search_color, (x, y, rect_width, rect_height))
    search_text = SMALL_FONT.render(" FindShortest path", True, TEXT_COLOR)
    WINDOW.blit(search_text, (x + rect_width + 5, y - 2))
    x += 210

    x+= 35

    pygame.draw.rect(WINDOW, demo_color, (x, y, rect_width, rect_height))
    demo_text = SMALL_FONT.render(" Anime Walls", True, TEXT_COLOR)
    WINDOW.blit(demo_text, (x + rect_width + 5, y - 2))


def get_clicked_pos(pos):
    x, y = pos
    row = (y - PADDING) // NODE_SIZE
    col = (x - PADDING) // NODE_SIZE
    return row, col

def main():
    btn_size = (NODE_SIZE * 3, NODE_SIZE)

    clear_btn_color = (0xFF, 0x28, 0x00)
    maze_btn_color = (0x00, 0xC0, 0x41)
    search_btn_color = (0x00, 0xA8, 0xE8)

    graph = Graph(ROWS, COLUMNS)

    clear_btn = Button(
        clear_btn_color, 
        PADDING * 5.4, 
        NODE_SIZE * 2.7, 
        btn_size, graph.clear)
    clear_btn.draw(WINDOW)

    maze_btn = Button(
        maze_btn_color,
        WIDTH - NODE_SIZE * 25.2,
        NODE_SIZE * 2.7,
        btn_size,
        lambda: generate_maze(graph, lambda: graph.draw(WINDOW)),
    )
    maze_btn.draw(WINDOW)

    search_btn = Button(
        search_btn_color,
        (WIDTH - 2 * PADDING) / 1.82,
        NODE_SIZE * 2.7,
        btn_size,
        lambda: a_star(
            graph,
            graph.get_start_node(),
            graph.get_end_node(),
            lambda: graph.draw(WINDOW),
        ),
    )
    search_btn.draw(WINDOW)

    running = True
    start_clicked = end_clicked = False
    has_searched = False

    while running:
        draw_heading()
        graph.draw(WINDOW)
        draw_legend()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            alt_down = pygame.key.get_mods() & pygame.KMOD_ALT

            if event.type == pygame.MOUSEBUTTONDOWN:
                if clear_btn.handle_event(event):
                    has_searched = False
                if maze_btn.handle_event(event):
                    has_searched = False
                if search_btn.handle_event(event):
                    has_searched = True

                left_mouse_clicked = event.button == 1

                if left_mouse_clicked:
                    pos = event.pos
                    graph_coordinate = get_clicked_pos(pos)

                    if graph.is_start(graph_coordinate):
                        start_clicked = True
                    elif graph.is_end(graph_coordinate):
                        end_clicked = True
                    else:
                        graph.toggle_wall(graph_coordinate)

            elif event.type == pygame.MOUSEBUTTONUP:
                start_clicked = False
                end_clicked = False

            elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
                current = event.pos
                pos = get_clicked_pos(current)

                if start_clicked and not graph.is_wall(pos) and not graph.is_end(pos):
                    graph.update_start(pos)
                    if has_searched:
                        a_star(graph, graph.get_start_node(), graph.get_end_node())
                elif end_clicked and not graph.is_wall(pos) and not graph.is_start(pos):
                    graph.update_end(pos)
                    if has_searched:
                        a_star(graph, graph.get_start_node(), graph.get_end_node())
                elif not graph.is_start(pos) and not graph.is_end(pos):
                    if alt_down:
                        graph.make_empty(pos)
                    else:
                        graph.make_wall(pos)

    pygame.quit()

main()
