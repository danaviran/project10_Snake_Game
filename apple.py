##############################################################################
# FILE: apple.py
# WRITERS:
# Dana Aviran, 211326608, dana.av
# Eldad Eliyahu, 318565058, eldad333
# EXERCISE: Intro2cs2 ex10 2021-2022
##############################################################################

class Apple:
    """
    Apple class - creates Apple objects
    """
    def __init__(self, coordinates, score):
        self.coordinates = coordinates
        self.score = score

    def get_coordinates(self):
        return self.coordinates

    def get_score(self):
        return self.score

    def set_coordinates(self, coordinates):
        self.coordinates = coordinates

    def set_score(self, score):
        self.score = score
