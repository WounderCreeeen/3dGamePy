import pickle


class MapManager():
    def __init__(self):
        self.model = 'block'
        self.texture = 'block.png'
        self.colors = [(.2, .2, .35, 1),
                      (.2, .2, .3, 1),
                      (.5, .5, .2, 1),
                      (.0, .6, .0, 1)]
        self.startNew()
        self.addBlock((0, 10, 0))

    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.color)-1]

    def clear(self):
        self.land.removeNode()
        self.startNew()

    def startNew(self):
        self.land = render.attachNewNode('Land.txt')

    def addBlock(self, position):
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(position)
        self.color = self.getColor(int(position[2]))
        self.block.setColor(self.color)
        self.block.setTag('at', str(position))
        self.block.reparentTo(self.land)

    def loadLand(self, filename):
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z0 in range(int(z)+1):
                        block = self.addBlock((x, y, z0))
                    x+=1
                y+=1
            return x, y

    def findBlocks(self, pos):
        return self.land.findAllMatches("=at=" + str(pos))

    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        return True

    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return x, y, z

    def delBlock(self, position):
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()

    def buildBlock(self, pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)

    def delBlockFrom(self, position):
        x, y, z = self.findHighestEmpty(position)
        pos = x, y, z-1
        for block in self.findBlocks(pos):
            block.removeNode()

    def saveMap(self):
        blocks = self.land.getChildren()
        with open('my_map.dat', 'wb') as file:
            pickle.dump(len(blocks), file)
            for block in blocks:
                x, y, z, = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, file)

    def loadMap(self):
        self.clear()
        with open('my_map.dat', 'rb') as file:
            length = pickle.load(file)
            for i in range(length):
                pos = pickle.load(file)
                self.addBlock(pos)