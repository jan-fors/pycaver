# PyCaver
Python wrapper for the protein channel calculation software caver[^1].

## Overview
A wrapper for the protein channel calculation software caver that allows to integrate it into other python workflows. Additional analysis scripts which let to perform downstream tasks by viewing the protein channels as rooted tree structure.

## Installation
Install directly from GitHub via pip into conda environmetn:
```sh
# in new environment
conda create -n pycaver python=3.11 -y
conda activate pycaver

# install pycaver
pip install git+https://github.com/solarflip/pycaver
```
Or clone and install from source (useful for development):
```sh
git clone https://github.com/solarflip/pycaver
cd pycaver
pip install -e .
```

## Usage
```sh
pycaver [input] [options]
```
### Example
```sh
pycaver input.pdb -o out/ --probe_radius 1.0 --starting_point_coordinates 1.0 2.0 3.0
```
### Options
| Flag | Description | Default |
|---|---|---|
| `-o, --output_dir <path>` | Output dir path | `.` |
| `--shell_radius <float>` | Shell Radius | `3.0`|
| `--shell_depth <float>` | Shell Depth | `4.0` |
| `--probe_radius <float>` | Probe Radius | `0.9` |
| `--desired_radius <float>` | Desired Radius | `5.0` |
| `--max_distance <float>` | Max Distance | `3.0` |
| `--starting_point_coordinates <float> <float> <float> | Starting Point Coordinates | |

## Sources / References
[^1] @article{caver-3_0,
  author  = "Eva Chovancová and Antonín Pavelka and Petr Beneš and Ondřej Strnad and Jan Brezovský and Barbora Kozlíková and Artur Gora and Vilém Šustr and Martin Klvaňa and Petr Medek and Lada Biedermannová and Jiří Sochor and Jiří Damborský",
  title   = "CAVER 3.0: A Tool for the Analysis of Transport Pathways in Dynamic Protein Structures",
  journal = "PLoS Computational Biology",
  volume  = "8",
  pages   = "e1002708",
  year    = "2012"
}
## Citation
If you use this script in your research, please cite:
t.b.p.

## License
[MIT](LICENSE)