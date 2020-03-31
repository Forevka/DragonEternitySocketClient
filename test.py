from db.global_map import MapDB
from db.bot_info_db import BotInfoDB
from db.items import ItemDB
from pprint import pprint, PrettyPrinter
from miniamf import decode
import json
#import networkx as nx
#import matplotlib.pyplot as plt

import math

#from bokeh.io import output_file, show
#from bokeh.models import GraphRenderer, Oval, StaticLayoutProvider, Circle,HoverTool
#from bokeh.palettes import Spectral8, Spectral4
#from bokeh.plotting import figure, ColumnDataSource



if __name__ == "__main__":
    db = BotInfoDB.get_instance()

    for i in db.db.values():
        if "грабитель дейдри" in i.get('title', '').lower():
            print(i)

    '''
    i = db.get_item(8067)
    pprint(i)
    if ('эликсир жизни' in i.get('title', '').lower()):
        print(True)
    '''

    '''pprint(db.db.get('17541'))
    
    for i in db.get_link_from(17541):
        print(i)
        print(db.id_to_coords(i[0]))
        print(db.id_to_coords(i[1]))
        print()
    '''
    '''
    G = nx.Graph()
    
    for i in db.tart_map_areas:
        G.add_node(
            i.get('title', ''), 
            pos=(
                i.get('mapPosX',0), 
                -i.get('mapPosY',0),
            )
        )
    
    pos=nx.get_node_attributes(G,'pos')
    labels=nx.draw_networkx_labels(G, pos=pos)
    '''
    '''
    tooltips = [
        ('Title', '@title'),
    ]

    source = ColumnDataSource(data=dict(
        x=[i.get('mapPosX') for i in db.tart_map_areas if i.get('mapPosX') is not None],
        y=[-i.get('mapPosY') for i in db.tart_map_areas if i.get('mapPosY') is not None],
        title=[i.get('title') for i in db.tart_map_areas if i.get('mapPosY') is not None],
    ))
    '''
    '''
    graph_layout = dict(zip(node_indices, zip(x, y)))
    graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
    '''
    '''
    p = figure(plot_width=500, plot_height=500, tooltips=tooltips,
            title="Mouse over the dots")

    p.circle('x', 'y', size=15, source=source)

    output_file('graph.html')
    show(p)
    '''
