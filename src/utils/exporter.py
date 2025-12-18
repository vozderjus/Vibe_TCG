"""
Модуль для экспорта тестовых случаев в разные форматы
"""

import json
import yaml
from pathlib import Path
from typing import List, Any

from ..generators.base_generator import TestCase


class Exporter:
    """Класс для экспорта тестовых случаев"""

    @staticmethod
    def to_json(test_cases: List[TestCase], filename: str) -> None:
        """
        Экспорт тестовых случаев в JSON формате
        
        Args:
            test_cases: Список тестовых случаев
            filename: Имя файла для сохранения
        """
        data = [tc.dict() for tc in test_cases]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def to_yaml(test_cases: List[TestCase], filename: str) -> None:
        """
        Экспорт тестовых случаев в YAML формате
        
        Args:
            test_cases: Список тестовых случаев
            filename: Имя файла для сохранения
        """
        data = [tc.dict() for tc in test_cases]
        
        with open(filename, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
    
    @staticmethod
    def to_python(test_cases: List[TestCase], filename: str) -> None:
        """
        Экспорт тестовых случаев в Python файл для pytest
        
        Args:
            test_cases: Список тестовых случаев
            filename: Имя файла для сохранения
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("import pytest\n\n")
            f.write("# Автоматически сгенерированные тестовые случаи\n")
            f.write("# Для использования импортируйте вашу функцию и раскомментируйте assert\n\n")
            
            for i, tc in enumerate(test_cases):
                f.write(f"def test_case_{i:03d}():\n")
                f.write(f'    """{tc.description}"""\n')
                f.write(f"    input_data = {repr(tc.input)}\n")
                f.write(f"    expected = {repr(tc.expected)}\n")
                f.write("    \n")
                f.write("    # Раскомментируйте и замените на вашу функцию:\n")
                f.write("    # result = your_function(input_data)\n")
                f.write("    # assert result == expected\n")
                
                if tc.is_edge_case:
                    f.write("    # Этот тест является крайним случаем\n")
                
                f.write("    \n")
                f.write("    # Временно всегда проходит:\n")
                f.write("    assert True\n\n")
    
    @staticmethod
    def to_markdown(test_cases: List[TestCase], filename: str) -> None:
        """
        Экспорт тестовых случаев в Markdown формат
        
        Args:
            test_cases: Список тестовых случаев
            filename: Имя файла для сохранения
        """
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Тестовые случаи\n\n")
            f.write(f"Всего случаев: {len(test_cases)}\n\n")
            
            normal_count = sum(1 for tc in test_cases if not tc.is_edge_case)
            edge_count = len(test_cases) - normal_count
            
            f.write(f"- Нормальных случаев: {normal_count}\n")
            f.write(f"- Крайних случаев: {edge_count}\n\n")
            
            f.write("## Список тестовых случаев\n\n")
            
            for i, tc in enumerate(test_cases, 1):
                case_type = "🚨 Крайний" if tc.is_edge_case else "✅ Нормальный"
                f.write(f"### Тест {i}: {case_type}\n\n")
                f.write(f"**Описание:** {tc.description}\n\n")
                f.write(f"**Входные данные:**\n```python\n{tc.input}\n```\n\n")
                f.write(f"**Ожидаемый результат:**\n```python\n{tc.expected}\n```\n\n")
                f.write(f"**Вес:** {tc.weight}\n\n")
                f.write("---\n\n")