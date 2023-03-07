These simulation experimets were done as part of the article [Tools for Emancipatory Societies](https://transform-social.org/texte/tools/).

# Simulation Experiments

This simulation is using [mesa](https://mesa.readthedocs.io/en/stable/).

The experiment is based on the [sugarscape example](https://ccl.northwestern.edu/netlogo/models/Sugarscape3WealthDistribution).

## General Idea of the Simulation

In a given territory, ants walk around collecting sugar.
In some areas there is more sugar to collect than in others.
Sugar needs to regrow. Some ants need more sugar than others.
The ants also have varied senses and can only walk up to x fields per simulation step depending on their vision.

In the basic version of the example, the ants just check the area within their vision to decide on their next move.

I added various other modes like internet, solidarity, and individualists to study the impact on the ants.

No real ants were hurt during the experiments.


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

See the included [Jupyter notebook](https://github.com/rakvat/ant_sim/blob/master/analysis.ipynb).

## Videos

Basic mode:

[![Example simulation run with basic mode](https://img.youtube.com/vi/HLzrQH-4Qxw/0.jpg)](https://youtu.be/HLzrQH-4Qxw)

Internet mode:

[![Example simulation run with internet mode](https://img.youtube.com/vi/_oGLnQ8XX7A/0.jpg)](https://youtu.be/_oGLnQ8XX7A)

Solidarity mode:

[![Example simulation run with solidarity mode](https://img.youtube.com/vi/zFG0JZGG-HA/0.jpg)](https://youtu.be/zFG0JZGG-HA)

10% Individualists:

[![Example simulation run with 10% individualists](https://img.youtube.com/vi/Z_o_bR9Fjt4/0.jpg)](https://youtu.be/Z_o_bR9Fjt4)
