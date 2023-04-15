##############################################################################
# FILE: bomb.py
# WRITERS:
# Dana Aviran, 211326608, dana.av
# Eldad Eliyahu, 318565058, eldad333
# EXERCISE: Intro2cs2 ex10 2021-2022
##############################################################################

class Bomb:
    """
    Bomb class - creates Bomb objects
    """
    def __init__(self, coordinates, radius, time):
        self.__coordinates = coordinates
        self.__time = time
        self.__radius = radius

    def get_coordinates(self):
        return self.__coordinates

    def get_time(self):
        return self.__time

    def get_radius(self):
        return self.__radius

    def set_coordinates(self, coordinates):
        self.__coordinates = coordinates

    def set_time(self, time):
        self.__time = time

    def set_radius(self, radius):
        self.__radius = radius

    def down_time(self):
        # down the timer of the bomb by one
        self.__time -= 1
