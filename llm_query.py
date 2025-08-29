import os

from dotenv import load_dotenv
from openai import OpenAI


def llm_query(context: str) -> str:
    load_dotenv()
    client = OpenAI(
        # This is the default and can be omitted
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
