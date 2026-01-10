###### library imports ######
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

df_sim.to_csv('database/work/compact.csv', index=False)


sim_1_size = Path('database/simulation/cholesterol_01A.csv').stat().st_size * 15 / (1024 ** 2)

sim_2_size = Path('database/work/compact.csv').stat().st_size / (1024 ** 2)

df_size = pd.DataFrame(data={'files':['before', 'filter'], 'size':[sim_1_size, sim_2_size]}).reset_index()

df_size.sort_values('size', inplace=True, ascending=False)

df_size

fig_size = (
ggplot(df_size, aes('files', 'size', fill = 'files')) + 
    geom_col(show_legend = False) +
    geom_text(aes(label = ('size'), y =50), 
        format_string='{:.2f}') +
        labs(title='GRAPH SIZE IN MEGAS FILES',
            subtitle='before and after reduction', 
            y ='size in megas')
)


df_sim

df_sim[['f1', 'f2']] = df_sim['X1'].str.extract(r'\[([\d.]+):([\d.]+)\]').astype(float)

df_sim.drop(['X1'], axis=1, inplace=True)


df_sim.sort_values('company', inplace=True, axis=1)

(
ggplot(df_sim, aes(y='f1', x='f2',
                color='company')) +
    geom_point() +
    facet_grid(cols='batch', rows='company') +
    scale_x_reverse() +
    scale_y_reverse() +
    theme_minimal() +
    labs(title='GRAPH VIEW OF ALL DATASET HSQC',
        subtitle='order by company & batch')
)



######## table summary ##########

from great_tables import *

(
    great_tables.GT(df_sim, rowname_col='id', groupname_col='company')
        .summary_rows(
            columns=['C13_jitter', 'H1_jitter', 'intensity'],
            fns=['mean', 'std', 'min', 'max'],
            groupname='Summary'
        )

)
