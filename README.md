# cadcad-explorations

Explorations into cadCAD

## Prerequisites

Have installed

- Python >= 3.8+
- A virtual environment
  - Currently using [VirtualFish](https://virtualfish.readthedocs.io/en/latest/install.html)
  - Uses the fish shell
- Jupyter Labs or Jupyter notebook
  - Download or use an extension inside of VScode
- `ipykernel`

## Setup

These steps assume virtual fish but should translate to any other python virtual
environment easy enough.

1. Create the virtual environment

```
vf new <env-name-you-choose>
```

The rest of the steps assume a name of `cadcad-explorations`.

2. Activate the environment

```
vf activate cadcad-explorations
```

3. Install the requirements

```
pip install -r requirements.txt
```

4. Setup a new kernel for the Jupyter notebook to source the requirements properly

```
python -m ipykernel install --user --name=cadcad-explorations
```

## Extras for those in Docker-land

Will need to have docker-ce installed

```
docker build . --no-cache -t cadcad

docker container run -p 8888:8888 cadcad
```
