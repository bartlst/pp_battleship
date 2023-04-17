class Position:
    x = None
    y = None


class Map:
    def __init__(self, width, height):
        self.map = []
        for x in range(width):
            for y in range(height):
                Position.x = x
                Position.y = y
                occupied = False
                temp_position = [Position, occupied]
                self.map.append(temp_position)

    def putBattleship(self,position, battleship):
        """"Method that is responsible for putting new battleship on map. Method is checking if position is not occupied,
        and then it change position of given battleship"""
        #for loop that will check each position on map that battleship want take
        battleshipPosition = battleship.getPosition()
        positionToCheck = Position
        for y in range(battleshipPosition["height"]):
            for x in range(battleshipPosition["width"]):
                positionToCheck.x = position.x+x
                positionToCheck.y = position.y+y
                #if position is occupied -> return false if not keep checking
                #after verification set all positions to occupied and set position of battleship




    def relocateBattleship(self,position, battleship):
        #maybe this method could be deleted after modifying putBattleship method
        return False
        """"Method that is responsible for relocating battleship from current position to another.
        Method is checking if position is not occupied,
        and then it change position of given battleship, and releases previous position"""



class Battleship:

    def __init__(self, healthPoints, imgRegular, imgDestroyed, width, height):

        self.__position = Position()
        self.__position.x = 0
        self.__position.y = 0
        self.__working = True
        self.__direction = "horizontal"

        self.__healthPoints = healthPoints
        self.__imgRegular = imgRegular
        self.__imgDestroyed = imgDestroyed

        self.__width = width
        self.__height = height

        self.__imgDisplayed = self.imgRegular
        print(self.__healthPoints)

        #additional for future development
        #self.actionList #list of actions that could be used by this battleship
        #self.type #type of battleship e.g. ocean/land
        #self.damage #each battleship will be able to  shoot

    def relocate(self, position, direction):
        """Method that is used to move battleship, it is taking new position and set battleship on it. Position is
        stored in x,y values which are the coordinates of the front of the ship
        (upper left corner in horizontal position) """
        self.__position = position
        self.__direction = direction

    def takeDamage(self, damage):
        """"Method that is used to deduct damage form health points,
        if health points <= 0 method is setting destroyed image as primary and deactivates battleship"""
        self.healthPoints -= damage
        if self.healthPoints <= 0:
            self.__imgDisplayed = self.__imgDestroyed
            self.__working = False

    def getImage(self):
        """"Method returns imaged of the battleship"""
        return self.__imgDisplayed

    def getStatus(self):
        """"Method returns True if battleship is working or False if is not"""
        return self.__working

    def getPosition(self):
        """"Method returns information in dictionary about position of battleship
        (position, width, height, direction)"""
        position= {
            "position": self.__position,
            "width": self.__width,
            "height": self.__height,
            "direction": self.__direction
        }
        return position

    def getHP(self):
        """"Method returns health points of battleship"""
        return self.__healthPoints

    def getSize(self):  #maybe this method could be deleted because of getPosition method
        """"Method returns size of battleship"""
        size ={
            "width": self.__width,
            "height": self.__height,
        }
        return size


battleshipOne = Battleship(54, 0, 0, 0, 0)
mapOne = Map(10, 10)

