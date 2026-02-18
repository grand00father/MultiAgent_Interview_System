import json

from langchain_core.messages import HumanMessage

def logger(state):
    logs = {
        "participant_name": state['name'],
        "participant_position": state['position'],
        "participant_grade": state['grade'],
        "participant_experience": state['experience'],
        "turns": [],
        "final_feedback": state['messages'][-1].content
    }
    id = -1
    turn = {
        "turn_id": id,
        "agent_visible_message": "",
        "user_message": "",
        "internal_thoughts": ""
    }
    for inx, message in enumerate(state['messages'][:len(state['messages'])-2]):
        
        if isinstance(message, HumanMessage):
            turn["user_message"] = message.content

        elif isinstance(state['messages'][inx+1], HumanMessage):
            if id != -1:
                logs["turns"].append(turn)
            id += 1
            if "[Interviewer]:" in message:
                turn = {
                    "turn_id": id,
                    "agent_visible_message": message.content[len("[Interviewer]: "):],
                    "user_message": "",
                    "internal_thoughts": ""
                    }
            else:
                turn = {
                    "turn_id": id,
                    "agent_visible_message": message.content,
                    "user_message": "",
                    "internal_thoughts": ""
                    }
            
        else:
            turn["internal_thoughts"] += message.content + "\n"
    
    with open("system/logs/interview_log.json", "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=4)
