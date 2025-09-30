from typing import List, Dict
from dataclasses import dataclass


# ========================
# Класи для завдань і обмежень
# ========================
@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


# ========================
# Основна функція оптимізації
# ========================
def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: список завдань на друк
        constraints: словник з обмеженнями принтера

    Returns:
        dict: порядок друку та загальний час
    """
    jobs = [PrintJob(**job) for job in print_jobs]
    constraints = PrinterConstraints(**constraints)

    jobs.sort(key=lambda x: x.priority)

    print_order = []
    total_time = 0

    while jobs:
        batch = []
        batch_volume = 0

        for job in list(jobs):  
            if len(batch) < constraints.max_items and batch_volume + job.volume <= constraints.max_volume:
                batch.append(job)
                batch_volume += job.volume

        if not batch:  
            batch.append(jobs[0])

        for job in batch:
            print_order.append(job.id)
            jobs.remove(job)

        batch_time = max(job.print_time for job in batch)
        total_time += batch_time

    return {
        "print_order": print_order,
        "total_time": total_time
    }


# ========================
# Тестування
# ========================
def test_printing_optimization():
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},   
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}   
    ]

    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("=== Тест 1 (однаковий пріоритет) ===")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\n=== Тест 2 (різні пріоритети) ===")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\n=== Тест 3 (перевищення обмежень) ===")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


# ========================
# Точка входу
# ========================
if __name__ == "__main__":
    test_printing_optimization()
