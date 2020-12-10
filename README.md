# Simulation Experiments

This simulation is using [mesa](https://mesa.readthedocs.io/en/stable/).

The experiment is based on the [sugarscape example](https://github.com/projectmesa/mesa/tree/master/examples/sugarscape_cg).

## General Idea of the Simulation

In a given territory, ants walk around collecting sugar.
In some areas there is more sugar to collect than in others.
Sugar needs to regrow. Ants have varied vision and can only walk up to x fields per simulation step depending on their vision.

In the basic version of the example, the ants just check the area within their vision to decide on their next move.

In the knowledge version the ants collectively build a shared knowledge map of the territory storing recent sugar availability. Sharing knowledge leads to a better chance of surviving.

## How to Run

Install requirements:

`pip install -r requirements.txt`

Run the interactive simulation:

`mesa runserver`

Run the batch processing which produces `ants.csv` (this will run for some hours):

`python batch.py`

Run the Jupyter notebook that analyzes `ants.csv`:

`jupyter notebook`


## Data-Analysis and Findings

See the included [Jupyter notebook](https://github.com/rakvat/ant_sim/blob/master/Ants%20with%20Knowledge%20and%20Solidarity.ipynb).

## Videos

Basic mode:

[![Example simulation run with basic mode](https://img.youtube.com/vi/DuyHtU5Atd0/0.jpg)](https://youtu.be/DuyHtU5Atd0)

Knowledge mode:

[![Example simulation run with knowledge mode](https://img.youtube.com/vi/oh7xUkg7cEE/0.jpg)](https://youtu.be/oh7xUkg7cEE)
