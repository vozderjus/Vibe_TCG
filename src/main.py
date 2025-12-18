#!/usr/bin/env python3
"""
Основной CLI интерфейс для генератора тестовых случаев
"""

import argparse
import sys
from typing import Dict, Type

from generators.sorting_generator import SortingGenerator
from generators.searching_generator import SearchingGenerator
from generators.math_generator import MathGenerator
from utils.exporter import Exporter


class TestCaseGeneratorCLI:
    """Командный интерфейс для генератора тестовых случаев"""

    GENERATORS: Dict[str, Type] = {
        "sorting": SortingGenerator,
        "searching": SearchingGenerator,
        "math": MathGenerator,
    }

    FORMATS = ["json", "yaml", "python"]

    def __init__(self) -> None:
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Генератор тестовых случаев для задач программирования",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Примеры использования:
  %(prog)s sorting -n 10 -o tests.json
  %(prog)s searching --format yaml
  %(prog)s math --no-edge-cases
            """,
        )

        parser.add_argument(
            "task_type",
            choices=list(self.GENERATORS.keys()),
            help="Тип задачи для генерации тестов",
        )

        parser.add_argument(
            "-n",
            "--normal-cases",
            type=int,
            default=5,
            help="Количество обычных тестовых случаев (по умолчанию: 5)",
        )

        parser.add_argument(
            "-o",
            "--output",
            type=str,
            default="test_cases.json",
            help="Имя выходного файла (по умолчанию: test_cases.json)",
        )

        parser.add_argument(
            "-f",
            "--format",
            choices=self.FORMATS,
            default="json",
            help="Формат выходного файла (по умолчанию: json)",
        )

        parser.add_argument(
            "--no-edge-cases",
            action="store_true",
            help="Не включать крайние случаи",
        )

        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Подробный вывод",
        )

        parser.add_argument(
            "-v", "--version", action="version", version=f"%(prog)s {__version__}"
        )

        return parser

    def run(self) -> None:
        """Запуск CLI интерфейса"""
        args = self.parser.parse_args()

        try:
            # Создание генератора
            generator_class = self.GENERATORS[args.task_type]
            generator = generator_class()

            # Генерация тестовых случаев
            test_cases = generator.generate_normal_cases(args.normal_cases)

            if not args.no_edge_cases:
                edge_cases = generator.generate_edge_cases()
                test_cases.extend(edge_cases)

            # Вывод информации
            if args.verbose:
                print(f"✅ Сгенерировано {len(test_cases)} тестовых случаев")
                print(f"📊 Нормальных случаев: {args.normal_cases}")
                print(f"🚨 Крайних случаев: {0 if args.no_edge_cases else len(edge_cases)}")

            # Экспорт
            if args.format == "json":
                Exporter.to_json(test_cases, args.output)
            elif args.format == "yaml":
                Exporter.to_yaml(test_cases, args.output)
            elif args.format == "python":
                Exporter.to_python(test_cases, args.output)

            if args.verbose:
                print(f"📁 Результат сохранен в {args.output}")

        except Exception as e:
            print(f"❌ Ошибка: {e}", file=sys.stderr)
            sys.exit(1)


def main() -> None:
    """Точка входа"""
    cli = TestCaseGeneratorCLI()
    cli.run()


if __name__ == "__main__":
    main()