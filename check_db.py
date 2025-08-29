import json
from typing import Any, Optional, List, Dict

from init_db import init_db


def pretty_print_results(results):
    ids = results.get('ids', [[]])[0]
    documents = results.get('documents', [[]])[0]
    distances = results.get('distances', [[]])[0]

    print("\nРезультаты similarity search:")
    for i, (doc_id, doc_text, dist) in enumerate(zip(ids, documents, distances), start=1):
        print(f"{i}. ID: {doc_id}")
        print(f"   Диагноз: {doc_text.strip()}")
        print(f"   Расстояние: {dist:.4f}")
        print("---")


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
            print(section.get("content"))
            return section.get("content")
    return None


# Пример использования:
def get_desc_by_key(request):
    # Загружаем JSON из файла
    with open("diagnoses.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    elements = get_elements_by_diagnosis(data, request)
    print(elements)
    return elements


def format_response(results):
    ids = results.get('ids', [[]])[0]
    documents = results.get('documents', [[]])[0]
    distances = results.get('distances', [[]])[0]
    response = []

    for i, (doc_id, doc_text, dist) in enumerate(zip(ids, documents, distances), start=1):
        response.append(map(doc_id, doc_text.strip()))
    return response


if __name__ == "__main__":
    collection = init_db()

    while True:
        user_input = input("\nВведите: ").strip()
        if user_input == 'q':
            break
        print(get_desc_by_key(user_input))

        # result = collection.query(
        #     query_texts=[user_input],
        #     n_results=5,  # количество похожих результатов
        #     include=["documents", "distances"]  # что вернуть в ответе
        # )
        # print("Результаты similarity search:")
        # pretty_print_results(result)
