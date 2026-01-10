###### library imports ######
from pathlib import Path
from _csv import writer
import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_point, theme_minimal, scale_x_reverse, scale_y_reverse


################ data loading and cleaning ################
cholesterol_shift = pd.read_csv("database/shift/cholesterol_propyl.csv", delimiter=';')

cholesterol_shift.dropna(inplace=True)

# cholesterol_shift[['C13', 'H1', 'intensity']] = cholesterol_shift[['C13', 'H1', 'intensity']].astype(float)

cholesterol_shift.fillna(0, inplace=True)

cholesterol_shift

rng = np.random.default_rng(seed=5234)

cholesterol_shift['C13_jitter'] = cholesterol_shift.apply(lambda row: rng.normal(loc=row['C13'],
                    scale=row['C13']*.05,
                    size=int(row['intensity']*.01)), axis=1)

cholesterol_shift['H1_jitter'] = cholesterol_shift.apply(lambda row: rng.normal(loc=row['H1'],
                    scale=row['H1']*.05,
                    size=int(row['intensity']*.01)), axis=1)


cholesterol_nmr = cholesterol_shift.explode(['C13_jitter', 'H1_jitter'])

cholesterol_nmr['C13_jitter'] = cholesterol_nmr['C13_jitter'].astype(float)
cholesterol_nmr['H1_jitter'] = cholesterol_nmr['H1_jitter'].astype(float)



##################noise addition ##################

noise = pd.DataFrame({
    'C13_jitter': np.random.uniform(low=0, high=200, size=100000),
    'H1_jitter': np.random.uniform(low=0, high=12, size=100000),
    'intensity': np.random.uniform(low=-25, high=25, size=100000)
})


cholesterol_simulation = pd.concat([cholesterol_nmr, noise], ignore_index=True)

cholesterol_simulation['X1'] = '[' + cholesterol_simulation['H1_jitter'].astype(str) + ':' + cholesterol_simulation['C13_jitter'].astype(str) + ']'

cholesterol_simulation['X2'] = cholesterol_simulation['intensity']

cholesterol_simulation.drop(['C13', 'H1', 'C13_jitter', 'H1_jitter'], axis=1, inplace=True)


################## export data ##################

cholesterol_simulation.to_csv('database/simulation/cholesterol_05C.csv', index=False)

