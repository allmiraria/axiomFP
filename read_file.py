from pathlib import Path
import pandas, typer
import tqdm.auto


txt = Path('input/SNP_call_contrast_positions_file.txt').resolve()
length = sum(1 for row in open(txt, 'r'))

# define a chunksize
chunksize = 10000

# initiate a blank dataframe
df = pandas.DataFrame()

# fancy logging with typer
typer.secho(f"Reading file: {txt}", fg="red", bold=True)
typer.secho(f"total rows: {length}", fg="green", bold=True)

# tqdm context
with tqdm.auto.tqdm(total=length, desc="chunks read: ") as bar:
    # enumerate chunks read without low_memory (it is massive for pandas to precisely assign dtypes)
    for i, chunk in enumerate(pandas.read_csv(txt, delimiter='\t', skiprows=5, header=0, chunksize=chunksize, low_memory=False)):
    
        
        # append it to df
        df = df._append(other=chunk)
        
        # update tqdm progress bar
        bar.update(chunksize)
        
        # 6 chunks are enough to test
        #$break
            
# finally inform with a friendly message
typer.secho("end of reading chunks...", fg=typer.colors.BRIGHT_RED)
typer.secho(f"Dataframe length:{len(df)}", fg="green", bold=True)

print(df.head)