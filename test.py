from panda3d.ode import OdeWorld, OdeBody, OdeMass, OdeTriMeshData
from panda3d.ode import OdeTriMeshGeom
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.world = OdeWorld()
        self.world.setGravity(0, 0, -9.81)

        self.create_blocks()

        taskMgr.add(self.update_physics, "update_physics")

    def create_blocks(self):
        for x in range(-5, 6):
            for y in range(-5, 6):
                geom = self.create_block((x, y, 0))
                geom.reparentTo(render)

    def create_block(self, pos):
        trimesh_data = OdeTriMeshData()
        trimesh_data.addBox(Vec3(0, 0, 0), Vec3(0.5, 0.5, 0.5))

        geom = OdeTriMeshGeom(self.world, trimesh_data)
        geom.setPos(*pos)

        body = OdeBody(self.world)
        mass = OdeMass()
        mass.setBox(1.0, 1.0, 1.0, 1.0)
        body.setMass(mass)
        geom.setBody(body)

        return geom

    def update_physics(self, task):
        dt = globalClock.getDt()
        self.world.quickStep(dt)
        return Task.cont

app = MyApp()
app.run()