from system.graph.graph_structure import graph_app
from system.graph.visualization_graph import visualization
from system.logger import logger

state = {
    'name':None,
    'position': None,
    'grade': None,
    'experience': None,
    'messages': [],
    'done': False,
    'start': True,
    'agree_with_obs': True
    
}

if __name__ == "__main__":
    state = graph_app.invoke(state)
    logger(state)

    #Получить схему графа:
    #visualization()

