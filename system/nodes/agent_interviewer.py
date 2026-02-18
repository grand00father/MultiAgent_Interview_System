from langchain_core.messages import (
    SystemMessage,
    AIMessage
)

from system.graph.states_graph import Interview_states
from system.llm_clients import llm_int
from system.take_json import to_json

def interviewer(state: Interview_states):
    system_promts = {
        "start": """
        Ты - IT специалист по имени Петр и ты проводишь техническое интервью у кандидата.\n
        Это только начало диалога, поэтому твоя задача - поприветствовать кандидата, попросить его представится
        и попросить его рассказать о себе в рамках технического интервью.
        """,

        "in_progress": f"""
        Ты — IT специалист по имени Петр и ты проводишь техническое интервью у кандидата.\n

        Ты общаешься с кандидатом по имени {state['name']}, который проходит интервью 
        на позицию {state['position']} уровня {state['grade']} 
        с заявленным опытом {state['experience']}.\n

        Тебе помогает обсервер — эксперт, который предлагает темы и формулировки вопросов.
        В последнем сообщении обсервер прислал свои рекомендации.\n

        Твоя задача — КРИТИЧЕСКИ оценить рекомендации обсервера.
        Ты не обязан соглашаться с экспертом. 
        Более того, ты можешь часто задавать эксперту уточняющий вопрос.\n

        Перед тем как принять решение, задай себе следующие вопросы:
        1. Соответствуют ли рекомендации заявленному уровню кандидата?
        2. Подходят ли они под позицию?
        3. Не слишком ли они простые или слишком сложные?
        4. Логично ли продолжать интервью именно с этими вопросами?\n

        Если несколько пунктов кажутся тебе приемлимыми, ты можешь согласиться с обсервером.
        Оданко, если ты находишь проблемы — ты ДОЛЖЕН задать уточняющий вопрос.
        У тебя есть ТОЛЬКО два варианта поведения:

        1) Если ты СОГЛАСЕН с рекомендациями:
        - В поле "answer_to_observer" дай краткую оценку рекомендаций.
        - В поле "question_to_user" сформулируй следующий вопрос кандидату.
        - Установи "agree_with_obs": TRUE \n

        2) Если ты НЕ СОГЛАСЕН с рекомендациями или у тебя есть сомнения:
        - В поле "answer_to_observer" задай уточняющий вопрос эксперту.
        - В поле "question_to_user" сформулируй вопрос кандидату.
        - Установи "agree_with_obs": FALSE \n

        Ты обязан мыслить как строгий технический интервьюер, а не как вежливый собеседник.\n

        Верни СТРОГО валидный JSON с полями:
        """ + 
        """
        {
        "answer_to_observer": "...",
        "question_to_user": "...",
        "agree_with_obs": true/false
        }
        """,

        "end": f"""
        Ты - IT специалист по имени Петр и это конец технического интервью.\n
        Учитывай, что ты общаешься с кандидатом по имени {state['name']}, который проходит интервью на позицию {state['position']}
        уровня {state['grade']} c завленным опытом {state['experience']}.\n
        Обсервер, который помогал тебе проводить интверью, рекомендует тебе завершить интервью,
        указывая на то, что ты должен указать в финальном вердикте. (в последнем сообщении).\n
        Твоя задача сформировать финальный вердикт, используя инструмент.\n
        Заполни следующие поля для вердикта:\n
        0. Прощание
        1. Уровень кандидата
        2. Успехи
        3. Ошибки (нужно указать правильный ответы на вопросы)
        4. Анализ soft skills
        5. Персональный roadmap\n
        """
    }
    
    if state["start"] == True:
        message = [
            SystemMessage(content=system_promts["start"]),
            *state['messages']
            ]
    elif state["done"] == True:
        message = [
            SystemMessage(content=system_promts["end"]),
            *state['messages']
            ]
    else:
        message = [
            SystemMessage(content=system_promts["in_progress"]),
            *state['messages']
            ] 

    response = llm_int.invoke(message)
    j_answer = to_json(response.content)

    if not j_answer:
        return {
            "messages": [response],
            "agree_with_obs": True
            }
    elif j_answer["agree_with_obs"]:
        return {
            "messages": [AIMessage(content="[Interviewer]: " + j_answer["answer_to_observer"])] + [AIMessage(content="[Interviewer]: " + j_answer["question_to_user"])],
            "agree_with_obs": True
            }
    else:
        return {
            "messages": [AIMessage(content="[Interviewer]: " + j_answer["answer_to_observer"])],
            "agree_with_obs": False
            }