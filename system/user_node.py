from system.graph.states_graph import Interview_states
from langchain_core.messages import HumanMessage

def user_dial(state: Interview_states):
  message = state['messages'][-1].content

  if "[Interviewer]:" in message:
    print(state['messages'][-1].content[len("[Interviewer]: "):])
  else: 
    print(state['messages'][-1].content)
    
  ans_user = input('>>> ')
  return {
    'messages': [HumanMessage(content=ans_user)]
  }