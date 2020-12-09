import numpy as np
import pandas as pd

from mesa.batchrunner import BatchRunnerMP
from mesa.datacollection import DataCollector

from sim.model import SugarscapeCg


# parameter lists for each parameter to be tested in batch run
model_params = {
    "initial_population": [100, 500, 1000, 2000],
    "share_knowledge": [False, True],
    "solidarity": [False, True],
    "recreate": [0, 1],
}

fixed_parameters = {}

br = BatchRunnerMP(
    model_cls=SugarscapeCg,
    nr_processes=8,
    variable_parameters=model_params,
    fixed_parameters={},
    iterations=5,
    max_steps=1000,
    model_reporters={"Data Collector": lambda m: m.datacollector},
    display_progress=True,
)

if __name__ == "__main__":
    br.run_all()
    br_df = br.get_model_vars_dataframe()
    br_step_data = pd.DataFrame()
    for i in range(len(br_df["Data Collector"])):
        if isinstance(br_df["Data Collector"][i], DataCollector):
            i_run_data = br_df["Data Collector"][i].get_model_vars_dataframe()
            br_step_data = br_step_data.append(i_run_data.tail(1), ignore_index=True)
    br_step_data.to_csv("ants.csv")
