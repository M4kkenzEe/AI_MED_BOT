import json
from typing import Any, Optional, List, Dict


def get_elements_by_diagnosis(data: Any, diagnosis_name: str) -> Optional[List]:
    """
    Находит диагноз по имени и возвращает его elements.
    """

    def search(node: Any) -> Optional[List]:
        if isinstance(node, dict):
            for k, v in node.items():
                if k == diagnosis_name and isinstance(v, dict):
                    return v.get("elements")
                # Рекурсивный поиск
                result = search(v)
                if result is not None:
                    return result
        elif isinstance(node, list):
            for item in node:
                result = search(item)
                if result is not None:
                    return result
        return None

    return search(data)


def get_diagnose_detail(sections: List[Dict], title: str) -> Optional[str]:
    title_lower = title.strip().lower()
    for section in sections:
        if section.get("title", "").strip().lower() == title_lower:
            return section.get("content")
    return None


def get_desc_by_key(request):
    # Загружаем JSON из файла
    with open("diagnoses.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    elements = get_elements_by_diagnosis(data, request)
    return elements
