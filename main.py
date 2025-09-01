from fastapi import FastAPI, Query

from check_db import get_desc_by_key, get_diagnose_detail
from extract_diagnoses import collect_diagnoses_from_file
from init_db import init_db
from llm_query import llm_query
from titles_from_section import get_titles_from_sections
import uvicorn

app = FastAPI()
DIAGNOSES_DB = collect_diagnoses_from_file("diagnoses.json")


@app.get("/diagnoses/similar")
async def get_similar_diagnoses(diagnosis: str = Query(..., description="Название диагноза для поиска похожих")):
    collection = init_db()

    result = collection.query(
        query_texts=[diagnosis],
        n_results=5,
        include=["documents", "distances"]
    )
    similar = result

    return {"diagnoses": similar["documents"][0]}


@app.get("/diagnoses/sections")
async def get_sections(diagnosis: str = Query(..., description="Название диагноза для получения разделов")):
    section_list = get_desc_by_key(diagnosis.strip())
    result = get_titles_from_sections(section_list)
    return {"sections": result}


@app.get("/diagnoses/{diagnosis}/sections/{sectionName}")
async def get_section_content(diagnosis: str, sectionName: str):
    sections = get_desc_by_key(diagnosis)
    content = get_diagnose_detail(sections, sectionName)
    result = llm_query(content)
    return {"content": result}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
