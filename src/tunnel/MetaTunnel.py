import networkx as nx
from src.tunnel.TunnelPoint import TunnelPoint
from src.tunnel.Tunnel import Tunnel
from typing import List
import json
from src.io.parser.CustomDecoder import CustomDecoder
from src.io.writers.CustomEncoder import CustomEncoder
from src.tunnel.TunnelUtils import TunnelUtils
import matplotlib.pyplot as plt
import plotly.graph_objects as go

class MetaTunnel:
    def __init__(self):
        self.graph = nx.Graph()
        self.root = None

    def add_first(self, tunnel : Tunnel):
        self.root = tunnel.root
        self.graph = tunnel.graph 

    def set_graph(self, graph):
        self.graph = graph

    def __str__(self):
        return f"Meta Tunnel, root: {self.root}"
    

    def get_bottleneck_value(self):
        """
        return smallest radius of the tunnel
        """
        return min([node.radius for node in self.graph.nodes()])
    
    def get_largest_bottleneck(self):
        """
        calculate the leaves and then the smalles radius for each path from root to leaf
        afterwards return the largest bottleneck
        """
        leaves = [node for node, degree in self.graph.degree() if degree == 1]
        if self.root in leaves:
            leaves.remove(self.root)
        bottlenecks = []
        for leaf in leaves:
            if leaf.get_coordinates() == self.root.get_coordinates():
                print("Skipping root as leaf")
                continue
            try:
                path = nx.shortest_path(self.graph, source=self.root, target=leaf)
            except nx.NetworkXNoPath:
                print(f"No path from {self.root} to {leaf}")
                continue
            bottleneck = min([node.radius for node in path])
            bottlenecks.append(bottleneck)
        return max(bottlenecks)
    
    def get_average_bottleneck(self):
        """
        calculate the leaves and then the smalles radius for each path from root to leaf
        afterwards return the average bottleneck
        """
        leaves = [node for node, degree in self.graph.degree() if degree == 1]
        if self.root in leaves:
            leaves.remove(self.root)
        bottlenecks = []
        for leaf in leaves:
            if leaf.get_coordinates() == self.root.get_coordinates():
                print("Skipping root as leaf")
                continue
            try:
                path = nx.shortest_path(self.graph, source=self.root, target=leaf)
            except nx.NetworkXNoPath:
                print(f"No path from {self.root} to {leaf}")
                continue
            bottleneck = min([node.radius for node in path])
            bottlenecks.append(bottleneck)
        return sum(bottlenecks) / len(bottlenecks) if bottlenecks else 0

    def get_average_tunnel_radius(self):
        """
        calculate the average radius of the tunnel
        """
        if len(self.graph.nodes()) == 0:
            return 0
        return sum([node.radius for node in self.graph.nodes()]) / len(self.graph.nodes())
    
    def get_amount_of_leaves(self):
        leaves = [node for node, degree in self.graph.degree() if degree == 1]
        if self.root in leaves:
            leaves.remove(self.root)
        return len(leaves)

    def write_to_json(self, filename : str = "meta_tunnel.json"):
        data = nx.node_link_data(self.graph, edges="links")
        meta_data = {
            "min_bottleneck" : self.get_bottleneck_value(),
            "max_bottleneck" : self.get_largest_bottleneck(),
            "avg_bottleneck" : self.get_average_bottleneck(),
            "#tunnel" : self.get_amount_of_leaves(),
            "avg_tunnel_radius" : self.get_average_tunnel_radius(),
            "root" : self.root,
            "graph" : data
        }
        with open(filename, 'w') as f:
            json.dump(meta_data, f, indent=4, cls=CustomEncoder)

    def get_meta_data(self) -> dict:
        data = nx.node_link_data(self.graph, edges="links")
        meta_data = {
            "min_bottleneck" : self.get_bottleneck_value(),
            "max_bottleneck" : self.get_largest_bottleneck(),
            "avg_bottleneck" : self.get_average_bottleneck(),
            "#tunnel" : self.get_amount_of_leaves(),
            "avg_tunnel_radius" : self.get_average_tunnel_radius(),
        }
        return meta_data
    
    def get_graph(self) -> dict:
        data = nx.node_link_data(self.graph, edges="links")
        return {
            "root": self.root,
            "graph" : data
        }
    
    def write_graph_to_json(self, filename: str = "tunnel_graph.json"):
        g = self.get_graph()
        with open(filename, "w") as f:
            json.dump(g, f, indent=4, cls=CustomEncoder)
    
    def read_from_json(self, filename : str):
        with open(filename, "r") as f:
            data = json.load(f, object_hook=CustomDecoder.tunnelpoint_decoder)
        self.graph = nx.node_link_graph(data["graph"], edges="links")
        self.root = data["root"]

    def plot(self, filename : str = "meta_tunnel.png"):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # draw nodes
        for node in self.graph.nodes():
            ax.scatter(node.x, node.y, node.z, c='b', marker='o')

        # draw edges
        for edge in self.graph.edges():
            node1 = edge[0]
            node2 = edge[1]
            ax.plot([node1.x, node2.x], [node1.y, node2.y], [node1.z, node2.z], c='b')

        plt.savefig(filename)

    def iplot(self, filename : str = "network_graph.html"):
        Xn = [node.x for node in self.graph.nodes()]
        Yn = [node.y for node in self.graph.nodes()]
        Zn = [node.z for node in self.graph.nodes()]

        node_values = [(node.radius)*10 for node in self.graph.nodes]

        special_node = list(self.graph.nodes)[0]

        node_trace = go.Scatter3d(
            x=Xn, y=Yn, z=Zn,
            mode='markers',
            marker=dict(size=node_values, 
                        opacity=0.8,
                        color=['red' if node == special_node else 'blue' for node in self.graph.nodes]),
            hoverinfo='text'
        )

        fig = go.Figure(data=[node_trace])
        fig.write_html(filename)

    def get_combined_root_end(self):
        """
        get the subtunnel of near the active site, where the tunnels are one

        Iterates over the path from root to any leave and adds the point to the output. 
        If a point is reached with a degree of 3 stop
        """
        combined_tunnel = Tunnel("combined_tunnel")
        combined_tunnel.add_root(self.root)
        leaves = [node for node, degree in self.graph.degree() if degree == 1]
        
        chosen_leaf = leaves[0] if leaves else None
        if chosen_leaf is None:
            return combined_tunnel
    
        path = nx.shortest_path(self.graph, source=self.root, target=chosen_leaf)
        for node in path:
            if self.graph.degree(node) > 2:
                break
            combined_tunnel.add_TunnelPoint(TunnelPoint(node.x, node.y, node.z, node.radius))

        return combined_tunnel

def build_metatunnel(tunnel_obj : List[Tunnel]) -> MetaTunnel:
    """
    """
    m = MetaTunnel()
    
    m.add_first(tunnel_obj[0])
    for t in tunnel_obj[1:]:
        m = TunnelUtils.merge(tunnel=t, meta_tunnel=m)

    return m