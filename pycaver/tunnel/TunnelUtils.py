import pycaver.tunnel.Tunnel as Tunnel
import pycaver.tunnel.TunnelPoint as TunnelPoint
import pycaver.tunnel.MetaTunnel as MetaTunnel
import networkx as nx

class TunnelUtils:
    def merge(tunnel : Tunnel, meta_tunnel : Tunnel) -> MetaTunnel:
        res = MetaTunnel.MetaTunnel()
        # TODO
        tunnel_nodes = tunnel.graph.nodes()
        tunnel_nodes = list(tunnel_nodes)
        tunnel_edges = tunnel.graph.edges()
        tunnel_edges = list(tunnel_edges)
        
        meta_nodes = meta_tunnel.graph.nodes()
        meta_nodes = list(meta_nodes)
        meta_edges = meta_tunnel.graph.edges()
        meta_edges = list(meta_edges)
         
        res_nodes = tunnel_nodes + meta_nodes
        res_nodes = list(set(res_nodes))
        res_edges = tunnel_edges + meta_edges
        res_edges = list(set(res_edges))

        res.graph.add_nodes_from(res_nodes)
        res.graph.add_edges_from(res_edges)
        res.root = meta_tunnel.root

        return res
        
    