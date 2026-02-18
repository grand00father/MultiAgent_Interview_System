from system.graph.states_graph import Interview_states
from langchain_core.messages import AIMessage

def for_user(state: Interview_states):
    last_message =state["messages"][-1]

    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "tools"
    elif state["agree_with_obs"]:
        return "user"
    
    return "observer"
