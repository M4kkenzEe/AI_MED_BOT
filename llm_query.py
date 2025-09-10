import os

from dotenv import load_dotenv
from openai import OpenAI

from extract_diagnoses import collect_diagnoses_from_file

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), )


def llm_query(context: str) -> str:
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
    diagnosis_list = collect_diagnoses_from_file()
    response = client.responses.create(
        model="gpt-4o",
        instructions=f"""Ты медик с 20-летним стажем.
        """
        ,
        input=f""" У тебя есть список диагнозов, описанных научным языком: {diagnosis_list}.

Врач сообщил диагноз: {context}.

Твоя задача — проанализировать диагноз врача и выбрать из списка только те диагнозы, которые максимально совпадают или похожи на введённый.

Выведи найденные диагнозы в порядке убывания сходства (от наиболее подходящих к менее подходящим), через запятую, без повторов.

Не придумывай новые диагнозы, не добавляй ничего вне списка.

Если похожих диагнозов нет — верни пустую строку.

Пример:
Если врач ввёл "бронхит", а в списке есть "Бронхит у детей", "бронхит", "бронхит у взрослых",
нужно вывести: "бронхит, бронхит у детей, бронхит у взрослых"

Не ставь точку в конце, разделяй диагнозы только запятыми.
        """,
    )
    return response.output_text.split(", ")


async def llm_query2(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-4o",
        instructions=f"""Веди себя как профессиональный педиатр с опытом работы 20 лет""",
        input=prompt,
    )
    return response.output_text


async def llm_query1(context: str, context_string) -> str:
    response = client.responses.create(
        model="gpt-4o",
        instructions=f"""Веди себя как профессиональный педиатр с опытом работы 20 лет""",
        input=f""" 
        вот документ с медицинским отчетом о пациенте {context_string}.
        Задание: {context}
        """,
    )
    return response.output_text
