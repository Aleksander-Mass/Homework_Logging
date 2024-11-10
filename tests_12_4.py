import unittest
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    filename='runner_tests.log',
    filemode='w',
    encoding='utf-8',
    format='%(levelname)s: %(message)s'
)


def freeze_control(func):
    def wrapper(self, *args, **kwargs):
        if self.is_frozen:
            self.skipTest("Тесты в этом кейсе заморожены")
        else:
            return func(self, *args, **kwargs)

    return wrapper


# Обновленный класс Runner с поддержкой скорости и проверкой типов
class Runner:
    def __init__(self, name, speed=5):
        if isinstance(name, str):
            self.name = name
        else:
            raise TypeError(f'Имя может быть только строкой, передано {type(name).__name__}')

        self.distance = 0
        if speed > 0:
            self.speed = speed
        else:
            raise ValueError(f'Скорость не может быть отрицательной, сейчас {speed}')

    def run(self):
        self.distance += self.speed * 2

    def walk(self):
        self.distance += self.speed

    def __str__(self):
        return self.name


# Класс тестов RunnerTest с обработкой исключений и логированием
class RunnerTest(unittest.TestCase):
    is_frozen = False  # Тесты в этом классе выполняются

    @freeze_control
    def test_walk(self):
        try:
            # Создание Runner с недопустимой отрицательной скоростью
            runner = Runner("TestRunner", speed=-5)
            for _ in range(10):
                runner.walk()
            self.assertEqual(runner.distance, 50)
            logging.info('"test_walk" выполнен успешно')
        except ValueError:
            logging.warning("Неверная скорость для Runner")

    @freeze_control
    def test_run(self):
        try:
            # Создание Runner с неверным типом данных для имени
            runner = Runner(123, speed=5)
            for _ in range(10):
                runner.run()
            self.assertEqual(runner.distance, 100)
            logging.info('"test_run" выполнен успешно')
        except TypeError:
            logging.warning("Неверный тип данных для объекта Runner")


# Запуск тестов из класса RunnerTest
if __name__ == "__main__":
    test_suite = unittest.TestSuite()
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(RunnerTest))

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)

"""
Пояснения к изменениям:
Настройка логирования:

level=logging.INFO: Логируются события уровня INFO и выше.
filename='runner_tests.log': Лог записывается в файл runner_tests.log.
filemode='w': Лог-файл перезаписывается при каждом запуске тестов.
encoding='utf-8': Используется кодировка UTF-8 для поддержки всех символов.
format='%(levelname)s: %(message)s': Формат вывода содержит уровень и сообщение.
Тест test_walk:

В try-блоке создается объект Runner с отрицательной скоростью, что вызывает исключение ValueError.
При успешном выполнении логируется сообщение INFO о завершении теста.
В except-блоке обрабатывается ValueError, логируется предупреждение уровня WARNING.
Тест test_run:

В try-блоке создается объект Runner с некорректным типом имени (int вместо str), что вызывает TypeError.
В случае успешного выполнения логируется сообщение INFO.
В except-блоке ловится TypeError, логируется предупреждение уровня WARNING.
После выполнения этого кода, в файле runner_tests.log будут записаны либо подтверждения об успешном выполнении тестов, 
либо предупреждения об ошибках и их типах.
"""