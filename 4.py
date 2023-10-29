# Теперь загрузим анимированного персонажа — допишем код:

from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

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
        # Loop its animation.
        self.pandaActor.loop("walk")

    # Функция которая обрабатывает управление камерой.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0

        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont


app = MyApp()
app.run()


# Класс Actor предназначен для анимированных моделей. Мы используем loadModel для статических моделей,
# и Actor только если они анимированы. Два аргумента конструктора класса Actor — первый - имя файла, содержащего модель,
# второй — словарь, содержащий записи о файлах анимации.
#
# Команда loop("walk") запускает анимацию на циклическое воспроизведение. В результате модель панды топчется на месте.