# axiomFP (axiom frequency plot)
A software for generating frequency plots from Axiom data.

_(Requires input files generated in Axiom Analysis Suite Software)_

# what's new
..Added the option to define the cutoff value for number of calls

## Step 1. 
_This step involves preparing the input files in the Axiome Analysis Suite  Software._
_In case you haven't used Axiom Analysis Suite before, it's best to check out the instructions manual from the official website._

A)

* In Axiome Analysis Suite, start New Analysis.
* Upload the files you want to test.
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
* Tick AA.meanX, AAvarX, AB.meanX, BB.meanX, and BB.varX, and n_NC
* Click export -> current table and save the file and name it _(for example "SNP_stat")_

D) 
> _To generate the SNP_call_contrast_positions_file_
> 
* Click export -> genotyping data
* In "Exported Data" fields tick "Signal"
* Uncheck everything in these fields: "Select Probeset Data Columns to Include" and "Select Annotation Column(s) to Add" 
* Insert output file name _(for example "SNP_call")_
* Click OK. Folder where the file is saved will be automaticaly opened. 

E) 

* Put all generated files _"SNP_statistics_file"_ _(SNP_stat.txt)_ and _"SNP_call_contrast_positions_file"_ _(SNP_call.txt)_ in the same folder with the software, or specify folder location in the code.

## Step 2. 
_This step explains how to use the software to create **b-allele plots**_

Clone a git repository to a desired folder 

`git clone https://github.com/dunchained/b_allele_plot.git B allele plot`

Change directory to the created folder
 
`cd axiom_FP`

This is how to run the software. "output" is the name of the newly generated folder that contains b allele plots :)

`python axiomFP.py SNP_statistics_file.txt SNP_call_contrast_positions_file.txt output`

_(*depending on the operating system, command ‘python’ may need to be replaced by the python version installed e.g python3)_

For help run:

`python axiomFP.py -h`

For any additional questions or issues feel free to leave a comment.
