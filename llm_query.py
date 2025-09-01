import os

from dotenv import load_dotenv
from openai import OpenAI

from extract_diagnoses import collect_diagnoses_from_file


def llm_query(context: str) -> str:
    load_dotenv()
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.responses.create(
        model="gpt-4o",
        instructions=f"""Ты медик с 20-летним стажем.
        """
        ,
        input=f""" Ниже выдержка из клинической рекомендации РФ по диагнозу {context}
        Распиши выдержку более понятно (раскрой абревиатуры, сделай более понятный язык)
        Не используй вступительные фразы а сразу начинай писать по делу;
        Сократи текст без потери смысла;
        """,
    )
    return response.output_text


def llm_query_choose_diagnosis(context: str) -> list[str]:
    load_dotenv()
    diagnosis_list = collect_diagnoses_from_file()
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.responses.create(
        model="gpt-4o",
        instructions=f"""Ты медик с 20-летним стажем.
        """
        ,
        input=f""" У тебя есть список диагнозов описанных научным языком: {diagnosis_list};
        Врач который осматривал пациента сказал тебе этот диагноз: {context};
        твоя задача проанализировать диагноз, что тебе написал врач и вывести все похожие и совпадающие из данного тебе списка диагнозы,
        с целью локализовать диагноз.
        
        Не выводи ничего нового или несуществующего, выводи только те диагнозы через запятую, которые должны уточнить диагноз или совпасть, например:
        Врач ввел бронхит, твоя задача попытаться понять, что это за диагноз и вывести похожие из списка - Бронхит у детей, бронхит, бронхит у взрослых
        Не ставь в конце точку
        """,
    )
    return response.output_text.split(", ")
