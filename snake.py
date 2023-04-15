##############################################################################
# FILE: snake.py
# WRITERS:
# Dana Aviran, 211326608, dana.av
# Eldad Eliyahu, 318565058, eldad333
# EXERCISE: Intro2cs2 ex10 2021-2022
##############################################################################

from nod import Node


class Snake:
    """
    a class that creates Snakes. the snake object is a two-sided linked list,
    that uses class Node for each chain of the list
    """
    def __init__(self, length, head_of_snake, tale_of_snake, directions,
                 num_of_steps):
        """
        :param length: length of snake
        :param head_of_snake: a Node object - the head of the snake
        :param tale_of_snake: a Node object - the tail of the snake
        :param directions: a string of valid directions
        :param num_of_steps: a num of valid steps that the snake can make
        """
        self.__length = length
        self.__directions = directions
        self.__num_of_steps = num_of_steps
        self.__head_of_snake = head_of_snake
        self.__tail_of_snake = tale_of_snake

    def get_num_steps(self):
        return self.__num_of_steps

    def get_directions(self):
        return self.__directions

    def get_head_of_snake(self):
        return self.__head_of_snake

    def set_head_of_snake(self, new_head_of_snake):
        self.__head_of_snake = new_head_of_snake

    def get_tale_of_snake(self):
        return self.__tail_of_snake

    def remove_head_of_snake(self):
        """
        we remove the head of the snake
        :return: None
        """
        head_of_snake = self.get_head_of_snake()
        prev = head_of_snake.get_prev()
        prev.set_next(None)
        head_of_snake.set_prev(None)
        self.set_head_of_snake(prev)

    def remove_tail_of_snake(self):
        # we remove the tail of the snake
        prev_tale = self.__tail_of_snake
        new_tale = prev_tale.get_next()
        self.__tail_of_snake = new_tale
        prev_tale.set_next(None)
        prev_tale.set_prev(None)

    def __str__(self):
        """
        we print the snake by printing it's coordinates
        :return: a string of the coordinates
        """
        list_of_coordinates = []
        if not self.__tail_of_snake:
            return None
        if not self.__tail_of_snake.get_next():
            list_of_coordinates = [self.__tail_of_snake.get_data()]
            return str(list_of_coordinates)
        if not self.__tail_of_snake.get_next().get_next():
            list_of_coordinates = [self.__tail_of_snake.get_data(),
                                   self.__tail_of_snake.get_next().get_data()]
            return str(list_of_coordinates)
        current = self.__tail_of_snake
        while current is not None:
            list_of_coordinates.append(current.get_data())
            current = current.get_next()
        return str(list_of_coordinates)

    def get_snake_coordinates(self):
        """
        :return: a list of all snake's coordinates, from tail to head
        """
        list_of_coordinates = []
        if not self.__tail_of_snake:
            return []
        if not self.__tail_of_snake.get_next():
            list_of_coordinates = [self.__tail_of_snake.get_data()]
            return list_of_coordinates
        # if the snake is longer than one cell:
        current = self.__tail_of_snake
        while current is not None:
            list_of_coordinates.append(current.get_data())
            current = current.get_next()
        return list_of_coordinates

    def move_snake(self, direction, is_growing_snake):
        """
        moving the snake to a certain direction.
        :param direction: the direction of that the snake need to move towards
        :param is_growing_snake: a bool that checks if the snake is growing
        :return: a list of the snake's new coordinates if the move succeeded,
        None otherwise
        """
        if direction in self.__directions:
            col, row = self.__head_of_snake.get_data()
            if direction == 'u':
                new_cell_coordinates = (col, row + self.__num_of_steps)
            elif direction == 'd':
                new_cell_coordinates = (col, row - self.__num_of_steps)
            elif direction == 'l':
                new_cell_coordinates = (col - self.__num_of_steps, row)
            elif direction == 'r':
                new_cell_coordinates = (col + self.__num_of_steps, row)
            # if the direction is not valid
            else:
                return None
            # Now, we make a node of class Node of the new head of the snake
            new_node = Node(new_cell_coordinates)
            # and we add it as the new head
            self.__head_of_snake.set_next(new_node)
            new_node.set_prev(self.__head_of_snake)
            self.__head_of_snake = self.__head_of_snake.get_next()
            # if the snake is not growing, we remove it's current tail, because
            # it moved to be the next cell
            if not is_growing_snake:
                self.remove_tail_of_snake()
            return new_cell_coordinates




