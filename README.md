# cadcad-explorations

Explorations into cadCAD

## Prerequisites

Have installed

- Jupyter Notebook (or Jupyter Labs)
- A virtual environment
  - [virtual fish]()
  - Or use the one you know best

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
