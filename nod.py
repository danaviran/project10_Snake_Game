##############################################################################
# FILE: nod.py
# WRITERS:
# Dana Aviran, 211326608, dana.av
# Eldad Eliyahu, 318565058, eldad333
# EXERCISE: Intro2cs2 ex10 2021-2022
##############################################################################

class Node:
    """
    Node class - creates Node objects
    """
    def __init__(self, data=None, prev=None, next=None):
        self.__data = data
        self.__prev = prev
        self.__next = next

    def __str__(self):
        return str(self.__data)

    def get_data(self):
        return self.__data

    def get_next(self):
        return self.__next

    def get_prev(self):
        return self.__prev

    def set_data(self, data):
        self.__data = data

    def set_next(self, next):
        self.__next = next

    def set_prev(self, prev):
        self.__prev = prev