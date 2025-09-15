import json
from typing import Any, List


def get_elements_by_diagnosis1(data: Any, diagnosis_name: str) -> List:
    results = []

    def search(node: Any):
        if isinstance(node, dict):
            if diagnosis_name in node and isinstance(node[diagnosis_name], dict):
                elements = node[diagnosis_name].get("elements")
                if elements:
                    results.extend(elements)
            for v in node.values():
                search(v)
        elif isinstance(node, list):
            for item in node:
                search(item)

    search(data)
    return results


def get_desc_by_key1(request):
    # Загружаем JSON из файла
    with open("diagnoses.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    elements = get_elements_by_diagnosis1(data, request)
    return elements


l = get_desc_by_key1("Инфекция мочевыводящих путей без установленной локализации")
print(l)
