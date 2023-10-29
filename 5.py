# Следующим шагом мы заставим панду перемещаться назад-вперёд:

from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Отключаем управление камерой которое было создано ShowBase.
        self.disableMouse()

        # Загрузка модели.
        self.scene = self.loader.loadModel("models/environment")
        # Прицепляем модель к узлу рендера.
        self.scene.reparentTo(self.render)
        # Устанавливаем масштаб и позицию для модели.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Добавляем в менеджер задач, запуск функции.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # Загрузка модели актера и анимации ходьбы.
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # Зацикливаем анимацию.
        self.pandaActor.loop("walk")

        # Создаем интервал для изменения позиции за 13 секунд.
        # Так же создаем интервал для изменение ориентации за 3 секунды.
        # Для имитации ходьбы, вперед и назад, а так же разворот на 180 градусов.
        pandaPosInterval1 = self.pandaActor.posInterval(13,
                                                        Point3(0, -10, 0),
                                                        startPos=Point3(0, 10, 0))
        pandaPosInterval2 = self.pandaActor.posInterval(13,
                                                        Point3(0, 10, 0),
                                                        startPos=Point3(0, -10, 0))
        pandaHprInterval1 = self.pandaActor.hprInterval(3,
                                                        Point3(180, 0, 0),
                                                        startHpr=Point3(0, 0, 0))
        pandaHprInterval2 = self.pandaActor.hprInterval(3,
                                                        Point3(0, 0, 0),
                                                        startHpr=Point3(180, 0, 0))

        # Создадим секвенцию для поочередного выполнения интервалов.
        self.pandaPace = Sequence(pandaPosInterval1,
                                  pandaHprInterval1,
                                  pandaPosInterval2,
                                  pandaHprInterval2,
                                  name="pandaPace")
        self.pandaPace.loop()

    # Функция которая обрабатывает управление камерой.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0

        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont


app = MyApp()
app.run()


# Интервалы (interval) — это фоновые задачи (tasks) которые меняют параметры от одного значения к другому
# в течение заданного времени. Например, рассмотрим pandaPosInterval1.
# Когда интервал запущен он постепенно меняет позицию панды от (0,10,0) до (0,-10,0) за период в 13 секунд.
# Аналогично pandaHprInterval1 меняет ориентацию — поворачивает панду на 180 градусов в течение 3 секунд.
#
# Последовательность (Sequences) — задача, которая запускает интервалы один за другим. PandaPace — последовательность,
# которая перемещает панду по прямой, затем разворачивает на 180 градусов и перемещает обратно, и снова поворачивает.
# PandaPace.loop() стартует последовательность в режиме цикла.
#
# В результате наша панда должна перемещаться между деревьями туда-сюда.