"""
Базовый класс для генераторов тестовых случаев
"""

from abc import ABC, abstractmethod
from typing import Any, List
from pydantic import BaseModel, Field


class TestCase(BaseModel):
    """Модель тестового случая"""

    input: Any
    expected: Any
    description: str = Field(default="", description="Описание тестового случая")
    is_edge_case: bool = Field(default=False, description="Является ли крайним случаем")
    weight: float = Field(default=1.0, description="Вес теста при оценивании")

    class Config:
        """Конфигурация Pydantic модели"""
        json_encoders = {
            # Добавьте кастомные энкодеры если нужно
        }


class BaseGenerator(ABC):
    """Абстрактный класс генератора тестовых случаев"""

    @abstractmethod
    def generate_normal_cases(self, n: int) -> List[TestCase]:
        """
        Генерация обычных тестовых случаев
        
        Args:
            n: Количество тестовых случаев
            
        Returns:
            Список тестовых случаев
        """
        pass

    @abstractmethod
    def generate_edge_cases(self) -> List[TestCase]:
        """
        Генерация крайних случаев
        
        Returns:
            Список крайних случаев
        """
        pass

    def generate_all(self, n_normal: int = 5) -> List[TestCase]:
        """
        Генерация всех тестовых случаев
        
        Args:
            n_normal: Количество обычных случаев
            
        Returns:
            Полный список тестовых случаев
        """
        normal_cases = self.generate_normal_cases(n_normal)
        edge_cases = self.generate_edge_cases()
        return normal_cases + edge_cases