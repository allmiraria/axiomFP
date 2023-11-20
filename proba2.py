import os
import sys
from tqdm import tqdm
import pandas as pd


INPUT_FILENAME = 'input/SNP_call_contrast_positions_file.txt'
LINES_TO_READ_FOR_ESTIMATION = 20
CHUNK_SIZE_PER_ITERATION = 10**5


temp = pd.read_csv(INPUT_FILENAME,
                   nrows=LINES_TO_READ_FOR_ESTIMATION)
N = len(temp.to_csv(index=False))
df = [temp[:0]]
t = int(os.path.getsize(INPUT_FILENAME)/N*LINES_TO_READ_FOR_ESTIMATION/CHUNK_SIZE_PER_ITERATION) + 1


with tqdm(total = t, file = sys.stdout) as pbar:
    for i,chunk in enumerate(pd.read_csv(INPUT_FILENAME, chunksize=CHUNK_SIZE_PER_ITERATION, low_memory=False)):
        df.append(chunk)
        pbar.set_description('Importing: %d' % (1 + i))
        pbar.update(1)

data = temp[:0]._append(df)
print(df)          