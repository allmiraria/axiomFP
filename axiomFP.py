import os, sys, pathlib, pandas, typer, argparse, tqdm.auto, matplotlib.pyplot as plt

# Argument parsing:
parser = argparse.ArgumentParser(description='Argument parser for axiom frequency plot.')
parser.add_argument('snp_stat', type=str, help='SNP Statistics file')
parser.add_argument('snp_ccp', type=str, help='SNP Call Contrast Positions file')
parser.add_argument('--nnc', type=int, default=20, help='Cutoff value for number of calls.')
parser.add_argument('output_folder', type=str, help='Output folder for histograms.')
args = parser.parse_args()

# Accessing the value of the 'nnc' argument from the parsed arguments
cutoff_value = args.nnc

# axiom_FP intro:
os.system('cls' if os.name == 'nt' else 'clear')
typer.secho('axiomFP')

# Loading files:
typer.secho('Loading files...')

typer.secho(f'Reading file: {pathlib.Path(args.snp_stat).resolve()}', fg=typer.colors.GREEN)
snp_statistics_df = pandas.DataFrame()
with tqdm.auto.tqdm(total=sum(1 for row in open(pathlib.Path(args.snp_stat).resolve(), 'r')), desc=str(pathlib.Path(args.snp_stat).resolve()).split('/')[-1]) as bar:
    for i, chunk in enumerate(pandas.read_csv(pathlib.Path(args.snp_stat).resolve(), delimiter='\t', header=0, chunksize=5000, low_memory=False)):
        snp_statistics_df = snp_statistics_df._append(other=chunk)
        bar.update(5000)
typer.secho('Done.', fg=typer.colors.GREEN)

typer.secho(f'Reading file: {pathlib.Path(args.snp_ccp).resolve()}', fg=typer.colors.GREEN)
snp_call_contrast_positions_df = pandas.DataFrame()
with tqdm.auto.tqdm(total=sum(1 for row in open(pathlib.Path(args.snp_ccp).resolve(), 'r')), desc=str(pathlib.Path(args.snp_ccp).resolve()).split('/')[-1]) as bar:
    for i, chunk in enumerate(pandas.read_csv(pathlib.Path(args.snp_ccp).resolve(), delimiter='\t', skiprows=5, header=0, chunksize=5000, low_memory=False)):
        snp_call_contrast_positions_df = snp_call_contrast_positions_df._append(other=chunk)
        bar.update(5000)
typer.secho('Done.', fg=typer.colors.GREEN)

# Filtering and histograms:
typer.secho('Removing and renaming columns.', fg=typer.colors.GREEN)
for column_name in tqdm.auto.tqdm(snp_call_contrast_positions_df.columns, desc='Removing columns'):
    if column_name == 'probeset_id':
        pass
    else:
        name_list = column_name.split('.')
        if name_list[-1] == 'CEL_log_ratio':
            snp_call_contrast_positions_df.rename(columns={column_name: name_list[0]}, inplace=True)
        else:
            snp_call_contrast_positions_df.drop(column_name, axis=1, inplace=True)
demo_df = pandas.merge(snp_call_contrast_positions_df, snp_statistics_df, on=['probeset_id'], how='inner')
typer.secho('Removing rows with high call rates.', fg=typer.colors.GREEN)
for index, row in tqdm.auto.tqdm(demo_df.iterrows(), total=demo_df.shape[0], desc='Removing rows'):
    if row['n_NC'] >= cutoff_value:
        demo_df.drop(index, inplace=True)
demo_df.reset_index(drop=True, inplace=True)
aa_meanx_min_value = demo_df['AA.meanX'].min()
bb_meanx_min_value = demo_df['BB.meanX'].min()
aa_meanx_max_value = demo_df['AA.meanX'].max()
bb_meanx_max_value = demo_df['BB.meanX'].max()
aa_meanx_delta = abs(aa_meanx_max_value) - aa_meanx_min_value
bb_meanx_delta = abs(bb_meanx_max_value) - bb_meanx_min_value
aa_bb = (aa_meanx_delta + bb_meanx_delta) / 2
typer.secho('Calculating AA.meanX and BB.meanX difference.', fg=typer.colors.GREEN)
for index, row in tqdm.auto.tqdm(demo_df.iterrows(), total=demo_df.shape[0], desc='Calculating AA-BB column'):
    demo_df.at[index, 'AA-BB'] = demo_df.at[index, 'AA.meanX'] - demo_df.at[index, 'BB.meanX']
demo_filtered_df = pandas.DataFrame(columns=demo_df.columns)
typer.secho('Removing rows where AA.meanX and BB.meanX difference is smaller than average...', fg=typer.colors.GREEN)
for index, row in tqdm.auto.tqdm(demo_df.iterrows(), total=demo_df.shape[0], desc='Removing AA-BB < aa-bb'):
    if row['AA-BB'] > aa_bb:
         if -0.5 <= row['AB.meanX'] <= 0.5:
            # If both conditions are met, add the row to demo_filtered_df
            demo_filtered_df.loc[len(demo_filtered_df)] = row
typer.secho('Removing rows where AB.meanX is outside the range [-0.5, 0.5]...', fg=typer.colors.GREEN)
demo_filtered_df = demo_filtered_df[(demo_filtered_df['AB.meanX'] >= -0.5) & (demo_filtered_df['AB.meanX'] <= 0.5)]
# Drop specified columns
columns_to_drop = ['n_NC', 'AA.meanX', 'AB.meanX', 'BB.meanX', 'AA-BB', 'probeset_id']
demo_filtered_df.drop(columns=columns_to_drop, inplace=True)
# Set DPI for the plot
plt.rcParams['savefig.dpi'] = 400
#Create output folder
os.makedirs(args.output_folder, exist_ok=True)
typer.secho('Generating column histograms.', fg=typer.colors.GREEN)
for column in tqdm.auto.tqdm(demo_filtered_df.columns, desc='Generating histograms'):
    plt.hist(demo_filtered_df[column], bins=160, edgecolor='black')
    plt.xlabel(column)
    #plt.xticks([])
    plt.ylabel('Frequency')
    plt.title(f'Histogram for {column}')
    output_file_path = os.path.join(args.output_folder, f'{column}_histogram.png')
    plt.savefig(output_file_path, bbox_inches='tight')
    plt.clf()
    plt.close('all')
