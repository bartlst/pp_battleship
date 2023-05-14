import pygame
import classes


# create dictionary that stores function creating objec for each battleship unit

def createOneFreighter():
    defineOneFreighter = classes.Battleship(1, 0, 0, 1, 1, 'oneFreighter')
    return defineOneFreighter

def createTwoFreighter():
    defineTwoFreighter = classes.Battleship(2, 0, 0, 1, 2, 'twoFreighter')
    return defineTwoFreighter

def createThreeFreighter():
    defineThreeFreighter = classes.Battleship(3, 0, 0, 1, 3, 'threeFreighter')
    return defineThreeFreighter

def createFourFreighter():
    defineFourFreighter = classes.Battleship(4, 0, 0, 1, 4, 'fourFreighter')
    return defineFourFreighter


battleshipTypes = {
    "oneFreighter": createOneFreighter(),
    "twoFreighter": createTwoFreighter(),
    "threeFreighter": createThreeFreighter(),
    "fourFreighter": createFourFreighter(),
}

battleships_pul = [
    battleshipTypes["oneFreighter"],
    battleshipTypes["twoFreighter"],
    battleshipTypes["threeFreighter"],
    battleshipTypes["fourFreighter"]
]



