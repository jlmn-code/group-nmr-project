###### library imports ######
from _operator import contains
from fontTools.misc.plistlib import start_array
from _operator import sub
from nbformat.v2.nbbase import new_worksheet
from numpy import true_divide
from htmltools.tags import data
import great_tables
from plotnine.facets.facet_wrap import facet_wrap
from pathlib import Path
from _csv import writer
import pandas as pd
import numpy as np
from plotnine import *

########## search shift compounds ##########

folder_sim = Path("database/simulation")
csv_sim = list(folder_sim.glob("*.csv"))

df_list = []

for file in csv_sim:
    temp_df = pd.read_csv(file) ### load each simulated nmr file
    temp_df = temp_df[temp_df['intensity'] > 50] ### filter low intensity peaks
    temp_df['id'] = file.stem ### add an id column based on file name
    df_list.append(temp_df)  ### append to list


df_sim = pd.concat(df_list, ignore_index=True) # concatenate all dataframes into one

df_sim['company'] = df_sim['id'].str[-1]  ### extract company name from id

df_sim['batch'] = df_sim['id'].str[-3:-1]  ### extract batch number from id

df_sim.drop('intensity', inplace=True, axis=1)


df_sim

df_sim[['f1', 'f2']] = df_sim['X1'].str.extract(r'\[([\d.]+):([\d.]+)\]').astype(float)

df_sim.drop(['X1'], axis=1, inplace=True)


df_sim.sort_index(['company'], inplace=True, axis=1)

df_sim.sample(5)







################ Asignation ########################
################ data table shift ################
cholesterol_shift = pd.read_csv("database/shift/cholesterol.csv", delimiter=';')

cholesterol_shift.dropna(inplace=True) ## na

cholesterol_shift.drop('intensity', inplace=True, axis=1) ## drop intensity

# cholesterol_shift[['C13', 'H1', 'intensity']] = cholesterol_shift[['C13', 'H1', 'intensity']].astype(float)

cholesterol_shift.rename(columns={"H1":"f1","C13":"f2"}, inplace=True) ## adjust names

df = df_sim[['id', 'company', 'batch', 'f1', 'f2']] ## df with all simulation only good columns


##############  join

# Sort both by the 'x' column (required for merge_asof)
df = df.sort_values('f1')
cholesterol_shift = cholesterol_shift.sort_values('f1')

# Join on 'x' with a 'nearest' match
# We don't use 'tolerance' here because it must be a percentage
merged = pd.merge_asof(df, cholesterol_shift, on='f1', direction='nearest', suffixes=('', '_cholesterol'))

merged

merged = merged.sort_values('f2')

merged = pd.merge_asof(merged, cholesterol_shift.sort_values('f2'), on='f2', direction='nearest', suffixes=('', '_cholesterol'))

# Filter both x and y by the 0.1% threshold
mask_x = (merged['f1'] - merged['f1_cholesterol']).abs() <= (0.001 * merged['f1'].abs())
mask_y = (merged['f2'] - merged['f2_cholesterol']).abs() <= (0.001 * merged['f2'].abs())

result = merged[mask_x & mask_y]

result
