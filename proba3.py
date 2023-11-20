import pandas as pd
from tqdm import tqdm

df = pd.concat([chunk for chunk in tqdm(pd.read_csv('input/SNP_call_contrast_positions_file.txt', chunksize=1000, delimiter='\t'), desc='Loading data')])
print(df)