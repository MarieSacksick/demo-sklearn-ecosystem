# %% [markdown]
#
# # `Skore` - an abstraction to ease data science project

# %%
import os

os.environ["TOKENIZERS_PARALLELISM"] = "true"

# %% [markdown]
#
# Let's open a skore project in which we will be able to store artifacts from our
# experiments.

# %%
import skore

my_project = skore.Project("../data/my_project", if_exists=True)

# %%
from skrub.datasets import fetch_employee_salaries

datasets = fetch_employee_salaries()
df, y = datasets.X, datasets.y

# %%
from skrub import TableReport

table_report = TableReport(datasets.employee_salaries)
table_report

# %% [markdown]
#
# Let's model our problem.

# %%
from skrub import TableVectorizer, TextEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import make_pipeline

model = make_pipeline(
    TableVectorizer(high_cardinality=TextEncoder()),
    RandomForestRegressor(n_estimators=20, max_leaf_nodes=40),
)
model

# %% [markdown]
#
# `skore` provides a couple of tools to ease the evaluation of model:

# %%
from skore import CrossValidationReport

report = CrossValidationReport(estimator=model, X=df, y=y, cv_splitter=5, n_jobs=-1)

# %%
report.help()

# %%
import time

start = time.time()
score = report.metrics.r2()
end = time.time()
print(f"Time taken: {end - start:.2f} seconds")

# %%
score

# %%
start = time.time()
score = report.metrics.r2()
end = time.time()
print(f"Time taken: {end - start:.2f} seconds")

# %%
score

# %%
import time

start = time.time()
score = report.metrics.rmse()
end = time.time()
print(f"Time taken: {end - start:.2f} seconds")

# %%
score

# %%
report.cache_predictions(n_jobs=-1)

# %%
my_project.put("Random Forest model report", report)

# %%
report = my_project.get("Random Forest model report")
report.help()

# %%
report.metrics.report_metrics(aggregate=["mean", "std"], indicator_favorability=True)

# %%
display = report.metrics.prediction_error()
display.plot(kind="actual_vs_predicted")

# %%
report.estimator_reports_

# %%
estimator_report = report.estimator_reports_[0]
estimator_report.help()

# %%
estimator_report.metrics.prediction_error().plot(kind="actual_vs_predicted")

# %%
import numpy as np
import skrub
from sklearn.linear_model import RidgeCV

model = skrub.tabular_learner(RidgeCV(np.logspace(-3, 3, 10)))
model

# %%
report = CrossValidationReport(estimator=model, X=df, y=y, cv_splitter=5, n_jobs=-1)
my_project.put("RidgeCV model report", report)

# %%
from skore import ComparisonReport

report = ComparisonReport(
    reports={
        "Random Forest": my_project.get("Random Forest model report"),
        "RidgeCV": my_project.get("RidgeCV model report"),
    },
)

# %%
report.metrics.report_metrics(indicator_favorability=True)

# %% [markdown]
#
# ## Conclusions
#
# **Vision**
# - Develop tooling to create data science artifacts
# - Help at following good practices for the problem at hand
# - Help at the collaboration to carry on data science project
#
# **Wrap-up**
# - Provide tools to evaluate predictive models
# - Make some internal magic to reduce user friction
# - Allow for persistence of artifacts
#
# **Roadmap**
# - Cover multiple aspects of the data science life cycles: data, model, etc.
# - Help at creating artifacts dedicated to the problem at hand and the model
# - Reduce the complexity related to code
