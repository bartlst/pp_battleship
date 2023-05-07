class communication:
    def __init__(self, packet_type, data):
        self.packet_type = packet_type
        self.data = data

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Map:
    def __init__(self, width, height):
        self.map = []
        for y in range(height):
            row = []
            for x in range(width):
                position = Position(x,y)
                occupied = False
                battleship = None
                temp_position = {
                    "position": position,
                    "occupied": occupied,
                    "battleship": battleship
                }
                row.append(temp_position)
            self.map.append(row)

    def putBattleship(self, position, direction, battleship):
        """Method that is responsible for putting battleship on map. Method is checking if
        position is not occupied, and then it change position of given battleship and in case of success returns true
        and in case of failure returns False"""
        battleshipPosition = battleship.getPosition()
        if direction != battleshipPosition["direction"]:
            height = battleshipPosition["width"]
            width = battleshipPosition["height"]
        else:
            width = battleshipPosition["width"]
            height = battleshipPosition["height"]

        for y in range(height):
            if position.y+y not in range(0, len(self.map)): return False
            row = self.map[position.y+y]
            for x in range(width):
                if position.x + x not in range(0, len(row)): return False
                if row[position.x+x]["occupied"]:
                    return False

        for y in range(height):
            row = self.map[position.y+y]
            for x in range(width):
                row[position.x+x]["occupied"] = True
                row[position.x+x]["battleship"] = battleship
        battleship.relocate(position, direction)
        return True

    def attacOnPosition(self, pos, damage):
        if self.map[pos.y][pos.x]["occupied"]:
            self.map[pos.y][pos.x]["battleship"].takeDamage(damage)
        return False


class Battleship:

    def __init__(self, healthPoints, imgRegular, imgDestroyed, width, height):

        self.__position = Position(0, 0)
        self.__position.x = 0
        self.__position.y = 0
        self.__working = True
        self.__direction = "horizontal"

        self.__healthPoints = healthPoints
        self.__imgRegular = imgRegular
        self.__imgDestroyed = imgDestroyed

        self.__width = width
        self.__height = height

        self.__imgDisplayed = self.__imgRegular

        #additional for future development \/

        #self.actionList #list of actions that could be used by this battleship
        #self.type #type of battleship e.g. ocean/land
        #self.damage #each battleship will be able to  shoot

    def relocate(self, position, direction):
        """Method that is used to move battleship, it is taking new position and set battleship on it. Position is
        stored in x,y values which are the coordinates of the front of the ship
        (upper left corner in horizontal position)"""
        self.__position = position
        self.__direction = direction

        #TODO
        # 1. if direction != __direction then image rotate

    def takeDamage(self, damage):
        """"Method that is used to deduct damage form health points,
        if health points <= 0 method is setting destroyed image as primary and deactivates battleship"""
        self.__healthPoints -= damage
        if self.__healthPoints <= 0:
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


battleshipOne = Battleship(54, 0, 0, 3, 1)
mapOne = Map(10, 10)
position = Position(2, 2)
mapOne.putBattleship(position, "horizontal", battleshipOne)

print(battleshipOne.getHP())
mapOne.attacOnPosition(position, 1)

print(battleshipOne.getHP())