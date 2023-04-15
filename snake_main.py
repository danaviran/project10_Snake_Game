##############################################################################
# FILE: snake_main.py
# WRITERS:
# Dana Aviran, 211326608, dana.av
# Eldad Eliyahu, 318565058, eldad333
# EXERCISE: Intro2cs2 ex10 2021-2022
##############################################################################

import game_parameters
from game_display import GameDisplay
from snake import Snake
from apple import Apple
from bomb import Bomb
from nod import Node

# Colors
APPLE_COLOR = "green"
BOMB_COLOR = "red"
EXPLOSION_COLOR = "orange"
SNAKE_COLOR = "black"

# Directions
INIT_DIRECTION = "Up"
SNAKE_LEGAL_DIRECTIONS = "udlr"
CLICKED_VALID_DIRECTIONS = ["Up", "Down", "Left", "Right"]
OPPOSITE_DIRECTIONS = {"Up": "Down", "Down": "Up", "Left": "Right",
                       "Right": "Left"}
DIRECTION_KEYS = {"Up": "u", "Down": "d", "Left": "l", "Right": "r"}

# Num values
NUM_APPLES = 3
SNAKE_INIT_LENGTH = 3


class Game:
    """
     Class methods make interactions between objects in it's different lists.
    """
    def __init__(self, snake, gd):
        # Apples:
        self.lst_of_apples = []

        # Bombs:
        self.lst_of_bombs = []
        self.lst_of_exploded_bombs = []
        self.lst_of_exploded_cells = []

        # Snake:
        self.snake = snake

        # Display:
        self.game_display = gd

    def add_apple_to_lst(self, apple):
        self.lst_of_apples.append(apple)

    def add_bomb_to_lst(self, bomb: Bomb):
        self.lst_of_bombs.append(bomb)

    def add_bomb_to_exploded_lst(self, bomb):
        self.lst_of_exploded_bombs.append(bomb)

    def remove_bomb_from_bomb_lst(self, bomb):
        self.lst_of_bombs.remove(bomb)

    def init_lst_of_exploded_cells(self):
        self.lst_of_exploded_cells = []

    def exploded_just_now_lst(self):
        """
        this function checks if one of the bombs in the bomb list exploded.
        if it did, it removes it from the bomb list and adds it to the exploded
        bomb list.
        :return: the exploded_just_now_lst
        """
        exploded_just_now_lst = []
        for i in range(len(self.lst_of_bombs)):
            if not self.lst_of_bombs[i].get_time():
                exploded_just_now_lst.append(self.lst_of_bombs[i])
        return exploded_just_now_lst

    def draw_snake(self):
        """
        we draw the cells of the snake
        :return: None
        """
        for coord in self.snake.get_snake_coordinates():
            col, row = coord
            self.game_display.draw_cell(col, row, SNAKE_COLOR)

    def draw_bombs(self):
        """
        we draw the cells of bombs
        :return: None
        """
        for bomb in self.lst_of_bombs:
            col, row = bomb.get_coordinates()
            self.game_display.draw_cell(col, row, BOMB_COLOR)

    def draw_apples(self):
        """
        we draw the cells of apples
        :return: None
        """
        for apple in self.lst_of_apples:
            col, row = apple.get_coordinates()
            self.game_display.draw_cell(col, row, APPLE_COLOR)

    def draw_explosion(self):
        """
        we draw the cells of explosion
        :return: None
        """
        for cell in self.lst_of_exploded_cells:
            col, row = cell
            self.game_display.draw_cell(col, row, EXPLOSION_COLOR)

    def is_snake_on_explosion(self):
        """
        checks if the snake is on the explosion cells
        :return: False if it is not, True if it is
        """
        for coordinate in self.snake.get_snake_coordinates():
            if coordinate in self.lst_of_exploded_cells:
                return True
        return False

    def is_snake_on_apple(self):
        """
        checks if the snake ate an apple (is on an apple)
        :return: returns the apple the snake ate if he did, else return None
        """
        head_of_snake_coords = self.snake.get_head_of_snake().get_data()
        for apple in self.lst_of_apples:
            if head_of_snake_coords == apple.get_coordinates():
                return apple

    def is_snake_on_bomb(self):
        """
        checks if the snake stepped a bomb
        :return: the bomb he stepped on if he did, None otherwise
        """
        for bomb in self.lst_of_bombs:
            if bomb.get_coordinates() in self.snake.get_snake_coordinates():
                return bomb

    def swap_helper(self, coordinates):
        """
        we checks the coords of the cell of the randomized object
        :param coordinates: the coordinates
        :return: False if there is an intersection, True otherwise
        """
        for other_coordinates in \
                [bomb.get_coordinates() for bomb in self.lst_of_bombs] + \
                [apple.get_coordinates() for apple in self.lst_of_apples] + \
                self.lst_of_exploded_cells + \
                self.snake.get_snake_coordinates():
            if other_coordinates == coordinates:
                return False
        return True

    def swap_apples(self, apple):
        """
        we swap the current apple with a new randomized one and add it to the
        apple list
        :param apple:
        :return: the new apple
        """
        col, row, score = game_parameters.get_random_apple_data()
        # we re-do the randomization till it is a valid cell
        while not self.swap_helper((col, row)):
            col, row, score = game_parameters.get_random_apple_data()
        # we set the new values of the apple
        apple.set_coordinates((col, row))
        apple.set_score(score)
        # we append it to the list
        self.lst_of_apples.append(apple)
        return apple

    def swap_bomb(self, bomb):
        """
        we swap the current bomb that exploded with a new randomized one and
        add it to the bomb list
        :param bomb: the current bomb
        :return: the new bomb
        """
        # we remove the current bomb from the exploded bomb list
        if bomb in self.lst_of_exploded_bombs:
            self.lst_of_exploded_bombs.remove(bomb)
        # we randomize
        col, row, radius, time = game_parameters.get_random_bomb_data()
        # we re-do the randomization till it is a valid cell
        while not self.swap_helper((col, row)):
            col, row, radius, time = game_parameters.get_random_bomb_data()
        # we create a new bomb with the values
        bomb = Bomb((col, row), radius, time)
        # we append the new bomb to the list of bombs
        self.lst_of_bombs.append(bomb)
        return bomb

    def find_cell_of_explosion(self, coordinates, radius):
        """
        we find the cells of explosion, according to the current iteration.
        the wave of explosion stops when the iteration equals the radius.
        we add those cells to the list of exploded cells
        :param coordinates: the coordinates of the bomb that exploded
        :param radius: the radius if the bomb
        :return: None
        """
        # first, we initialize the list because it changes with each iteration
        self.lst_of_exploded_cells = []
        col, row = coordinates
        # we calculate the square of cells for this iteration of explosion -
        # indicated by the radius
        lst_cell_to_check = []
        for j in range(col - radius, col + radius + 1):
            for i in range(row - radius, row + radius + 1):
                lst_cell_to_check.append((j, i))
        # we check which cells from the square are in the explosion by formula,
        # and that we did not go out of the board:
        for j, i in lst_cell_to_check:
            if abs(col - j) + abs(row - i) == radius and j >= 0 and i >= 0 and\
                    j < game_parameters.WIDTH and i < game_parameters.HEIGHT:
                self.lst_of_exploded_cells.append((j, i))

    def look_after_apple_in_explosion(self):
        """
        we look after apples that were exploded and create new randomized ones
        :return:
        """
        for apple in self.lst_of_apples:
            if apple.get_coordinates() in self.lst_of_exploded_cells:
                self.lst_of_apples.remove(apple)
                self.swap_apples(apple)


# Object initialization functions:

def init_snake():
    """
    we create the snake object of class Snake by instructions.
    the Snake object is a two-sided linked list that uses 'nod' class of Nodes.
    :return: snake
    """
    init_height = game_parameters.HEIGHT // 2
    init_width = game_parameters.WIDTH // 2
    # the head of the snake
    head_of_snake = Node((init_width, init_height))
    # the middle cell
    middle_node = Node((init_width, init_height - 1))
    # the last cell - the tail of the snake
    tail_of_snake = Node((init_width, init_height - 2))
    # we link the nodes together
    tail_of_snake.set_next(middle_node)
    middle_node.set_prev(tail_of_snake)
    middle_node.set_next(head_of_snake)
    head_of_snake.set_prev(middle_node)
    # we create the snake object
    snake = Snake(SNAKE_INIT_LENGTH, head_of_snake, tail_of_snake,
                  SNAKE_LEGAL_DIRECTIONS, 1)
    return snake


def init_bomb(game_helper: Game, snake):
    """
    we create a bomb object of class Bomb
    :param game_helper: we use the object game_helper of class Game
    :param snake: we check that we don't put a bomb on the snake
    :return:
    """
    while True:
        # we randomize the bomb values
        col, row, radius, time = game_parameters.get_random_bomb_data()
        # we create a new bomb
        bomb = Bomb((col, row), radius, time)
        # if the bomb is on the snake, we try again
        if (col, row) in snake.get_snake_coordinates():
            continue
        # else, the bomb is randomized correctly, we append it to the list of
        # bombs and return it
        else:
            game_helper.lst_of_bombs.append(bomb)
            return bomb


def init_apples(game_helper: Game):
    """
    we create the first three apples of the game, using the class Apple and
    the randomization functions in game_parameters.py
    :param game_helper: we use the object game_helper of class Game
    :return: None
    """
    while len(game_helper.lst_of_apples) < 3:
        # we initialize values to be randomized
        col, row, score = 1, 1, 1
        # we create the current apple
        random_apple = Apple((col, row), score)
        # we swap the current initialized apple with a randomized one, using
        # the apple swap function
        game_helper.swap_apples(random_apple)


def check_lose_conditions(game_helper, snake, prev_coords, bomb):
    """
    Checks if the snake is in the borders, if it did not step on itself, if
    it did not step on a bomb, if it did not step on an explosion, and if there
    is still space for it to move in the board. otherwise, we end the game.
    :param game_helper: we use the object game_helper of class Game
    :param snake: our snake of class Snake
    :param prev_coords: the prev_coords of the snake to check if the new head
    is not on them
    :param bomb: the current bomb, to check that the snake is not on it
    :return: False if one of the conditions is true - the snake loses
    True if we did not lose - the conditions are all False
    """
    col, row = snake.get_head_of_snake().get_data()
    if col < 0 or row < 0 or col >= game_parameters.WIDTH or \
            row >= game_parameters.HEIGHT or \
            (col, row) in prev_coords or \
            (col, row) == bomb.get_coordinates() or \
            game_helper.is_snake_on_explosion() or (
            game_parameters.WIDTH * game_parameters.HEIGHT - len(
        snake.get_snake_coordinates()) <= 5):
        return False
    return True


def check_lose_explosion_conditions(game_helper, snake, bomb):
    """
    checks if the snake got into the explosion
    :param game_helper:
    :param snake:
    :param bomb:
    :return: False if the snake's body got in the explosion or the snake is on
    the bomb, the snake's head if his head got exploded (not the body), and
    True if everything is ok
    """
    col, row = snake.get_head_of_snake().get_data()
    if (col, row) == bomb.get_coordinates():
        return False
    # if the snake exploded
    if game_helper.is_snake_on_explosion():
        # if his head exploded, we return it (because later we nedd to remove it)
        if snake.get_head_of_snake().get_data() in game_helper.lst_of_exploded_cells:
            return snake.get_head_of_snake()
        # else, just his body got exploded
        else:
            return False
    return True


def draw_screen(gd, game_helper, score_of_game):
    """
    :param gd: the game display given
    :param game_helper: an object of class Game
    :param score_of_game: we show the score of the game
    :return: None, uses that functions in game_helper (an object of class Game)
    to draw the cells in each iteration of the main loop
    """
    gd.show_score(score_of_game)
    game_helper.draw_snake()
    game_helper.draw_bombs()
    game_helper.draw_apples()
    game_helper.draw_explosion()


def update_snake(is_growing_snake, new_direction, num_of_growing_rounds,
                 snake):
    """
    :param is_growing_snake: a boolean that indicates if the snake is growing
    (if he ate an apple and the number if growing rounds did not pass yet)
    :param new_direction: the new direction if the snake's move, indicated by
    the click of the player
    :param num_of_growing_rounds: a num that indicates how many round the snake is
    still supposed to grow (after eating an apple)
    :param snake: a Snake object we created for the game
    :return: the new num_of_growing_rounds, prev_coord the current coordinates
    of the snake to check in the main loop if he stepped on himself by moving,
    and the same new direction (that will act in the loop from now on as the
    current direction
    """
    if num_of_growing_rounds:
        num_of_growing_rounds -= 1
    if is_growing_snake:
        prev_coords = snake.get_snake_coordinates()
    else:
        # the snake is able to move to the cell that his tail was in the last
        # iteration
        prev_coords = snake.get_snake_coordinates()[1:]
    # we move the snake by using the method in class Snake
    snake.move_snake(DIRECTION_KEYS[new_direction], is_growing_snake)
    return num_of_growing_rounds, prev_coords, new_direction


def update_bombs(bomb, counter_of_explosion_rounds, did_explode,
                 explosion_center, game_helper):
    """
    this function updates the bombs in the main loop in each iteration.
    :param bomb: the current bomb we are checking
    :param counter_of_explosion_rounds: if the bomb exploded, we count the num
    of iterations since the explosion, in order to draw the explosion cells
    :param did_explode: a boolean
    :param explosion_center: the coordinates of the bomb
    :param game_helper: an object of class Game. we use it's functions.
    :return: new counter_of_explosion_rounds, the did_explode boolean (maybe
     it changed) and the explosion center
    """
    # if there is a ticking bomb on the board (did not explode yet), we down
    # the time of the bomb by one (there is only one bomb on the board,
    # therefore we check the first one in the list
    if game_helper.lst_of_bombs:
        game_helper.lst_of_bombs[0].down_time()

    # if the bomb already exploded:
    if did_explode:
        explosion_center = game_helper.lst_of_exploded_bombs[
            0].get_coordinates()

        # if there supposed to be more iterations of explosion wave
        if counter_of_explosion_rounds <= \
                game_helper.lst_of_exploded_bombs[0].get_radius():
            # we find the cells of explosion and put them in the exploded cells
            # list of our game_helper Game object
            game_helper.find_cell_of_explosion(explosion_center,
                                               counter_of_explosion_rounds)
            counter_of_explosion_rounds += 1
        # else, if the counter_of_explosion_rounds is bigger than the bombs
        # radius,the explosion wave is finished - we initialize the list of the
        # exploded cells, we swap the current bomb with a new randomized one
        # and we False the did_explode boolean
        else:
            game_helper.init_lst_of_exploded_cells()
            did_explode = False
            game_helper.swap_bomb(bomb)

    # if the bomb did not explode yet
    else:
        # if the timer of the bomb got down to zero
        if game_helper.lst_of_bombs and game_helper.lst_of_bombs[0].get_time() \
                == 0:
            # we remove the bomb from the bomb list
            game_helper.remove_bomb_from_bomb_lst(bomb)
            # we add the bomb to the exploded list
            game_helper.add_bomb_to_exploded_lst(bomb)
            # we get the coordinates of the exploded bomb
            explosion_center = game_helper.lst_of_exploded_bombs[0] \
                .get_coordinates()
            # we find the cells of explosion and put them in the exploded cells
            # list
            game_helper.find_cell_of_explosion(explosion_center, 0)
            # we initialize the counter to 1
            counter_of_explosion_rounds = 1
            # we True the boolean
            did_explode = True
    # we return the current counter of explosion rounds, the explosion_center
    # and the boolean
    return counter_of_explosion_rounds, explosion_center, did_explode


def update_apple(game_helper, gd, counter_of_growing_rounds, score_of_game):
    """
    this function updates the apples in the main loop in each iteration.
    :param game_helper: the Game object we use
    :param gd: the game_display object of Game_display class
    :param counter_of_growing_rounds: if the snake ate an apple, we update the
    number of growing rounds of the snake (we add 3 each time he eats an apple)
    :param score_of_game: we update the score of the game according to the
    score of the eaten apple
    :return: the current boolean is_growing_snake, the current
    counter_of_growing_rounds, and the current score_of_game
    """
    # we update the apples that were exploded (if there were any)
    game_helper.look_after_apple_in_explosion()

    # we check if the snake ate an apple
    is_on_apple = game_helper.is_snake_on_apple()  # apple or none
    if is_on_apple is not None:
        # we remove the apple from the list
        game_helper.lst_of_apples.remove(is_on_apple)
        # we add 3 to the counter of growing rounds
        counter_of_growing_rounds += 3
        # we update the score of the game
        score_of_game += is_on_apple.get_score()
        gd.show_score(score_of_game)
        # we swap the apple with a new randomized one
        game_helper.swap_apples(is_on_apple)
        # we True the boolean
        is_growing_snake = True

    else:  # else, the snake did not step on an apple
        # if the counter initialized to zero, we update the boolean
        if counter_of_growing_rounds == 0:
            is_growing_snake = False
        # else, the snake is still growing
        else:
            is_growing_snake = True
    return is_growing_snake, counter_of_growing_rounds, score_of_game


def main_loop(gd: GameDisplay) -> None:
    # initialization
    # objects of the game
    snake = init_snake()
    game_helper = Game(snake, gd)
    bomb = init_bomb(game_helper, snake)
    init_apples(game_helper)

    # counters of the main loop
    score_of_game = 0
    counter_of_growing_rounds = 0
    counter_of_explosion_rounds = 0

    # booleans
    is_growing_snake = False
    did_explode = False

    # more
    current_direction = INIT_DIRECTION
    explosion_center = None

    # we draw the screen
    draw_screen(gd, game_helper, score_of_game)
    gd.end_round()

    # the actual loop of the game
    while True:
        # 1. Get the keys from the user:
        new_direction = gd.get_key_clicked()
        if new_direction == OPPOSITE_DIRECTIONS[current_direction] or\
                new_direction not in CLICKED_VALID_DIRECTIONS:
            new_direction = current_direction

        # 2. Update of objects and their state for the next round:
        # a. Update snake:
        counter_of_growing_rounds, prev_coords, current_direction = \
            update_snake(is_growing_snake, new_direction,
                         counter_of_growing_rounds, snake)
        # b. Update apple (with snake):
        is_growing_snake, counter_of_growing_rounds, score_of_game = update_apple(
            game_helper, gd, counter_of_growing_rounds, score_of_game)

        # 3. Check if the game continues - the snake didn't step on itself,
        # did not get out of the borders of board and did not get into a bomb
        if not check_lose_conditions(game_helper, snake, prev_coords, bomb):
            game_helper.snake.remove_head_of_snake()
            draw_screen(gd, game_helper, score_of_game)
            gd.end_round()
            break
        # 4. Update bombs:
        if game_helper.lst_of_bombs:
            bomb = game_helper.lst_of_bombs[0]  # there is just one in our game
        counter_of_explosion_rounds, explosion_center, did_explode = \
            update_bombs(bomb, counter_of_explosion_rounds, did_explode,
                         explosion_center, game_helper)
        game_helper.look_after_apple_in_explosion()

        # 5. Check if the game continues - if the snake did not exploded
        check_if_exploded = check_lose_explosion_conditions(game_helper, snake,
                                                            bomb)
        # False, the head of the snake or True
        # if the value is False, the snake's body got exploded and we end game
        if not check_if_exploded:
            draw_screen(gd, game_helper, score_of_game)
            gd.end_round()
            break
        # else, if we got the head of the snake, we remove it and end game
        elif check_if_exploded == snake.get_head_of_snake():
            snake.remove_head_of_snake()
            draw_screen(gd, game_helper, score_of_game)
            gd.end_round()

        # 6. Draw board:
        draw_screen(gd, game_helper, score_of_game)
        gd.end_round()
