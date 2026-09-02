import networkx as nx
from pycaver.tunnel.TunnelPoint import TunnelPoint
from typing import List

class Tunnel:
    def __init__(self, name):
        self.name = name
        self.graph = nx.Graph()
        self.root = None
        self.last = None

    def add_root(self, TunnelPoint):
        self.root = TunnelPoint
        self.graph.add_node(TunnelPoint)
        self.last = TunnelPoint

    def add_TunnelPoint(self, TunnelPoint : TunnelPoint):
        self.graph.add_node(TunnelPoint)
        self.graph.add_edge(self.last, TunnelPoint)
        self.last = TunnelPoint

    def __str__(self):
        return self.name + " Tunnel"
    
    def print_graph(self):
        print("nodes:", self.graph.nodes())
        print("edges:", self.graph.edges())

    def get_coordinates(self):
        return [node.get_coordinates() for node in self.graph.nodes()]
    
    def get_radii(self):
        return [node.radius for node in self.graph.nodes()]
    
    def get_bottleneck_value(self):
        """
        return smallest radius of the tunnel
        """
        return min([node.radius for node in self.graph.nodes()])


def build_tunnels(tunnel_profiles : dict) -> List[Tunnel]:
    """
    """
    tunnel_obj = []
    for t in tunnel_profiles.keys():
        tunnel = Tunnel(t)
        tunnel.add_root(TunnelPoint(tunnel_profiles[t]["x"][0], tunnel_profiles[t]["y"][0], tunnel_profiles[t]["z"][0], tunnel_profiles[t]["r"][0]))
        for i in range(1,len(tunnel_profiles[t]["x"])):
            tunnel.add_TunnelPoint(TunnelPoint(tunnel_profiles[t]["x"][i], tunnel_profiles[t]["y"][i], tunnel_profiles[t]["z"][i], tunnel_profiles[t]["r"][i]))
        tunnel_obj.append(tunnel)

    return tunnel_obj