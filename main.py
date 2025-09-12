import uvicorn
from fastapi import FastAPI, Query, UploadFile, File
from fastapi.responses import JSONResponse

from check_db import get_desc_by_key, get_diagnose_detail
from extract_diagnoses import collect_diagnoses_from_file
from llm_query import llm_query_choose_diagnosis, llm_query
from tasks11_15 import *
from tasks5_10 import tasks5_10
from titles_from_section import get_titles_from_sections

app = FastAPI()
DIAGNOSES_DB = collect_diagnoses_from_file("diagnoses.json")


@app.get("/diagnoses/similar")
async def get_similar_diagnoses(diagnosis: str = Query(..., description="Название диагноза для поиска похожих")):
    result = llm_query_choose_diagnosis(diagnosis)
    return {"diagnoses": result}


@app.get("/diagnoses/{diagnosis:path}/sections")
async def get_sections(diagnosis: str):
    section_list = get_desc_by_key(diagnosis.strip())
    result = get_titles_from_sections(section_list)
    return {"sections": result}


@app.get("/diagnoses/{diagnosis:path}/sections/{sectionName:path}")
async def get_section_content(diagnosis: str, sectionName: str):
    sections = get_desc_by_key(diagnosis)
    content = get_diagnose_detail(sections, sectionName)
    result = llm_query(content)
    return {"content": result}


@app.post("/check-protokol")
async def check_protokol(file: UploadFile = File(...)):
    content = await file.read()
    protocol = content.decode("utf-8")

    l1 = await tasks5_10(protocol)  # Ваш вызов для получения начальных данных
    l = get_desc_by_key(l1["мкб"])
    clinic_picture = get_diagnose_detail(l, "Клиническая картина")
    clinic_diagnostic = get_diagnose_detail(l, "Диагностика")
    quality_criteria = get_diagnose_detail(l, "Критерии оценки качества")
    zhalobi = l1["жалобы"]
    osmotr = l1["осмотр"]
    diagnostic = l1["диагностика"]
    healing = l1["лечение"]

    response = {
        "icd": l1["мкб"],
        "complaints": zhalobi,  # жалобы
        "examination_results": osmotr,  # результаты осмотра
        "diagnostic_recommendations": diagnostic,  # диагностика
        "treatment": healing,  # лечение
        "comparison_complaints": await task11(clinic_picture, zhalobi, osmotr),  # сравнение протоколов
        "comparison_examination_results": await task12(diagnostic, clinic_diagnostic),  # сравнение рез-тов диагностики
        "comparison_diagnostic_recommendations": await task13(clinic_diagnostic, healing),  # сравнения Рез-таты Лечение
        "quality_control": await task14(quality_criteria, protocol),  # контроль качества лечения
        "suggestion_complaints": await task15(protocol),  # предложения и рекомендации
    }

    return JSONResponse(content=response)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
