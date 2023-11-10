keySwCam = 't'
keySwMode = 'y'

keyFw = 'w'
keyBk = 's'
keyLt = 'a'
keyRt = 'd'

keyUp = 'space'
keyDn = 'shift'

keyTnLt = 'q'
keyTnRt = 'e'

keyBld = 'z'
keyDst = 'x'

keySv = 'k'
keyLd = 'l'

def check_dir(angle):
    if 0 <= angle <= 20:
        return 0, -1
    elif angle <= 65:
        return 1, -1
    elif angle <= 110:
        return 1, 0
    elif angle <= 155:
        return 1, 1
    elif angle <= 200:
        return 0, 1
    elif angle <= 245:
        return -1, 1
    elif angle <= 290:
        return -1, 0
    elif angle <= 335:
        return -1, -1
    else:
        return 0, -1

class Hero:

    def __init__(self, pos, land):
        self.land = land
        self.mode = True
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraBind()
        self.accept_events()

    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True

    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def tnLt(self):
        self.hero.setH((self.hero.getH() + 5) % 360)
    def tnRt(self):
        self.hero.setH((self.hero.getH() - 5) % 360)
    def look_at(self, angle):
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())
        dx, dy = check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from

    def changeMode(self):
        if self.mode:
            self.mode = False
        else:
            self.mode = True

    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)
    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)

    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ()+1)

    def dn(self):
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ()-1)

    def rt(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)

    def lt(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def fw(self):
        angle = (self.hero.getH() + 360) % 360
        self.move_to(angle)

    def bk(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)

    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)


    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockFrom(pos)


    def accept_events(self):
        base.accept(keyTnLt, self.tnLt)
        base.accept(keyTnLt + '-repeat', self.tnLt)
        base.accept(keyTnRt, self.tnRt)
        base.accept(keyTnRt + '-repeat', self.tnRt)

        base.accept(keyFw, self.fw)
        base.accept(keyFw + '-repeat', self.fw)

        base.accept(keyBk, self.bk)
        base.accept(keyBk + '-repeat', self.bk)

        base.accept(keyLt, self.lt)
        base.accept(keyLt + '-repeat', self.lt)

        base.accept(keyRt, self.rt)
        base.accept(keyRt + '-repeat', self.rt)

        base.accept(keyUp, self.up)
        base.accept(keyUp + '-repeat', self.up)

        base.accept(keyDn, self.dn)
        base.accept(keyDn + '-repeat', self.dn)

        base.accept(keyBld, self.build)
        base.accept(keyDst, self.destroy)

        base.accept(keySwCam, self.changeView)
        base.accept(keySwMode, self.changeMode)

        base.accept(keySv, self.land.saveMap)
        base.accept(keyLd, self.land.loadMap)










