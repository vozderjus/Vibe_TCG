"""
Тесты для генератора тестов поиска
"""

import pytest
from src.generators.searching_generator import SearchingGenerator, TestCase


class TestSearchingGenerator:
    """Тесты для SearchingGenerator"""

    def test_generate_normal_cases(self):
        """Тест генерации нормальных случаев"""
        generator = SearchingGenerator()
        cases = generator.generate_normal_cases(3)
        
        assert len(cases) == 3
        
        for case in cases:
            assert isinstance(case.input, dict)
            assert "array" in case.input
            assert "target" in case.input
            assert isinstance(case.input["array"], list)
            assert isinstance(case.expected, int)
            assert not case.is_edge_case
    
    def test_array_is_sorted(self):
        """Тест что массивы всегда отсортированы"""
        generator = SearchingGenerator()
        cases = generator.generate_normal_cases(5)
        
        for case in cases:
            arr = case.input["array"]
            assert arr == sorted(arr), f"Массив не отсортирован: {arr}"
    
    def test_search_results(self):
        """Тест корректности результатов поиска"""
        generator = SearchingGenerator()
        cases = generator.generate_normal_cases(10)
        
        for case in cases:
            arr = case.input["array"]
            target = case.input["target"]
            expected_idx = case.expected
            
            if expected_idx == -1:
                # Если ожидается -1, элемента не должно быть в массиве
                assert target not in arr, \
                    f"Элемент {target} есть в массиве, но ожидается -1"
            else:
                # Если ожидается индекс, элемент должен быть по этому индексу
                assert 0 <= expected_idx < len(arr), \
                    f"Индекс {expected_idx} вне границ массива"
                assert arr[expected_idx] == target, \
                    f"Элемент по индексу {expected_idx} не равен target"
    
    def test_edge_cases(self):
        """Тест генерации крайних случаев"""
        generator = SearchingGenerator()
        edge_cases = generator.generate_edge_cases()
        
        assert len(edge_cases) >= 7  # Минимум 7 предопределенных
        
        # Проверяем конкретные edge cases
        empty_case = next(
            (c for c in edge_cases if c.description.startswith("Поиск в пустом массиве")),
            None
        )
        assert empty_case is not None
        assert empty_case.input["array"] == []
        assert empty_case.expected == -1
        assert empty_case.is_edge_case
    
    def test_edge_cases_have_valid_results(self):
        """Тест что edge cases имеют корректные результаты"""
        generator = SearchingGenerator()
        edge_cases = generator.generate_edge_cases()
        
        for case in edge_cases:
            arr = case.input["array"]
            target = case.input["target"]
            expected_idx = case.expected
            
            if expected_idx == -1:
                assert target not in arr
            else:
                assert 0 <= expected_idx < len(arr)
                assert arr[expected_idx] == target
    
    @pytest.mark.parametrize("min_len,max_len", [(1, 5), (10, 30), (20, 20)])
    def test_length_constraints(self, min_len, max_len):
        """Тест ограничений по длине массива"""
        generator = SearchingGenerator(min_len=min_len, max_len=max_len)
        cases = generator.generate_normal_cases(5)
        
        for case in cases:
            arr_len = len(case.input["array"])
            assert min_len <= arr_len <= max_len
    
    def test_unique_elements_in_array(self):
        """Тест что элементы в массиве уникальны"""
        generator = SearchingGenerator()
        cases = generator.generate_normal_cases(5)
        
        for case in cases:
            arr = case.input["array"]
            # Проверяем что все элементы уникальны
            assert len(arr) == len(set(arr)), \
                f"Массив содержит дубликаты: {arr}"