"""
Генератор тестовых случаев для задач поиска
"""

import random
import copy
from typing import List, Dict, Any

from .base_generator import BaseGenerator, TestCase


class SearchingGenerator(BaseGenerator):
    """Генератор для задач поиска (бинарный поиск, линейный поиск)"""

    def __init__(self, min_len: int = 1, max_len: int = 50) -> None:
        self.min_len = min_len
        self.max_len = max_len

    def generate_normal_cases(self, n: int = 5) -> List[TestCase]:
        cases = []

        for i in range(n):
            # Генерация отсортированного массива
            length = random.randint(self.min_len, self.max_len)
            
            # Создаем массив с уникальными элементами
            arr = []
            while len(arr) < length:
                num = random.randint(1, 1000)
                if num not in arr:
                    arr.append(num)
            
            arr.sort()

            # Выбор элемента для поиска
            if random.random() > 0.3:  # 70% что элемент есть
                target = random.choice(arr)
                expected = arr.index(target)
                desc_suffix = f"элемент {target} присутствует в массиве"
            else:  # 30% что элемента нет
                # Генерируем число которого точно нет в массиве
                target = 1001
                while target in arr:
                    target = random.randint(1001, 2000)
                expected = -1
                desc_suffix = f"элемент {target} отсутствует в массиве"

            cases.append(
                TestCase(
                    input={"array": copy.deepcopy(arr), "target": target},
                    expected=expected,
                    description=(
                        f"Поиск элемента в отсортированном массиве "
                        f"из {length} элементов. {desc_suffix}"
                    ),
                    is_edge_case=False,
                    weight=1.0,
                )
            )

        return cases

    def generate_edge_cases(self) -> List[TestCase]:
        return [
            TestCase(
                input={"array": [], "target": 5},
                expected=-1,
                description="Поиск в пустом массиве",
                is_edge_case=True,
                weight=1.5,
            ),
            TestCase(
                input={"array": [1], "target": 1},
                expected=0,
                description="Поиск в массиве из одного элемента (элемент есть)",
                is_edge_case=True,
                weight=1.2,
            ),
            TestCase(
                input={"array": [1], "target": 2},
                expected=-1,
                description="Поиск в массиве из одного элемента (элемента нет)",
                is_edge_case=True,
                weight=1.2,
            ),
            TestCase(
                input={"array": [1, 2, 3, 4, 5], "target": 1},
                expected=0,
                description="Поиск первого элемента",
                is_edge_case=True,
                weight=1.1,
            ),
            TestCase(
                input={"array": [1, 2, 3, 4, 5], "target": 5},
                expected=4,
                description="Поиск последнего элемента",
                is_edge_case=True,
                weight=1.1,
            ),
            TestCase(
                input={"array": [1, 2, 2, 2, 3], "target": 2},
                expected=1,  # Первое вхождение
                description="Поиск элемента с дубликатами",
                is_edge_case=True,
                weight=1.3,
            ),
            TestCase(
                input={"array": [1, 3, 5, 7, 9], "target": 4},
                expected=-1,
                description="Поиск элемента который должен быть в середине но отсутствует",
                is_edge_case=True,
                weight=1.2,
            ),
        ]