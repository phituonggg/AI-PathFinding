import sys
from settings import *
from buttons import *
from bfs_class import *
from dfs_class import *
from astar_class import *

from visualize_path_class import *
from maze_class import *


pygame.init()

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'main menu'
        self.algorithm_state = ''
        self.grid_square_length = 24 # The dimensions of each grid square is 24 x 24
        self.load()
        self.start_end_checker = 0
        self.mouse_drag = 0

        # Start and End Nodes Coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None
        
        #Draw Path
        self.check_point=True
        self.astar_bool=False
        self.bfs_bool=False
        self.dfs_bool=False
        self.drawbfs_path=None
        self.drawdfs_path=None
        self.drawastar_path=None
        # Wall Nodes List (list already includes the coordinates of the borders)
        self.wall_pos = wall_nodes_coords_list.copy()
        self.wall_List=[]
        self.player_List=[]

        # Define Main-Menu buttons
        self.bfs_button = Buttons(self, WHITE, 228, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Breadth-First Search')
        self.dfs_button = Buttons(self, WHITE, 448, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Depth-First Search')
        self.astar_button = Buttons(self, WHITE, 668, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'A-Star Search')
        self.start_game_button=Buttons(self, WHITE, 700, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Start Program')

        # Define Grid-Menu buttons
        self.show_winner=Buttons(self,AQUAMARINE,20,55,GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Result')
        self.astar1_button=Buttons(self, AQUAMARINE, 20, 125, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'ASTAR')
        self.dfs1_button = Buttons(self, AQUAMARINE, 20, 195, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'DFS')
        self.bfs1_button = Buttons(self, AQUAMARINE, 20, 265, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'BFS')
        self.start_end_node_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Start/End Node')
        self.wall_node_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT + BUTTON_SPACER, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Wall Node')
        self.reset_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT*2 + BUTTON_SPACER*2, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Reset')
        self.start_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT*3 + BUTTON_SPACER*3, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Visualize Path')
        self.main_menu_button = Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT * 4 + BUTTON_SPACER * 4, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Main Menu')
        self.player_button=Buttons(self, AQUAMARINE, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT * 5 + BUTTON_SPACER * 5, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Player draw')
    def run(self):
        while self.running:
            if self.state == 'main menu':
                self.main_menu_events()
            if self.state == 'grid window':
                self.grid_events()
            if self.state == 'draw S/E' or self.state == 'draw walls':
                self.draw_nodes()
            if self.state == 'start visualizing':
                self.execute_search_algorithm()
            if self.state == 'aftermath':
                self.reset_or_main_menu()
            if self.state=='draw_player':
                self.player_move()
        pygame.quit()
        sys.exit()

#################################### SETUP FUNCTIONS #########################################

##### Loading Images
    def load(self):
        self.main_menu_background = pygame.image.load('logo.png')
        self.grid_background = pygame.image.load('grid_logo.png')

##### Draw Text
    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

##### Setup for Main Menu
    def sketch_main_menu(self):
        self.screen.blit(self.main_menu_background, (0, 0))

        # Draw Buttons
        
        self.start_game_button.draw_button(AQUAMARINE)
        

##### Setup for Grid
    def sketch_hotbar(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, (0, 0, 240, 768), 0)
        #self.screen.blit(self.grid_background, (0, 0))

    def sketch_grid(self):
        # Add borders for a cleaner look
        pygame.draw.rect(self.screen, ALICE, (240, 0, WIDTH, HEIGHT), 0)
        pygame.draw.rect(self.screen, AQUAMARINE, (264, 24, GRID_WIDTH, GRID_HEIGHT), 0)

        # Draw grid
        # There are 52 square pixels across on grid [ WITHOUT BORDERS! ]
        # There are 30 square pixels vertically on grid [ WITHOUT BORDERS! ]
        for x in range(52):
            pygame.draw.line(self.screen, ALICE, (GS_X + x*self.grid_square_length, GS_Y),
                             (GS_X + x*self.grid_square_length, GE_Y))
        for y in range(30):
            pygame.draw.line(self.screen, ALICE, (GS_X, GS_Y + y*self.grid_square_length),
                             (GE_X, GS_Y + y*self.grid_square_length))

    def sketch_grid_buttons(self):
        # Draw buttons
        
        self.start_end_node_button.draw_button(STEELBLUE)
        self.wall_node_button.draw_button(STEELBLUE)
        self.reset_button.draw_button(STEELBLUE)
        self.start_button.draw_button(STEELBLUE)
        self.main_menu_button.draw_button(STEELBLUE)
        self.player_button.draw_button(STEELBLUE)
        self.bfs1_button.draw_button(STEELBLUE)
        self.dfs1_button.draw_button(STEELBLUE)
        self.astar1_button.draw_button(STEELBLUE)
        self.show_winner.draw_button(STEELBLUE)

##### Function for the buttons on grid window. Became too repetitive so, I made it a function.
    # Checks for state when button is clicked and changes button colour when hovered over.
    def grid_window_buttons(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_end_node_button.isOver(pos):
                self.state = 'draw S/E'
            elif self.wall_node_button.isOver(pos):
                self.state = 'draw walls'
            elif self.reset_button.isOver(pos):
                self.execute_reset()
            elif self.start_button.isOver(pos):
                self.state = 'start visualizing'
            elif self.main_menu_button.isOver(pos):
                self.back_to_menu()
            elif self.player_button.isOver(pos):
                self.state= 'draw_player'
            elif self.bfs1_button.isOver(pos):
                self.algorithm_state = 'bfs'
            elif self.dfs1_button.isOver(pos):
                self.algorithm_state = 'dfs'
            elif self.astar1_button.isOver(pos):
                self.algorithm_state='astar'
            elif self.show_winner.isOver(pos):
                self.show_leaderboard()
                
            

        # Get mouse position and check if it is hovering over button
        if event.type == pygame.MOUSEMOTION:
            if self.start_end_node_button.isOver(pos):
                self.start_end_node_button.colour = MINT
            elif self.wall_node_button.isOver(pos):
                self.wall_node_button.colour = MINT
            elif self.reset_button.isOver(pos):
                self.reset_button.colour = MINT
            elif self.start_button.isOver(pos):
                self.start_button.colour = MINT
            elif self.main_menu_button.isOver(pos):
                self.main_menu_button.colour = MINT
            elif self.player_button.isOver(pos):
                self.player_button.colour=MINT
            elif self.bfs1_button.isOver(pos):
                self.bfs1_button.colour=MINT
            elif self.dfs1_button.isOver(pos):
                self.dfs1_button.colour=MINT
            elif self.astar1_button.isOver(pos):
                self.astar1_button.colour=MINT
            elif self.show_winner.isOver(pos):
                self.show_winner.colour=MINT
            else:
                self.start_end_node_button.colour, self.wall_node_button.colour, self.reset_button.colour, \
                self.start_button.colour, self.main_menu_button.colour,self.player_button.colour,self.bfs1_button.colour,self.dfs1_button.colour,self.astar1_button.colour,self.show_winner.colour = \
                STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE,STEELBLUE,STEELBLUE,STEELBLUE,STEELBLUE

    def grid_button_keep_colour(self):
        if self.state == 'draw S/E':
            self.start_end_node_button.colour = MINT

        elif self.state == 'draw walls':
            self.wall_node_button.colour = MINT
        elif self.state == 'draw player':
            self.player_button.colour = MINT
        elif self.algorithm_state=='bfs':
            self.bfs1_button=MINT
        elif self.algorithm_state=='dfs':
            self.dfs1_button.colour=MINT
        elif self.algorithm_state=='astar':
            self.astar1_button.colour=MINT
        elif self.state == 'draw_player':
            if (self.start_node_x,self.start_node_y,self.end_node_x,self.end_node_y) is not None:
                self.player_button.colour = MINT
            else:
                self.state='grid window'

    def execute_reset(self):
        self.start_end_checker = 0

        # Start and End Nodes Coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None
         
        #Draw Path
        self.check_point=True
        self.astar_bool=False
        self.bfs_bool=False
        self.dfs_bool=False
        self.drawbfs_path=None
        self.drawdfs_path=None
        self.drawastar_path=None

        # Wall Nodes List (list already includes the coordinates of the borders)
        self.wall_pos = wall_nodes_coords_list.copy()
        self.wall_List=[]
        self.player_List=[]
        # Switch States
        self.state = 'grid window'

    def back_to_menu(self):
        self.start_end_checker = 0

        # Start and End Nodes Coordinates
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None

        # Wall Nodes List (list already includes the coordinates of the borders)
        self.wall_pos = wall_nodes_coords_list.copy()

        # Switch States
        self.state = 'main menu'


#################################### EXECUTION FUNCTIONS #########################################

##### MAIN MENU FUNCTIONS

    def main_menu_events(self):
        # Draw Background
        pygame.display.update()
        self.sketch_main_menu()
        

        # Check if game is running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()
            # Get mouse position and check if it is clicking button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.bfs_button.isOver(pos):
                    self.algorithm_state = 'bfs'
                    self.state = 'grid window'
                if self.dfs_button.isOver(pos):
                    self.algorithm_state = 'dfs'
                    self.state = 'grid window'
                if self.astar_button.isOver(pos):
                    self.algorithm_state = 'astar'
                    self.state = 'grid window'
                if self.start_game_button.isOver(pos):
                    self.algorithm_state = 'bfs'
                    self.state = 'grid window'

            # Get mouse position and check if it is hovering over button
            if event.type == pygame.MOUSEMOTION:
                if self.bfs_button.isOver(pos):
                    self.bfs_button.colour = AQUAMARINE
                elif self.dfs_button.isOver(pos):
                    self.dfs_button.colour = AQUAMARINE
                elif self.astar_button.isOver(pos):
                    self.astar_button.colour = AQUAMARINE
                elif self.start_game_button.isOver(pos):
                    self.start_game_button.colour = AQUAMARINE
                else:
                    self.bfs_button.colour, self.dfs_button.colour,\
                    self.astar_button.colour,self.start_game_button.colour= WHITE, WHITE, WHITE,WHITE

##### PLAYING STATE FUNCTIONS #####

    def grid_events(self):
        #print(len(wall_nodes_coords_list))
        self.sketch_hotbar()
        self.sketch_grid()
        self.sketch_grid_buttons()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()

            # Grid button function from Helper Functions
            self.grid_window_buttons(pos, event)

##### DRAWING STATE FUNCTIONS #####
    # Check where the mouse is clicking on grid
    # Add in feature to Draw nodes on grid
    # Add in feature so that the drawn nodes on grid translate onto text file
    def draw_nodes(self):
        # Function made in Helper Functions to check which button is pressed and to make it keep colour
        self.grid_button_keep_colour()
        self.sketch_grid_buttons()
        pygame.display.update()
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Grid button function from Helper Functions
            self.grid_window_buttons(pos, event)

            # Set boundaries for where mouse position is valid
            if pos[0] > 264 and pos[0] < 1512 and pos[1] > 24 and pos[1] < 744:
                x_grid_pos = (pos[0] - 264) // 24
                y_grid_pos = (pos[1] - 24) // 24
                #print('GRID-COORD:', x_grid_pos, y_grid_pos)

                # Get mouse position and check if it is clicking button. Then, draw if clicking. CHECK DRAG STATE
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_drag = 1

                    # The chunk of code for start/end pos is placed here, because I do not want the drag feature to be available for start/end nodes
                    if self.state == 'draw S/E' and self.start_end_checker < 2:
                        # Choose point colour for grid and record the coordinate of start pos
                        if self.start_end_checker == 0 and (x_grid_pos+1, y_grid_pos+1) not in self.wall_pos:
                            node_colour = TOMATO
                            self.start_node_x = x_grid_pos + 1
                            self.start_node_y = y_grid_pos + 1
                            # print(self.start_node_x, self.start_node_y)
                            self.start_end_checker += 1

                        # Choose point colour for grid and record the coordinate of end pos
                        # Also, check that the end node is not the same point as start node
                        elif self.start_end_checker == 1 and (x_grid_pos+1, y_grid_pos+1) != (self.start_node_x, self.start_node_y) and (x_grid_pos+1, y_grid_pos+1) not in self.wall_pos:
                            node_colour = ROYALBLUE
                            self.end_node_x = x_grid_pos + 1
                            self.end_node_y = y_grid_pos + 1
                            # print(self.end_node_x, self.end_node_y)
                            self.start_end_checker += 1

                        else:
                            continue

                        # Draw point on Grid
                        pygame.draw.rect(self.screen, node_colour, (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24), 0)

                # Checks if mouse button is no longer held down
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_drag = 0

                # Checks if mouse button is being held down; drag feature
                if self.mouse_drag == 1:
                    # Draw Wall Nodes and append Wall Node Coordinates to the Wall Nodes List
                    # Check if wall node being drawn/added is already in the list and check if it is overlapping start/end nodes
                    if self.state == 'draw walls':
                        if (x_grid_pos + 1, y_grid_pos + 1) not in self.wall_pos \
                                and (x_grid_pos + 1, y_grid_pos + 1) != (self.start_node_x, self.start_node_y) \
                                and (x_grid_pos + 1, y_grid_pos + 1) != (self.end_node_x, self.end_node_y):
                            pygame.draw.rect(self.screen, BLACK, (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24), 0)
                            self.wall_pos.append((x_grid_pos + 1, y_grid_pos + 1))
                            self.wall_List.append((x_grid_pos, y_grid_pos))
                        # print(len(self.wall_pos))

    def draw_again(self,bfsbool,dfsbool,drawbfs_path,drawdfs_path,node_list): 
        self.sketch_grid()
        
       
        
        if self.bfs_bool:
            self.drawbfs_path.draw_path(PURPLE)
        if self.dfs_bool:
            self.drawdfs_path.draw_path(OLIVE)
        if self.astar_bool:
            self.drawastar_path.draw_path(BROWN)
        for (x_pos,y_pos) in self.wall_List:
            pygame.draw.rect(self.screen, BLACK, (264 + x_pos * 24, 24 + y_pos * 24, 24, 24), 0)
        for (x_pos,y_pos) in self.player_List:
            pygame.draw.rect(self.screen, TAN, (240 + x_pos* 24,  y_pos * 24, 24, 24), 0)
        pygame.draw.rect(self.screen, TOMATO, (240 + self.start_node_x * 24, self.start_node_y * 24, 24, 24), 0)
        pygame.draw.rect(self.screen, ROYALBLUE, (240 + self.end_node_x * 24, self.end_node_y * 24, 24, 24), 0)

        pygame.display.update()

#################################### VISUALIZATION FUNCTIONS #########################################
    
    def execute_search_algorithm(self):
        
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.grid_window_buttons(pos, event)
        #print(self.start_node_x, self.start_node_y)
        #print(self.end_node_x, self.end_node_y)

        ### BFS ###

        if self.algorithm_state == 'bfs' and self.bfs_bool==False:
            self.bfs = BreadthFirst(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)
            
            if self.start_node_x or self.end_node_x is not None:
                self.bfs.bfs_execute()

            # Make Object for new path
            if self.bfs.route_found:
                self.drawbfs_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, self.bfs.route, [])
                self.drawbfs_path.get_path_coords()
                self.drawbfs_path.draw_path(PURPLE)
                self.bfs_bool=True
            else:
                self.draw_text('NO ROUTE FOUND!', self.screen, [768,384], 50, RED, FONT, centered = True)

        ### DFS ###

        elif self.algorithm_state == 'dfs' and  self.dfs_bool==False:
            self.dfs = DepthFirst(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.dfs.dfs_execute()

            # Make Object for new path
            if self.dfs.route_found:
                self.drawdfs_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, self.dfs.route, [])
                self.drawdfs_path.get_path_coords()
                self.drawdfs_path.draw_path(OLIVE)
                self.dfs_bool=True
            else:
                self.draw_text('NO ROUTE FOUND!', self.screen, [768,384], 50, RED, FONT, centered = True)

        ### A-STAR ###

        elif self.algorithm_state == 'astar':
            self.astar = AStar(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.astar.astar_execute()

            if self.astar.route_found:
                self.drawastar_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, None, self.astar.route)
                self.drawastar_path.draw_path(BROWN)
                self.astar_bool=True
            else:
                self.draw_text('NO ROUTE FOUND!', self.screen, [768, 384], 50, RED, FONT, centered=True)
        pygame.display.update()
        self.draw_again(self.bfs_bool,self.dfs_bool,self.drawbfs_path,self.drawdfs_path,self.wall_List)
        
        self.state = 'aftermath'

#################################### AFTERMATH FUNCTIONS #########################################

    def reset_or_main_menu(self):
        self.sketch_grid_buttons()
        pygame.display.update()

        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEMOTION:
                if self.start_end_node_button.isOver(pos):
                    self.start_end_node_button.colour = MINT
                elif self.wall_node_button.isOver(pos):
                    self.wall_node_button.colour = MINT
                elif self.reset_button.isOver(pos):
                    self.reset_button.colour = MINT
                elif self.start_button.isOver(pos):
                    self.start_button.colour = MINT
                elif self.main_menu_button.isOver(pos):
                    self.main_menu_button.colour = MINT
                elif self.dfs1_button.isOver(pos):
                    self.dfs1_button.colour=MINT
                elif self.bfs1_button.isOver(pos):
                    self.bfs1_button.colour=MINT
                elif self.show_winner.isOver(pos):
                    self.show_winner.colour=MINT
                else:
                    self.start_end_node_button.colour, self.wall_node_button.colour, self.reset_button.colour, self.start_button.colour,\
                          self.main_menu_button.colour,self.dfs1_button.colour,self.bfs1_button.colour,self.show_winner.colour = STEELBLUE, STEELBLUE,\
                              STEELBLUE, STEELBLUE, STEELBLUE,STEELBLUE,STEELBLUE,STEELBLUE

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.reset_button.isOver(pos):
                    self.execute_reset()
                elif self.main_menu_button.isOver(pos):
                    self.back_to_menu()
                elif self.dfs1_button.isOver(pos):
                    self.state ='start visualizing'
                    self.algorithm_state='dfs'
                    self.execute_search_algorithm()
                elif self.bfs1_button.isOver(pos):
                    self.state ='start visualizing'
                    self.algorithm_state='bfs'
                    self.execute_search_algorithm()
                elif self.astar1_button.isOver(pos):
                    self.state ='start visualizing'
                    self.algorithm_state='astar'
                    self.execute_search_algorithm()
                elif self.show_winner.isOver(pos):
                    self.show_leaderboard()

#################################### PLAYER FUNCTIONS #########################################
    def player_move(self):
        
        self.start_move_x=self.start_node_x 
        self.start_move_y= self.start_node_y
        self.end_move_x= self.end_node_x 
        self.end_move_y= self.end_node_y 
        
        pos=pygame.mouse.get_pos()
        key=pygame.key.get_pressed()
        while self.check_point is True:
            for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    self.running = False
                      
                if events.type==pygame.KEYDOWN and events.key==pygame.K_UP:
                    if (self.start_move_x ,self.start_move_y-1) not in self.wall_pos \
                        and (self.start_move_x ,self.start_move_y-1)!=(self.start_node_x ,self.start_node_y) :
                        
                        self.start_move_y-=1
                        pygame.draw.rect(self.screen, TAN, (self.start_move_x * 24 + 240, self.start_move_y * 24, 24, 24), 0)
                        self.player_List.append((self.start_move_x,self.start_move_y))
                if events.type==pygame.KEYDOWN and events.key==pygame.K_DOWN:
                    if (self.start_move_x ,self.start_move_y+1) not in self.wall_pos \
                        and (self.start_move_x ,self.start_move_y+1)!=(self.start_node_x ,self.start_node_y) :
                        
                        self.start_move_y+=1
                        pygame.draw.rect(self.screen, TAN, (self.start_move_x * 24 + 240, self.start_move_y * 24, 24, 24), 0)
                        self.player_List.append((self.start_move_x,self.start_move_y))
                if events.type==pygame.KEYDOWN and events.key==pygame.K_LEFT:
                    if (self.start_move_x-1 ,self.start_move_y) not in self.wall_pos \
                        and (self.start_move_x-1 ,self.start_move_y)!=(self.start_node_x ,self.start_node_y):
                        self.start_move_x-=1
                        pygame.draw.rect(self.screen, TAN, (self.start_move_x * 24 + 240, self.start_move_y * 24, 24, 24), 0)
                        self.player_List.append((self.start_move_x,self.start_move_y))
                if events.type==pygame.KEYDOWN and events.key==pygame.K_RIGHT:
                    if (self.start_move_x+1 ,self.start_move_y) not in self.wall_pos \
                        and (self.start_move_x+1 ,self.start_move_y)!=(self.start_node_x ,self.start_node_y):
                        self.start_move_x+=1
                        pygame.draw.rect(self.screen, TAN, (self.start_move_x * 24 + 240, self.start_move_y * 24, 24, 24), 0)
                        self.player_List.append((self.start_move_x,self.start_move_y))
                pygame.display.update()
                if(self.start_move_x,self.start_move_y)==(self.end_move_x,self.end_move_y):
                    pygame.draw.rect(self.screen, ROYALBLUE, (264 + self.end_move_x * 24, 24 + self.end_move_y * 24, 24, 24), 0)
                    self.player_List.pop()
                    self.check_point=False
        
        for events in pygame.event.get():
                if events.type == pygame.QUIT:
                    self.running = False
                self.grid_window_buttons(pos,events)  
                
                
 #################################### LEADERBOARD FUNCTIONS #########################################                    
    def show_leaderboard(self):
        self.len_player=None
        self.len_bfs=None
        self.len_dfs=None
        self.len_astar=None
        self.list_winner=[(None,None)]
        self.count=55
        self.sort=1
        self.run=True
        if  self.player_List :
            self.len_player=len(self.player_List)
            self.list_winner.append([self.len_player,'Player'])

        if self.drawbfs_path is not None :
            
            self.len_bfs=self.drawbfs_path.list_len()
            self.list_winner.append([self.len_bfs,'BFS'])

        if self.drawdfs_path is not None:
            
            self.len_dfs=self.drawdfs_path.list_len()
            self.list_winner.append([self.len_dfs,'DFS'])

        if self.drawastar_path is not None:
            
            self.len_astar=self.drawastar_path.list_len()
            self.list_winner.append([self.len_astar,'ASTAR'])

        if self.list_winner :
            sorted(self.list_winner,key=len)

            self.screen.fill(BLACK)
            self.draw_text('Leader Board!', self.screen, [768,55], 50, RED, FONT, centered = True)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            
            for (element,name) in self.list_winner:
                if name is not None:
                    self.count+=70  
                    
                    
                    self.z =  str(name if name is not None else '')+str('  ')+str(element if element is not None else '')
                    
                    self.draw_text(self.z, self.screen, [768,self.count], 50, RED, FONT, centered = True)
                    pygame.display.update()
    
                
                




























