from check_db import get_desc_by_key, get_diagnose_detail

diagnose = "Острый бронхит"
section = "Этиология и патогенез"

ls = get_desc_by_key(diagnose)

from typing import List, Dict

def get_titles_from_sections(sections: List[Dict]) -> List[str]:
    """
    Извлекает список значений title из переданного списка sections.
    """
    if not sections:
        return []
    return [section.get("title", "") for section in sections]


print(get_titles_from_sections(ls))


# print(get_diagnose_detail(ls, section))