"""
Тесты для генератора тестов сортировки
"""

import pytest
from src.generators.sorting_generator import SortingGenerator, TestCase


class TestSortingGenerator:
    """Тесты для SortingGenerator"""

    def test_initialization(self):
        """Тест инициализации генератора"""
        generator = SortingGenerator(min_len=5, max_len=20)
        assert generator.min_len == 5
        assert generator.max_len == 20
    
    def test_generate_normal_cases_count(self):
        """Тест количества генерируемых нормальных случаев"""
        generator = SortingGenerator()
        cases = generator.generate_normal_cases(3)
        
        assert len(cases) == 3
        assert all(isinstance(case, TestCase) for case in cases)
    
    def test_generate_normal_cases_content(self):
        """Тест содержания нормальных случаев"""
        generator = SortingGenerator(min_len=3, max_len=10)
        cases = generator.generate_normal_cases(2)
        
        for case in cases:
            assert isinstance(case.input, list)
            assert isinstance(case.expected, list)
            assert len(case.input) == len(case.expected)
            assert case.expected == sorted(case.input)
            assert not case.is_edge_case
            assert case.weight == 1.0
    
    def test_generate_edge_cases(self):
        """Тест генерации крайних случаев"""
        generator = SortingGenerator()
        edge_cases = generator.generate_edge_cases()
        
        assert len(edge_cases) >= 5  # Минимум 5 предопределенных
        
        # Проверяем конкретные edge cases
        empty_case = next(
            (c for c in edge_cases if c.description == "Пустой массив"),
            None
        )
        assert empty_case is not None
        assert empty_case.input == []
        assert empty_case.expected == []
        assert empty_case.is_edge_case
        assert empty_case.weight == 1.5
    
    def test_generate_all(self):
        """Тест генерации всех случаев"""
        generator = SortingGenerator()
        all_cases = generator.generate_all(n_normal=2)
        
        assert len(all_cases) >= 7  # 2 нормальных + минимум 5 крайних
        
        normal_count = sum(1 for c in all_cases if not c.is_edge_case)
        edge_count = sum(1 for c in all_cases if c.is_edge_case)
        
        assert normal_count == 2
        assert edge_count >= 5
    
    def test_edge_cases_have_higher_weight(self):
        """Тест что edge cases имеют больший вес"""
        generator = SortingGenerator()
        edge_cases = generator.generate_edge_cases()
        
        for case in edge_cases:
            assert case.is_edge_case
            assert case.weight >= 1.0  # Вес должен быть >= 1.0
    
    @pytest.mark.parametrize("min_len,max_len", [(0, 5), (10, 20), (1, 1)])
    def test_length_constraints(self, min_len, max_len):
        """Тест ограничений по длине массива"""
        generator = SortingGenerator(min_len=min_len, max_len=max_len)
        cases = generator.generate_normal_cases(5)
        
        for case in cases:
            assert min_len <= len(case.input) <= max_len
    
    def test_sorted_output(self):
        """Тест что ожидаемый результат всегда отсортирован"""
        generator = SortingGenerator()
        all_cases = generator.generate_all(n_normal=3)
        
        for case in all_cases:
            if isinstance(case.expected, list):
                assert case.expected == sorted(case.expected)