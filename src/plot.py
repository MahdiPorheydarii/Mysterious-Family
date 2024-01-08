import networkx as nx
import plotly.graph_objects as go

def plot_family_tree(person, graph=None, pos=None, level=0, width=1., vert_gap=0.4, xcenter=0.5, visited=None):
    if visited is None:
        visited = set()

    if person in visited:
        return pos

    if pos is None:
        pos = {person: (xcenter, 1 - level * vert_gap)}
    else:
        pos[person] = (xcenter, 1 - level * vert_gap)

    visited.add(person)
    neighbors = person.children

    tmp = []

    for i in neighbors:
        tmp += i.parents
    neighbors += tmp


    if len(neighbors) != 0:
        dx = width / 2
        nextx = xcenter - width/2 - dx/2
        for neighbor in neighbors:
            nextx += dx
            pos = plot_family_tree(neighbor, graph=graph, pos=pos,
                                   level=level+1, width=dx, xcenter=nextx, visited=visited)
            if person != neighbor:
                graph.add_edge(person, neighbor)

    return pos

def graph_to_plotly(graph, pos):
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        edge_x += [pos[edge[0]][0], pos[edge[1]][0], None]
        edge_y += [pos[edge[0]][1], pos[edge[1]][1], None]

    node_x, node_y, node_text = zip(*[(pos[node][0], pos[node][1], node.name) for node in graph.nodes()])

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#777'), hoverinfo='none', mode='lines')

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers',
        hoverinfo='text',
        text=node_text,
    )

    annotations = [dict(x=x, y=y, xref='x', yref='y', text=text, showarrow=True, arrowhead=4, ax=0, ay=-20) for x, y, text in zip(node_x, node_y, node_text)]

    fig = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(showlegend=False, hovermode='closest', margin=dict(b=0, l=0, r=0, t=0), xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False), annotations=annotations))
    
    return fig
