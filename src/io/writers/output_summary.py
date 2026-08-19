from src.tunnel.MetaTunnel import MetaTunnel
from pathlib import Path
import os
import json
from src.io.writers.CustomEncoder import CustomEncoder

def write_outputs(output_dir : Path, meta_tunnel : MetaTunnel, tunnel_characteristics : dict, residue_data : dict):
    """"""
    # save metatunnel
    meta_tunnel_dir = output_dir / Path("meta-tunnel")
    os.makedirs(meta_tunnel_dir, exist_ok=True)

    iplot_path = meta_tunnel_dir / Path("tunnel.html")
    meta_tunnel.iplot(iplot_path)

    graph_json = meta_tunnel_dir / Path("graph.json")
    meta_tunnel.write_graph_to_json(graph_json)

    # write summary
    meta_tunnel_meta_data = meta_tunnel.get_meta_data()

    summary_data = {}
    summary_data.update(meta_tunnel_meta_data)
    summary_data.update(tunnel_characteristics)
    summary_data.update(residue_data)

    for k in summary_data.keys():
        print(k,":::", summary_data[k])

    summary_path = meta_tunnel_dir / Path("summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary_data, f, indent=4, cls=CustomEncoder)
          