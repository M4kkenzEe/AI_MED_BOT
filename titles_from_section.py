from typing import List, Dict

def get_titles_from_sections(sections: List[Dict]) -> List[str]:
    """
    Извлекает список значений title из переданного списка sections.
    """
    if not sections:
        return []
    return [section.get("title", "") for section in sections]


