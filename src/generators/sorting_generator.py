"""
Генератор тестовых случаев для задач сортировки
"""

import random
import copy
from typing import List

from .base_generator import BaseGenerator, TestCase


class SortingGenerator(BaseGenerator):
    """Генератор тестовых случаев для задач сортировки"""

    def __init__(self, min_len: int = 0, max_len: int = 100) -> None:
        """
        Инициализация генератора
        
        Args:
            min_len: Минимальная длина массива
            max_len: Максимальная длина массива
        """
        self.min_len = max(0, min_len)
        self.max_len = max(min_len, max_len)

    def generate_normal_cases(self, n: int = 5) -> List[TestCase]:
        cases = []
        
        for i in range(n):
            # Разная сложность для разных случаев
            if i == 0:
                length = random.randint(5, 10)  # Маленький массив
            elif i == 1:
                min_val = max(50, self.min_len)
                max_val = min(100, self.max_len)
                if min_val <= max_val:
                    length = random.randint(min_val, max_val)
                else:
                    length = random.randint(self.min_len, self.max_len)
            else:
                length = random.randint(self.min_len, self.max_len)
            
            # Генерация массива
            arr = [random.randint(-1000, 1000) for _ in range(length)]
            
            # Добавление особенностей
            if length > 5 and random.random() > 0.5:
                # Добавляем дубликаты
                duplicates = random.randint(1, 3)
                for _ in range(duplicates):
                    arr.append(arr[random.randint(0, len(arr) - 1)])
            
            if random.random() > 0.7:
                # Добавляем отрицательные числа
                for j in range(len(arr)):
                    if random.random() > 0.5:
                        arr[j] = -arr[j]
            
            cases.append(
                TestCase(
                    input=arr.copy(),  # Используем copy вместо deepcopy
                    expected=sorted(arr),
                    description=f"Нормальный случай {i+1}: "
                    f"массив из {length} элементов",
                    is_edge_case=False,
                    weight=1.0,
                )
            )
    
        return cases

    def generate_edge_cases(self) -> List[TestCase]:
        """Генерация крайних случаев для сортировки"""
        edge_cases = [
            TestCase(
                input=[],
                expected=[],
                description="Пустой массив",
                is_edge_case=True,
                weight=1.5,
            ),
            TestCase(
                input=[42],
                expected=[42],
                description="Массив из одного элемента",
                is_edge_case=True,
                weight=1.2,
            ),
            TestCase(
                input=[5, 5, 5, 5, 5],
                expected=[5, 5, 5, 5, 5],
                description="Все элементы одинаковые",
                is_edge_case=True,
                weight=1.3,
            ),
            TestCase(
                input=list(range(100, 0, -1)),
                expected=list(range(1, 101)),
                description="Обратно отсортированный массив из 100 элементов",
                is_edge_case=True,
                weight=1.4,
            ),
            TestCase(
                input=[-10, -5, -1, 0, 1, 5, 10],
                expected=[-10, -5, -1, 0, 1, 5, 10],
                description="Уже отсортированный массив",
                is_edge_case=True,
                weight=1.1,
            ),
        ]

        # Добавляем случай с очень большими числами
        large_numbers = [random.randint(10**6, 10**9) for _ in range(20)]
        edge_cases.append(
            TestCase(
                input=large_numbers,
                expected=sorted(large_numbers),
                description="Массив с очень большими числами",
                is_edge_case=True,
                weight=1.3,
            )
        )

        return edge_cases