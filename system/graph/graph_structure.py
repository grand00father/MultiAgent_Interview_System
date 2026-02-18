from langgraph.graph import StateGraph
from system.graph.states_graph import Interview_states
from langgraph.prebuilt import ToolNode

from system.nodes.agent_interviewer import interviewer
from system.nodes.agent_observer import observer
from system.nodes.user_node import user_dial
from system.tools import tools
from system.conditional_edges import for_user

graph = StateGraph(Interview_states)

graph.add_node('interviewer', interviewer)
tool_node = ToolNode(tools=tools)
graph.add_node('tools', tool_node)
graph.add_node('observer', observer)
graph.add_node('user', user_dial)

graph.set_entry_point('interviewer')

graph.add_conditional_edges(
    "interviewer",
    for_user,
    {
        "tools": "tools",
        "user": "user",
        "observer": "observer"
    }
)

graph.add_edge("user", "observer")
graph.add_edge("observer", "interviewer")

graph_app = graph.compile()
