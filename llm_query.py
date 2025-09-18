import os

from dotenv import load_dotenv
from openai import OpenAI

from extract_diagnoses import collect_diagnoses_from_file

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), )


def llm_query(context: str) -> str:
    response = client.responses.create(
        model="gpt-4.1",
        instructions=f"""
Ты медик с 20-летним стажем.
 - Распиши выдержку более понятно, раскрывая аббревиатуры и делая текст доступнее.
- Сократи текст, сохраняя смысл.
- Ограничь длину ответа 4000 символами.
- Не пиши вступительных фраз, сразу переходи к сути.
Если ответ получается длиннее 4000 символов, сократи его до этого лимита.
Отвечай только содержательным текстом.
        """,
        input=f""" Ниже выдержка из клинической рекомендации РФ по диагнозу {context} """,
        max_output_tokens=1000
    )
    return response.output_text


def llm_query_choose_diagnosis(context: str) -> list[str]:
    diagnosis_list = collect_diagnoses_from_file()
    response = client.responses.create(
        model="gpt-4o",
        instructions=f"""Ты опытный медик с 20-летним стажем."""
        ,
        input=f""" У тебя есть список диагнозов, описанных научным языком: {diagnosis_list}.

Врач сообщил диагноз: {context}.

Твоя задача — проанализировать диагноз врача и выбрать только те диагнозы из списка, которые максимально совпадают или похожи на введённый.

Если нет ни одного совпадения — выведи пустую строку (не выдавай никаких слов или сообщений).

Выведи найденные диагнозы в порядке убывания сходства, разделяя их только запятыми без пробелов и без точек в конце. Не добавляй никаких пояснений, вступительных фраз или комментариев.

Пример:
Если врач ввёл "бронхит", а в списке есть "Бронхит у детей", "бронхит", "бронхит у взрослых",
нужно вывести: "бронхит,бронхит у детей,бронхит у взрослых"

Не придумывай новые диагнозы и не добавляй ничего вне списка.
        """,
        temperature=0.1,
    )
    return response.output_text.split(",")


async def llm_query2(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-4.1",
        instructions=f"""Веди себя как профессиональный педиатр с опытом работы 20 лет""",
        input=prompt,
    )
    return response.output_text


async def llm_query1(context: str, context_string) -> str:
    response = client.responses.create(
        model="gpt-4.1",
        instructions=f"""Веди себя как профессиональный педиатр с опытом работы 20 лет""",
        input=f""" 
        вот документ с медицинским отчетом о пациенте {context_string}.
        Задание: {context}
        """,
    )
    return response.output_text
