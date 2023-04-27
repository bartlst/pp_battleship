import pygame
import classes


# create dictionary that stores function creating objec for each battleship unit

def createOneFreighter():
    defineOneFreighter = classes.Battleship(1, 0, 0, 1, 1)
    return defineOneFreighter

def createTwoFreighter():
    defineTwoFreighter = classes.Battleship(2, 0, 0, 1, 2)
    return defineTwoFreighter

def createThreeFreighter():
    defineThreeFreighter = classes.Battleship(3, 0, 0, 1, 3)
    return defineThreeFreighter

def createFourFreighter():
    defineFourFreighter = classes.Battleship(4, 0, 0, 1, 4)
    return defineFourFreighter


battleshipTypes = {
    "oneFreighter": createOneFreighter(),
    "twoFreighter": createTwoFreighter(),
    "threeFreighter": createThreeFreighter(),
    "fourFreighter": createFourFreighter(),
}

q = createOneFreighter()
w = createOneFreighter()
print("Q HP: ", q.getHP(), "W HP: ", w.getHP())
q.takeDamage(1)
print("Q HP: ", q.getHP(), "W HP: ", w.getHP())



