# axiomFP (axiom frequency plot)
A software for generating frequency plots from Axiom data.

_(Requires input files generated in Axiom Analysis Suite Software)_

# what's new
..Added the option to define the cutoff value for number of calls

## Required Python Libraries 
* os (built-in, no installation required) 
* sys (built-in, no installation required) 
* pathlib (built-in, no installation required)
* argparse (built-in, no installation required)
* pandas
* typer
* tqdm
*  matplotlib
_Install using the following code_

_pip3 install pandas typer tqdm matplotlib_

## Step 1. 
_This step involves preparing the input files in the Axiome Analysis Suite  Software._
_In case you haven't used Axiom Analysis Suite before, it's best to check out the instructions manual from the official website._

A)

* In Axiome Analysis Suite, start New Analysis.
* Upload the .CEL files you want to test.
* In threshold settings, make the cr-cutoff arbitrarily low.
* Run a new Genotyping project.

B)

* Select ProbeSet Summary Table
* Select "Reanalyze"
* Select "Regenerate SNP Metrics"
* Tick the box for "Generate advanced metrics
* Click OK and wait for the advanced metrics to calculate

C)
> _To generate the SNP_statistics_file_
> 
* Click show/hide columns
* Tick AA.meanX, AB.meanX, BB.meanX, and n_NC (make sure to untick everything else)
* Click export -> current table and save the file and name it _(for example "SNP_stat")_
*  Click OK. Folder where the file is saved will be automaticaly opened. 

D) 
> _To generate the SNP_call_contrast_positions_file_
> 
* Click export -> genotyping data
* In "Exported Data" field tick "Signal"
* Uncheck everything in these fields: "Select Probeset Data Columns to Include" and "Select Annotation Column(s) to Add" 
* Insert output file name _(for example "SNP_call")_
* Make sure to choose the destination folder for your file in the "Output files" field.

E) 

* Put all generated files _"SNP_statistics_file"_ _(SNP_stat.txt)_ and _"SNP_call_contrast_positions_file"_ _(SNP_call.txt)_ in the same folder with the software, or specify folder location in the code.

## Step 2. 
_This step explains how to use the software to create **b-allele plots**_

Clone a git repository to a desired folder 

`git clone https://github.com/dunchained/b_allele_plot.git B allele plot`

Change directory to the created folder
 
`cd axiom_FP`

This is how to run the software. "output" is the name of the newly generated folder that contains the newly generated plots

`python axiomFP.py SNP_statistics_file.txt SNP_call_contrast_positions_file.txt output 

_(*depending on the operating system, command ‘python’ may need to be replaced by the python version installed e.g python3)_

The deafult threshold for missing call rates is 20. If you want to define this value use function: --nnc
For example: if we want to set the cut off rate at 60 

`python axiomFP.py SNP_statistics_file.txt SNP_call_contrast_positions_file.txt --nnc 60 output

For help run:

`python axiomFP.py -h`

For any additional questions or issues feel free to leave a comment.
