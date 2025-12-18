"""
Генератор тестовых случаев для математических задач
"""

import random
import math
from typing import List, Callable

from .base_generator import BaseGenerator, TestCase


class MathGenerator(BaseGenerator):
    """Генератор для математических задач"""

    def __init__(self) -> None:
        self.task_types = [
            self._generate_factorial,
            self._generate_fibonacci,
            self._generate_gcd,
            self._generate_prime,
            self._generate_palindrome,
        ]

    def generate_normal_cases(self, n: int = 5) -> List[TestCase]:
        cases = []

        for i in range(n):
            # Выбираем случайный тип задачи
            generator = random.choice(self.task_types)
            test_case = generator(normal_case=True)
            test_case.description = f"Нормальный случай {i+1}: {test_case.description}"
            cases.append(test_case)

        return cases

    def generate_edge_cases(self) -> List[TestCase]:
        edge_cases = []

        # Факториал крайние случаи
        edge_cases.extend([
            TestCase(
                input=0,
                expected=1,
                description="Факториал 0",
                is_edge_case=True,
                weight=1.5,
            ),
            TestCase(
                input=1,
                expected=1,
                description="Факториал 1",
                is_edge_case=True,
                weight=1.2,
            ),
        ])

        # Числа Фибоначчи крайние случаи
        edge_cases.extend([
            TestCase(
                input=0,
                expected=0,
                description="Число Фибоначчи F(0)",
                is_edge_case=True,
                weight=1.5,
            ),
            TestCase(
                input=1,
                expected=1,
                description="Число Фибоначчи F(1)",
                is_edge_case=True,
                weight=1.2,
            ),
            TestCase(
                input=2,
                expected=1,
                description="Число Фибоначчи F(2)",
                is_edge_case=True,
                weight=1.1,
            ),
        ])

        # НОД крайние случаи
        edge_cases.extend([
            TestCase(
                input=(0, 5),
                expected=5,
                description="НОД(0, 5) - один аргумент ноль",
                is_edge_case=True,
                weight=1.5,
            ),
            TestCase(
                input=(5, 0),
                expected=5,
                description="НОД(5, 0) - один аргумент ноль",
                is_edge_case=True,
                weight=1.5,
            ),
            TestCase(
                input=(1, 100),
                expected=1,
                description="НОД(1, 100) - один из аргументов 1",
                is_edge_case=True,
                weight=1.2,
            ),
            TestCase(
                input=(17, 17),
                expected=17,
                description="НОД одинаковых чисел",
                is_edge_case=True,
                weight=1.1,
            ),
        ])

        return edge_cases

    def _generate_factorial(self, normal_case: bool = True) -> TestCase:
        if normal_case:
            n = random.randint(2, 10)  # Ограничиваем для простоты
        else:
            n = random.choice([0, 1])  # Для edge cases

        return TestCase(
            input=n,
            expected=math.factorial(n),
            description=f"Вычислить факториал {n}!",
            is_edge_case=not normal_case,
            weight=1.3 if not normal_case else 1.0,
        )

    def _generate_fibonacci(self, normal_case: bool = True) -> TestCase:
        if normal_case:
            n = random.randint(3, 15)
        else:
            n = random.choice([0, 1, 2])

        def fib(x: int) -> int:
            if x <= 1:
                return x
            a, b = 0, 1
            for _ in range(x - 1):
                a, b = b, a + b
            return b

        return TestCase(
            input=n,
            expected=fib(n),
            description=f"Найти {n}-е число Фибоначчи",
            is_edge_case=not normal_case,
            weight=1.3 if not normal_case else 1.0,
        )

    def _generate_gcd(self, normal_case: bool = True) -> TestCase:
        if normal_case:
            a = random.randint(10, 100)
            b = random.randint(10, 100)
        else:
            # Для edge cases
            options = [(0, 5), (5, 0), (1, 100), (17, 17)]
            a, b = random.choice(options)

        return TestCase(
            input=(a, b),
            expected=math.gcd(a, b),
            description=f"Найти наибольший общий делитель чисел {a} и {b}",
            is_edge_case=not normal_case,
            weight=1.3 if not normal_case else 1.0,
        )

    def _generate_prime(self, normal_case: bool = True) -> TestCase:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        non_primes = [1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20]

        if normal_case:
            if random.random() > 0.5:
                n = random.choice(primes)
                expected = True
            else:
                n = random.choice(non_primes)
                expected = False
        else:
            # Edge cases
            n = random.choice([0, 1, 2])
            expected = n in [2]

        return TestCase(
            input=n,
            expected=expected,
            description=f"Проверить, является ли число {n} простым",
            is_edge_case=not normal_case,
            weight=1.3 if not normal_case else 1.0,
        )

    def _generate_palindrome(self, normal_case: bool = True) -> TestCase:
        if normal_case:
            if random.random() > 0.5:
                # Генерируем палиндром
                half = str(random.randint(10, 999))
                n = int(half + half[::-1])
                expected = True
            else:
                # Генерируем не палиндром
                while True:
                    n = random.randint(100, 9999)
                    if str(n) != str(n)[::-1]:
                        expected = False
                        break
        else:
            # Edge cases для палиндромов
            n = random.choice([0, 1, 9, 11, 99])
            expected = str(n) == str(n)[::-1]

        return TestCase(
            input=n,
            expected=expected,
            description=f"Проверить, является ли число {n} палиндромом",
            is_edge_case=not normal_case,
            weight=1.3 if not normal_case else 1.0,
        )