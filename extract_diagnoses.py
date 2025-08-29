import json
from typing import List, Any, Set


def collect_diagnoses_from_file(path: str = "diagnoses.json") -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return collect_diagnoses(data)

def collect_diagnoses(node: Any) -> List[str]:
    diagnoses: List[str] = []
    seen: Set[str] = set()

    def is_diagnosis_obj(v: Any) -> bool:
        return (
            isinstance(v, dict) and
            "url" in v and
            "elements" in v and
            isinstance(v.get("url"), str) and
            isinstance(v.get("elements"), list)
        )

    def walk(x: Any):
        if isinstance(x, dict):
            for k, v in x.items():
                # если узел выглядит как диагноз — забираем его ключ (название)
                if isinstance(k, str) and is_diagnosis_obj(v) and k not in seen:
                    seen.add(k)
                    diagnoses.append(k)
                # продолжаем обход
                walk(v)
        elif isinstance(x, list):
            for item in x:
                walk(item)

    walk(node)
    return diagnoses

if __name__ == "__main__":
    result = collect_diagnoses_from_file("diagnoses.json")
    print(result)


