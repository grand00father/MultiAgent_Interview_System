from typing import TypedDict, Optional, Annotated, Sequence
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class Interview_states(TypedDict):
  name: Optional[str]
  position: Optional[str]
  grade: Optional[str]
  experience: Optional[str]
  messages:Annotated[Sequence[BaseMessage], add_messages]
  done: bool
  start: bool
  agree_with_obs: bool
