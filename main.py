"""Консольная информационная система демонстрации алгоритмов сортировки.

Алгоритмы загружаются из отдельного Git-подмодуля algorithms.
"""
import argparse
import importlib
import sys

EXAMPLE = [9, -3, 7, 0, 7, 2, -10, 5]
METHODS = (
    ('bubble', 'Сортировка пузырьком', 'bubble_sort'),
    ('insertion', 'Сортировка вставками', 'insertion_sort'),
    ('selection', 'Сортировка выбором', 'selection_sort'),
    ('cocktail', 'Шейкерная сортировка', 'cocktail_sort'),
)


def parse_numbers(value: str) -> list[int]:
    """Преобразует числа через пробел или запятую в список целых чисел."""
    tokens = value.replace(',', ' ').split()
    if not tokens:
        raise ValueError('Введите хотя бы одно целое число.')
    try:
        return [int(part) for part in tokens]
    except ValueError as exc:
        raise ValueError('Разрешены только целые числа, разделенные пробелом или запятой.') from exc


def load_methods() -> dict[str, tuple[str, object]]:
    try:
        module = importlib.import_module('algorithms.sorting')
    except ModuleNotFoundError as exc:
        if exc.name and (exc.name == 'algorithms' or exc.name.startswith('algorithms.')):
            raise RuntimeError(
                'Git-подмодуль algorithms не найден. '
                'Выполните: git submodule update --init --recursive'
            ) from exc
        raise
    result = {}
    for key, label, function_name in METHODS:
        func = getattr(module, function_name, None)
        if callable(func):
            result[key] = (label, func)
    if not result:
        raise RuntimeError('В подмодуле не найдено доступных алгоритмов сортировки.')
    return result


def run_sort(numbers: list[int], name: str = 'bubble') -> tuple[str, list[int]]:
    methods = load_methods()
    if name not in methods:
        raise ValueError('Алгоритм не найден. Доступны: ' + ', '.join(methods))
    label, func = methods[name]
    output = func(numbers)
    if sorted(numbers) != output:
        raise RuntimeError('Алгоритм вернул некорректный результат.')
    if numbers is output:
        raise RuntimeError('Алгоритм обязан возвращать новый список.')
    return label, output


def print_comparison(numbers: list[int]) -> None:
    print('\nИсходный массив:', numbers)
    for method in load_methods():
        label, output = run_sort(numbers, method)
        print(f'{label}: {output}')
    print('Проверка: все алгоритмы вернули одинаковый отсортированный массив.')


def interactive() -> None:
    print('=' * 55)
    print('ИНФОРМАЦИОННАЯ СИСТЕМА «АЛГОРИТМЫ СОРТИРОВКИ»')
    print('Алгоритмы загружаются из Git-подмодуля algorithms')
    print('=' * 55)
    while True:
        text = input('\nВведите целые числа через пробел (Enter — выход): ').strip()
        if not text:
            print('Работа завершена.')
            return
        try:
            numbers = parse_numbers(text)
            print_comparison(numbers)
        except (ValueError, RuntimeError) as exc:
            print('Ошибка:', exc)


def main() -> int:
    parser = argparse.ArgumentParser(description='Приложение для демонстрации алгоритмов сортировки')
    parser.add_argument('--demo', action='store_true', help='запустить пример без ввода')
    parser.add_argument('--numbers', help='числа через пробел или запятую')
    args = parser.parse_args()
    try:
        if args.demo:
            print_comparison(EXAMPLE)
        elif args.numbers is not None:
            print_comparison(parse_numbers(args.numbers))
        else:
            interactive()
        return 0
    except (ValueError, RuntimeError) as exc:
        print('Ошибка:', exc, file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
