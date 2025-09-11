from typing import List, Dict


def get_titles_from_sections(sections: List[Dict]) -> List[str]:
    """
    Извлекает список значений title из переданного списка sections.
    """
    result = []
    if not sections:
        return []
    for section in sections:
        if section.get("content") != "":
            result.append(section["title"])
    return result
