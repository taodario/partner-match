import pandas as pd
import networkx as nx
import itertools
import graphviz

# List of all timeslots (same as header order in CSV)
TIMES = [
    'Friday afternoon', 'Friday evening', 'Friday morning',
    'Monday afternoon', 'Monday evening', 'Monday morning',
    'Saturday afternoon', 'Saturday evening', 'Saturday morning',
    'Sunday afternoon', 'Sunday evening', 'Sunday morning',
    'Thursday afternoon', 'Thursday evening', 'Thursday morning',
    'Tuesday afternoon', 'Tuesday evening', 'Tuesday morning',
    'Wednesday afternoon', 'Wednesday evening', 'Wednesday morning'
]

# Load dataset
def load_data(path="availability.csv"):
    return pd.read_csv(path, index_col="Codename")

# Build weighted compatibility graph
def make_graph(data):
    graph = nx.Graph()
    edge_list = []
    for (user1, p1), (user2, p2) in itertools.combinations(data.iterrows(), 2):
        # overlap = number of shared timeslots
        overlap = sum(p1[TIMES].values & p2[TIMES].values)
        if overlap > 0:
            # bonus if both have same Virtual flag
            overlap += 10 * int(p1.Virtual == p2.Virtual)
            edge_list.append((str(user1), str(user2), overlap))
    graph.add_weighted_edges_from(edge_list)
    return graph

# Plotting helpers
def plot_graph(g):
    plot = graphviz.Graph()
    for v in g.nodes:
        plot.node(v)
    for u, v in g.edges():
        plot.edge(u, v, label=str(g.edges[(u, v)]['weight']))
    plot.render("graph", format="png", cleanup=True)
    print("Graph saved as graph.png")

def plot_graph_with_matching(g, m):
    plot = graphviz.Graph()
    for v in g.nodes:
        plot.node(v)
    for u, v in g.edges():
        if (u, v) in m or (v, u) in m:
            plot.edge(u, v, label=str(g.edges[(u, v)]['weight']), color="blue")
        else:
            plot.edge(u, v, label=str(g.edges[(u, v)]['weight']))
    plot.render("graph_matching", format="png", cleanup=True)
    print("Graph with matching saved as graph_matching.png")

# Example usage
if __name__ == "__main__":
    data = load_data()
    g = make_graph(data)
    matching = nx.max_weight_matching(g, maxcardinality=True)
    print("Optimal matching:", matching)
    plot_graph_with_matching(g, matching)
