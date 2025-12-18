"""
Тесты для валидатора тестовых случаев
"""

import pytest
from src.utils.validator import Validator
from src.generators.base_generator import TestCase


class TestValidator:
    """Тесты для Validator"""

    def test_validate_empty_list(self):
        """Тест валидации пустого списка"""
        is_valid, errors = Validator.validate_test_cases([])
        
        assert not is_valid
        assert "Список тестовых случаев пуст" in errors
    
    def test_validate_valid_sorting_cases(self):
        """Тест валидации корректных случаев сортировки"""
        test_cases = [
            TestCase(
                input=[3, 1, 2],
                expected=[1, 2, 3],
                description="Сортировка массива",
            ),
            TestCase(
                input=[],
                expected=[],
                description="Пустой массив",
            ),
        ]
        
        is_valid, errors = Validator.validate_test_cases(test_cases)
        
        assert is_valid
        assert len(errors) == 0
    
    def test_validate_invalid_sorting_cases(self):
        """Тест валидации некорректных случаев сортировки"""
        test_cases = [
            TestCase(
                input=[3, 1, 2],
                expected=[1, 2],  # Неправильная длина
                description="Некорректная длина",
            ),
            TestCase(
                input=[3, 1, 2],
                expected=[3, 1, 2],  # Не отсортирован
                description="Не отсортирован",
            ),
        ]
        
        is_valid, errors = Validator.validate_test_cases(test_cases)
        
        assert not is_valid
        assert len(errors) == 2
    
    def test_validate_searching_cases(self):
        """Тест валидации случаев поиска"""
        test_cases = [
            TestCase(
                input={"array": [1, 2, 3], "target": 2},
                expected=1,
                description="Поиск существующего элемента",
            ),
            TestCase(
                input={"array": [1, 2, 3], "target": 4},
                expected=-1,
                description="Поиск отсутствующего элемента",
            ),
        ]
        
        is_valid, errors = Validator.validate_test_cases(test_cases)
        
        assert is_valid
        assert len(errors) == 0
    
    def test_validate_invalid_searching_cases(self):
        """Тест валидации некорректных случаев поиска"""
        test_cases = [
            TestCase(
                input={"array": [1, 2, 3], "target": 2},
                expected=5,  # Индекс вне границ
                description="Некорректный индекс",
            ),
            TestCase(
                input={"array": [1, 2, 3], "target": 2},
                expected=0,  # Неправильный индекс
                description="Неправильный индекс",
            ),
        ]
        
        is_valid, errors = Validator.validate_test_cases(test_cases)
        
        assert not is_valid
        assert len(errors) == 2
    
    def test_find_duplicates(self):
        """Тест поиска дубликатов"""
        test_cases = [
            TestCase(input=[1, 2, 3], expected=[1, 2, 3], description="Тест 1"),
            TestCase(input=[4, 5, 6], expected=[4, 5, 6], description="Тест 2"),
            TestCase(input=[1, 2, 3], expected=[1, 2, 3], description="Тест 3"),  # Дубликат
            TestCase(input=[7, 8, 9], expected=[7, 8, 9], description="Тест 4"),
        ]
        
        duplicates = Validator.find_duplicates(test_cases)
        
        assert len(duplicates) == 1
        assert duplicates[0] == (0, 2)  # Индексы дублирующихся тестов
    
    def test_calculate_coverage(self):
        """Тест расчета покрытия"""
        test_cases = [
            TestCase(
                input=[1, 2, 3],
                expected=[1, 2, 3],
                description="Нормальный",
                is_edge_case=False,
                weight=1.0,
            ),
            TestCase(
                input=[],
                expected=[],
                description="Крайний",
                is_edge_case=True,
                weight=1.5,
            ),
            TestCase(
                input=[4, 5, 6],
                expected=[4, 5, 6],
                description="Нормальный",
                is_edge_case=False,
                weight=1.0,
            ),
        ]
        
        coverage = Validator.calculate_coverage(test_cases)
        
        assert coverage["total_cases"] == 3
        assert coverage["normal_cases"] == 2
        assert coverage["edge_cases"] == 1
        assert coverage["total_weight"] == 3.5
        assert coverage["normal_weight"] == 2.0
        assert coverage["edge_weight"] == 1.5
        assert coverage["normal_percentage"] == pytest.approx(66.666, 0.001)
        assert coverage["edge_percentage"] == pytest.approx(33.333, 0.001)
    
    def test_missing_fields(self):
        """Тест отсутствующих полей"""
        test_cases = [
            TestCase(
                input=None,  # Отсутствуют входные данные
                expected=[1, 2, 3],
                description="Тест",
            ),
            TestCase(
                input=[1, 2, 3],
                expected=None,  # Отсутствует ожидаемый результат
                description="Тест",
            ),
            TestCase(
                input=[1, 2, 3],
                expected=[1, 2, 3],
                description="",  # Пустое описание
            ),
        ]
        
        is_valid, errors = Validator.validate_test_cases(test_cases)
        
        assert not is_valid
        assert len(errors) == 3