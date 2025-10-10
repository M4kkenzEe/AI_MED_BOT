import os

from dotenv import load_dotenv
from openai import OpenAI

from extract_diagnoses import collect_diagnoses_from_file

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), )


def truncate_after_last_newline(text: str) -> str:
    last_newline_pos = text.rfind('\n')
    if last_newline_pos != -1:
        return text[:last_newline_pos]
    return text


def llm_query(context: str) -> str:
    response = client.responses.create(
        model="gpt-4.1",
        instructions=f"""
Ты медик с 20-летним стажем.
- Не используй Markdown разметку и прочие служебные символы, кроме знаков препинания.
- Упрости и сократи текст, раскрывая аббревиатуры.
- Если исходный текст очень длинный, выдели ТОЛЬКО самое важное и ключевые моменты.
- Пиши кратко, по существу, без воды.
- Расскажи информацию так, будто перед тобой сидит пациент, который должен понять информацию без трудностей
- Без вступительных и заключительных фраз.
- Сразу переходи к сути.
- ЖЕСТКО ОГРАНИЧЬ ответ до 2800 символов (примерно 900 токенов).
- Если ответ получается длиннее, сократи ещё раз до нужного размера.
        """,
        input=f""" Ниже выдержка из клинической рекомендации РФ по диагнозу {context} """,
        temperature=0.8,
    )
    result = response.output_text

    # Дополнительная гарантированная обрезка до 2800 символов
    if len(result) > 2800:
        result = truncate_after_last_newline(result[:2800])

    return result


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
