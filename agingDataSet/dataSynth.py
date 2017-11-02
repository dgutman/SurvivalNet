# -*- coding: utf-8 -*-

import random
import numpy as np
import pandas as pd
import pprint  # This is for printing keys of dict
from collections import OrderedDict
from sklearn.utils import shuffle


patientCohortSize = 1000
randVars = 49

age = []
survival = []
censored = []
# AGE are in years : 50 - 70; 70 - 80; 80 -
# survival time is in months : 0 - 120 (10 years)

np.random.seed(66)    # numpy format is preferred for random matrix generation.
features = np.random.uniform(low=0.0, high=3, size=(patientCohortSize, randVars))
# high=3; because for std normal distribution, max width 3
# print features

# ----------------------------------------------------------------
# --------------------- Censored == Flase ------------------------
# ----------------------------------------------------------------
random.seed(66)
for pt in range(patientCohortSize / 2):

    censored.append(0)

    pt_age = random.randint(50, 100)
    age.append(pt_age)

    if pt_age > 80:
        # pt_survival = pt_age + random.randint(1, 2)
        pt_survival = random.randint(0, 24)
        survival.append(pt_survival)
    # ------------------------------------------------
    elif pt_age <= 80 & pt_age >= 70:
        # pt_survival = pt_age + random.randint(0, 3)
        pt_survival = random.randint(0, 36)
        survival.append(pt_survival)
    # ------------------------------------------------
    else:
        # pt_survival = pt_age + random.randint(0, 10)
        pt_survival = random.randint(0, 120)
        survival.append(pt_survival)

# ----------------------------------------------------------------
# --------------------- Censored == True -------------------------
# ----------------------------------------------------------------
random.seed(67)
for pt in range(patientCohortSize / 2):

    censored.append(1)

    pt_age = random.randint(50, 100)
    age.append(pt_age)

    if pt_age > 80:
        # pt_survival = pt_age + random.randint(1, 2)
        pt_follow_up = random.randint(0, 24)
        survival.append(pt_follow_up)
    # ------------------------------------------------
    elif pt_age <= 80 & pt_age >= 70:
        # pt_survival = pt_age + random.randint(0, 3)
        pt_follow_up = random.randint(0, 36)
        survival.append(pt_follow_up)
    # ------------------------------------------------
    else:
        # pt_survival = pt_age + random.randint(0, 10)
        pt_follow_up = random.randint(0, 120)
        survival.append(pt_follow_up)

# ----------------------------------------------------------------
# ----------------------------------------------------------------

features_matrix = np.asarray(features, np.float32)
age_col = np.asarray(age, np.int32)
survival_col = np.asarray(survival, np.int32)
censored_col = np.asarray(censored, np.int32)
# print(features_matrix)
# print(age_col)
# print(survival_col)
# print(censored_col)


# ==============================================================================
patientID = ['patientID_' + str(i + 1) for i in range(1000)]
feature_headers = ['feature_' + str(i + 1) for i in range(49)]

df = pd.DataFrame({"Patient ID": patientID, "Survival Time": survival_col,
                   "Censored Status": censored_col, "Age(Feature_0)": age_col},
                  columns=["Patient ID", "Survival Time", "Censored Status",
                           "Age(Feature_0)"])

headed_features = zip(feature_headers, np.transpose(features_matrix))
# Dictionary in Python returns an disordered key, value paris
headed_features_dict = OrderedDict(headed_features)

for key, value in headed_features_dict.iteritems():
    df[key] = value

# Set index as Sample ID, because pandas will add default index of numbers
df.set_index('Patient ID', inplace=True)

df = shuffle(df)
df.to_csv('survivalData.csv', index=True)
