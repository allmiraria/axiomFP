from pathlib import Path
import pandas, typer
import tqdm.auto
import matplotlib.pyplot as plt


# input
path_to_snp_statistics = 'input/SNP_statistics_file.txt'
path_to_snp_call_contrast_positions = 'input/SNP_call_contrast_positions_file.txt'
chunksize = 10000
output_directory = 'histograms'
columns_to_remove = ['n_NC', 'AA.meanX', 'AA.varX', 'AB.meanX', 'BB.meanX', 'BB.varX', 'AA-BB', 'probeset_id']

# loading files
snp_statistics_txt = Path(path_to_snp_statistics).resolve()
snp_call_contrast_positions_txt = Path(path_to_snp_call_contrast_positions).resolve()
snp_statistics_length = sum(1 for row in open(snp_statistics_txt, 'r'))
snp_call_contrast_positions_length = sum(1 for row in open(snp_call_contrast_positions_txt, 'r'))
snp_statistics_df = pandas.DataFrame()
snp_call_contrast_positions_df = pandas.DataFrame()

    # snp_statistics
typer.secho(f"Reading file: {snp_statistics_txt}", fg="red", bold=True)
typer.secho(f"total rows: {snp_statistics_length}", fg="green", bold=True)
with tqdm.auto.tqdm(total=snp_statistics_length, desc="chunks read: ") as bar:
    for i, chunk in enumerate(pandas.read_csv(snp_statistics_txt, delimiter='\t', header=0, chunksize=chunksize, low_memory=False)):
        snp_statistics_df = snp_statistics_df._append(other=chunk)
        bar.update(chunksize)
typer.secho("end of reading chunks...", fg=typer.colors.BRIGHT_RED)
typer.secho(f"Dataframe length:{len(snp_statistics_df)}", fg="green", bold=True)

    # snp_statistics
typer.secho(f"Reading file: {snp_call_contrast_positions_txt}", fg="red", bold=True)
typer.secho(f"total rows: {snp_call_contrast_positions_length}", fg="green", bold=True)
with tqdm.auto.tqdm(total=snp_call_contrast_positions_length, desc="chunks read: ") as bar:
    for i, chunk in enumerate(pandas.read_csv(snp_call_contrast_positions_txt, delimiter='\t', skiprows=5, header=0, chunksize=chunksize, low_memory=False)):
        snp_call_contrast_positions_df = snp_call_contrast_positions_df._append(other=chunk)
        bar.update(chunksize)
typer.secho("end of reading chunks...", fg=typer.colors.BRIGHT_RED)
typer.secho(f"Dataframe length:{len(snp_call_contrast_positions_df)}", fg="green", bold=True)

# hue
for column_name in tqdm.auto.tqdm(snp_call_contrast_positions_df.columns, desc='Removing columns:'):
    if column_name == 'probeset_id':
        pass
    else:
        name_list = column_name.split('.')
        if name_list[-1] == 'CEL_log_ratio':
            snp_call_contrast_positions_df.rename(columns={column_name: name_list[0]}, inplace=True)
        else:
            snp_call_contrast_positions_df.drop(column_name, axis=1, inplace=True)

# merging dataframes
demo_df = pandas.merge(snp_call_contrast_positions_df, snp_statistics_df, on=['probeset_id'], how='inner')


# removing rows with nnc<20
for index, row in tqdm.auto.tqdm(demo_df.iterrows(), total=demo_df.shape[0], desc='Removing rows:'):
    if row['n_NC'] >= 20:
        demo_df.drop(index, inplace=True)
demo_df.reset_index(drop=True, inplace=True)

# kalkulacija
aa_meanx_min_value = demo_df['AA.meanX'].min()
bb_meanx_min_value = demo_df['BB.meanX'].min()
aa_meanx_max_value = demo_df['AA.meanX'].max()
bb_meanx_max_value = demo_df['BB.meanX'].max()
aa_meanx_delta = abs(aa_meanx_max_value) - aa_meanx_min_value
bb_meanx_delta = abs(bb_meanx_max_value) - bb_meanx_min_value

aa_bb = (aa_meanx_delta + bb_meanx_delta) / 2

# calculating aa-bb
for index, row in tqdm.auto.tqdm(demo_df.iterrows(), total=demo_df.shape[0], desc='Calculating AA-BB column:'):
    demo_df.at[index, 'AA-BB'] = demo_df.at[index, 'AA.meanX'] - demo_df.at[index, 'BB.meanX']

demo_filtered_df = pandas.DataFrame(columns=demo_df.columns)
for index, row in tqdm.auto.tqdm(demo_df.iterrows(), total=demo_df.shape[0], desc='Removing AA-BB < aa-bb:'):
    if row['AA-BB'] > aa_bb:
        demo_filtered_df.loc[len(demo_filtered_df)] = row

demo_filtered_df.drop(columns=columns_to_remove, inplace=True)

import os
os.makedirs(output_directory, exist_ok=True)
for column in tqdm.auto.tqdm(demo_filtered_df.columns, desc='Removing columns:'):
    plt.hist(demo_filtered_df[column], bins=160, edgecolor='black')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.title(f'Histogram for {column}')
    output_file_path = os.path.join(output_directory, f'{column}_histogram.png')
    plt.savefig(output_file_path, bbox_inches='tight')
    #plt.show()
    plt.clf()
plt.close('all')