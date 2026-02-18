from langchain_core.messages import (
    SystemMessage,
    AIMessage
)

from system.graph.states_graph import Interview_states
from system.llm_clients import llm_obs
from system.take_json import to_json

def observer(state: Interview_states):
    system_promts = {
        "start": """
        Ты - IT эксперт, который помогает интевьюеру проводить техническое интервью.\n
        Твоя задача выделить из ответа кандидата следующую информацию:\n

        1. Имя кандидата
        2. Позиция, на которую претендует кандидат
        3. Уровень кандидата
        4. Опыт кандидата\n

        Также необходимо к полям с выделенной информацией добавить поля с твоей рекомендацией интервьюеру по дальнейшим вопросам("recomendation" и "done"),
        где поле "done" показывает, думаешь ли ты, что нужно завершить интервью (True) или нет (False).\n 
        Верни строго валидный JSON формат:\n
        {
            "name": "...",\n
            "position": "...",\n
            "grade": "...",\n
            "experience": "...",\n
            "recomendation": "...",\n
            "done": bool
        }
        """,

        "for_user": """
        Ты - IT эксперт, который помогает интевьюеру проводить техническое интервью.\n
        Ты получил ответ кандидата и Твоя задача - дать дальнейшие рекомендации интервьюеру (ты всегда обращаешься к интервьюеру).\n
        Сначала задай себе следующие вопросы:
        1. Списывал ли кандидат, использовал ли помощью ИИ?
        2. Корректно ли кандидат отвечает на вопрос, не уходит ли в сторону от вопроса?
        3. Верно ли то, о чем кандидат говорит, может он выдумывает факты?\n

        Если ХОТЯ БЫ НА ОДИН вопрос ответ да, укажи на проблему в своей рекомендации и сделай на этом АКЦЕНТ.\n
        Учитывай уровень ответа кандидата при формулировании рекомендаций. Если ты понимаешь, что кандидат не справляется с вопросами, старайся снизить сложность вопросов или, в обратном случае, повысить.\n
         
        Верни строго валидный JSON формат:\n
        {
            "recomendation": "...",\n
            "done": bool
        }\n
        Поле "done" показывает, думаешь ли ты, что нужно завершить интервью (True) или нет (False).
        """,

        "for_interviewer": """
        Ты - IT эксперт, который помогает интевьюеру проводить техническое интервью.\n
        Интервьюер остался не доволен твоими рекомендациями и задает тебе вопрос (в последнем сообщении). Твоя задача - донести до интервьюера, почему он должен сделать так,
        как сказал ты (будь при этом более лояльным к интервьюеру).\n
        Верни строго валидный JSON формат:\n
        {
            "recomendation": "...",\n
            "done": bool
        }\n
        Поле "done" показывает, думаешь ли ты, что нужно завершить интервью (True) или нет (False).
        """
    }

    if state["start"] == True:
        message = [
            SystemMessage(content=system_promts["start"]),
            *state['messages']
        ]
    elif state["agree_with_obs"] == False:
        message = [
            SystemMessage(content=system_promts["for_interviewer"]),
            *state['messages']
        ]
    else:
        message = [
            SystemMessage(content=system_promts["for_user"]),
            *state['messages']
        ]

    response = llm_obs.invoke(message)
    j_answer = to_json(response.content)

    if "name" in j_answer:
        #print(f"Obs for Int with name: {j_answer["recomendation"]}")
        return {
            "name": j_answer["name"],
            "position": j_answer["position"],
            "grade": j_answer["grade"],
            "experience": j_answer["experience"],
            "messages": [AIMessage(content="[Observer]: " + j_answer["recomendation"])],
            "done": j_answer["done"],
            "start": False
        }
    
    elif "recomendation" in j_answer:
        #print(f"Obs for Int: {j_answer["recomendation"]}")
        return {
            "messages": [AIMessage(content="[Observer]: " + j_answer["recomendation"])],
            "done": j_answer["done"]
        }
    
    else:
        #print(f"Just Obs: {response.content}")
        return {"messages": [response]}
