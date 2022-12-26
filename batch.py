import pandas as pd

from mesa.batchrunner import batch_run

from sim.model import SugarscapeCg


# parameter lists for each parameter to be tested in batch run
model_params = {
    "initial_population": [100, 500],
    "recreate": [0, 10],
    "shared_knowledge": [False, True],
    "solidarity": [False, True],
    "individualist_percent": [0, 1, 10, 50, 90],
}

fixed_parameters = {}


if __name__ == "__main__":
    results = batch_run(
        model_cls=SugarscapeCg,
        parameters=model_params,
        iterations=5,   # per parameter operation
        max_steps=1000,
        number_processes=None,  # use all awailable processors
        display_progress=True,
    )

    results_df = pd.DataFrame(results)
    results_df.to_csv("ants.csv")
