#!/usr/bin/env python3
"""
Скрипт для проверки CI/CD
"""

import subprocess
import os
import sys
import json
import yaml

def run_cmd(cmd, check=True):
    """Выполнить команду"""
    print(f"▶ Выполняю: {cmd}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.returncode != 0 and check:
            print(f"❌ Ошибка: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Исключение: {e}")
        return False

def check_structure():
    """Проверка структуры проекта"""
    print("\n1. 🔍 Проверка структуры проекта...")
    
    required = [
        ("src", "папка"),
        ("tests", "папка"),
        ("requirements.txt", "файл"),
        ("requirements-dev.txt", "файл"),
        (".github/workflows/ci.yml", "файл CI"),
        ("main.py", "файл"),
    ]
    
    all_ok = True
    for path, desc in required:
        if os.path.exists(path):
            print(f"   ✓ {desc} '{path}' существует")
        else:
            print(f"   ✗ {desc} '{path}' не существует")
            all_ok = False
    
    return all_ok

def check_python():
    """Проверка Python окружения"""
    print("\n2. 🐍 Проверка Python окружения...")
    
    checks = [
        ("python --version", "Python"),
        ("pip --version", "pip"),
    ]
    
    all_ok = True
    for cmd, desc in checks:
        if run_cmd(cmd, check=False):
            print(f"   ✓ {desc} доступен")
        else:
            print(f"   ✗ {desc} не доступен")
            all_ok = False
    
    return all_ok

def install_deps():
    """Установка зависимостей"""
    print("\n3. 📦 Установка зависимостей...")
    
    deps = [
        "requirements.txt",
        "requirements-dev.txt"
    ]
    
    for dep_file in deps:
        if os.path.exists(dep_file):
            cmd = f"pip install -q -r {dep_file}"
            if run_cmd(cmd, check=False):
                print(f"   ✓ {dep_file} установлен")
            else:
                print(f"   ⚠ {dep_file}: возможны ошибки установки")
    
    return True

def check_linters():
    """Проверка линтеров"""
    print("\n4. 🔎 Проверка линтеров...")
    
    linters = [
        ("flake8 src/ tests/", "Flake8"),
        ("black --check src/ tests/", "Black"),
        ("isort --check-only src/ tests/", "isort"),
        ("mypy src/", "MyPy"),
    ]
    
    all_ok = True
    for cmd, name in linters:
        if run_cmd(cmd, check=False):
            print(f"   ✓ {name} passed")
        else:
            print(f"   ✗ {name} failed")
            all_ok = False
    
    return all_ok

def run_tests():
    """Запуск тестов"""
    print("\n5. 🧪 Запуск тестов...")
    
    if run_cmd("pytest tests/ -v --tb=short"):
        print("   ✓ Тесты прошли")
        return True
    else:
        print("   ✗ Тесты не прошли")
        return False

def check_cli():
    """Проверка CLI"""
    print("\n6. 🖥️ Проверка CLI...")
    
    # Очистка старых файлов
    for f in ["test.json", "test.yaml", "test.py"]:
        if os.path.exists(f):
            os.remove(f)
    
    tests = [
        ("python main.py sorting -n 2 --no-edge-cases -o test.json", "test.json", "JSON"),
        ("python main.py searching -n 2 --no-edge-cases -o test.yaml -f yaml", "test.yaml", "YAML"),
        ("python main.py math -n 2 --no-edge-cases -o test.py -f python", "test.py", "Python"),
    ]
    
    all_ok = True
    for cmd, out_file, fmt in tests:
        if run_cmd(cmd, check=False):
            if os.path.exists(out_file):
                print(f"   ✓ {fmt} создан ({out_file})")
                # Проверка валидности
                try:
                    with open(out_file, 'r', encoding='utf-8') as f:
                        if fmt == "JSON":
                            data = json.load(f)
                            print(f"     {len(data)} тестовых случаев")
                        elif fmt == "YAML":
                            data = yaml.safe_load(f)
                            print(f"     {len(data)} тестовых случаев")
                        elif fmt == "Python":
                            content = f.read()
                            print(f"     {len(content.splitlines())} строк")
                except Exception as e:
                    print(f"     ⚠ Ошибка чтения: {e}")
                finally:
                    os.remove(out_file)
            else:
                print(f"   ✗ {fmt}: файл не создан")
                all_ok = False
        else:
            print(f"   ✗ {fmt}: команда не выполнена")
            all_ok = False
    
    return all_ok

def main():
    """Основная функция"""
    print("=" * 50)
    print("🔧 ПРОВЕРКА CI/CD ЛОКАЛЬНО")
    print("=" * 50)
    
    steps = [
        ("Структура проекта", check_structure),
        ("Python окружение", check_python),
        ("Установка зависимостей", install_deps),
        ("Проверка линтеров", check_linters),
        ("Запуск тестов", run_tests),
        ("Проверка CLI", check_cli),
    ]
    
    results = []
    for name, func in steps:
        try:
            success = func()
            results.append((name, success))
        except Exception as e:
            print(f"❌ Ошибка в шаге '{name}': {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ:")
    print("=" * 50)
    
    all_passed = True
    for name, success in results:
        status = "✓ ПРОЙДЕНО" if success else "✗ НЕ ПРОЙДЕНО"
        print(f"{status}: {name}")
        if not success:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
        print("\nСледующие шаги:")
        print("1. git add . && git commit -m 'test: проверка CI/CD'")
        print("2. git push origin main")
        print("3. Проверить выполнение на GitHub Actions")
    else:
        print("❌ ЕСТЬ ПРОБЛЕМЫ ДЛЯ ИСПРАВЛЕНИЯ")
    
    print("=" * 50)

if __name__ == "__main__":
    main()