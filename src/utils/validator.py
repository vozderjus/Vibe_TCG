"""
Модуль для валидации тестовых случаев
"""

from typing import List, Tuple, Optional
from ..generators.base_generator import TestCase


class Validator:
    """Класс для валидации тестовых случаев"""

    @staticmethod
    def validate_test_cases(test_cases: List[TestCase]) -> Tuple[bool, List[str]]:
        """
        Валидация списка тестовых случаев
        
        Args:
            test_cases: Список тестовых случаев для валидации
            
        Returns:
            Кортеж (валидны ли все случаи, список ошибок)
        """
        errors = []
        
        if not test_cases:
            errors.append("Список тестовых случаев пуст")
            return False, errors
        
        for i, tc in enumerate(test_cases):
            # Проверяем обязательные поля
            if tc.input is None:
                errors.append(f"Тест {i}: отсутствуют входные данные")
            
            if tc.expected is None:
                errors.append(f"Тест {i}: отсутствует ожидаемый результат")
            
            if not tc.description:
                errors.append(f"Тест {i}: отсутствует описание")
            
            # Проверяем типы данных для известных типов задач
            error = Validator._validate_specific_types(tc, i)
            if error:
                errors.append(error)
        
        return len(errors) == 0, errors
    
    @staticmethod
    def _validate_specific_types(tc: TestCase, index: int) -> Optional[str]:
        """Валидация специфичных типов данных"""
        
        # Проверка для задач сортировки
        if isinstance(tc.input, list):
            # Проверяем, что ожидаемый результат тоже список
            if not isinstance(tc.expected, list):
                return f"Тест {index}: для списка на входе ожидается список на выходе"
            
            # Проверяем, что длины совпадают
            if len(tc.input) != len(tc.expected):
                return f"Тест {index}: длина входного списка ({len(tc.input)}) " \
                       f"не совпадает с длиной ожидаемого ({len(tc.expected)})"
            
            # Проверяем, что ожидаемый результат отсортирован
            if tc.expected != sorted(tc.expected):
                return f"Тест {index}: ожидаемый результат не отсортирован"
        
        # Проверка для задач поиска
        elif isinstance(tc.input, dict) and "array" in tc.input and "target" in tc.input:
            arr = tc.input["array"]
            target = tc.input["target"]
            
            if not isinstance(arr, list):
                return f"Тест {index}: поле 'array' должно быть списком"
            
            if not isinstance(tc.expected, int):
                return f"Тест {index}: для поиска ожидается целое число"
            
            if tc.expected != -1 and (tc.expected < 0 or tc.expected >= len(arr)):
                return f"Тест {index}: индекс {tc.expected} вне границ массива"
            
            if tc.expected >= 0 and arr[tc.expected] != target:
                return f"Тест {index}: элемент по индексу {tc.expected} не равен target"
        
        # Проверка для математических задач с кортежем
        elif isinstance(tc.input, tuple) and len(tc.input) == 2:
            a, b = tc.input
            if not (isinstance(a, int) and isinstance(b, int)):
                return f"Тест {index}: оба аргумента должны быть целыми числами"
        
        return None
    
    @staticmethod
    def find_duplicates(test_cases: List[TestCase]) -> List[Tuple[int, int]]:
        """
        Поиск дубликатов среди тестовых случаев
        
        Args:
            test_cases: Список тестовых случаев
            
        Returns:
            Список пар индексов дублирующихся тестов
        """
        duplicates = []
        seen = {}
        
        for i, tc in enumerate(test_cases):
            # Создаем ключ на основе входных данных и ожидаемого результата
            key = (str(tc.input), str(tc.expected))
            
            if key in seen:
                duplicates.append((seen[key], i))
            else:
                seen[key] = i
        
        return duplicates
    
    @staticmethod
    def calculate_coverage(test_cases: List[TestCase]) -> dict:
        """
        Расчет покрытия тестовыми случаями
        
        Args:
            test_cases: Список тестовых случаев
            
        Returns:
            Словарь с метриками покрытия
        """
        normal_cases = [tc for tc in test_cases if not tc.is_edge_case]
        edge_cases = [tc for tc in test_cases if tc.is_edge_case]
        
        total_weight = sum(tc.weight for tc in test_cases)
        normal_weight = sum(tc.weight for tc in normal_cases)
        edge_weight = sum(tc.weight for tc in edge_cases)
        
        return {
            "total_cases": len(test_cases),
            "normal_cases": len(normal_cases),
            "edge_cases": len(edge_cases),
            "total_weight": total_weight,
            "normal_weight": normal_weight,
            "edge_weight": edge_weight,
            "normal_percentage": (len(normal_cases) / len(test_cases) * 100) if test_cases else 0,
            "edge_percentage": (len(edge_cases) / len(test_cases) * 100) if test_cases else 0,
        }