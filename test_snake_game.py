from snake_game import eating_food, screen_area_of_rectangle

import pytest
import pygame
import os
import sys
import random
import time


def test_eating_food():
    assert eating_food(3) == 4

 
def test_area():
    output = screen_area_of_rectangle(2,5)
    assert output == 10

pytest.main(["-v", "--tb=line", "-rN", __file__])