# b_allele_plot
A software for generating b allele plots from Axiom data.

_(Requires input files generated in Axiom Analysis Suite Software)_

# what's new
New...

# how to use
Visit _www.motherlandia.org_ for details.

## Step 1. 
_This step involves preparing the input files in the Axiome Analysis Suite  Software._

* Run a new Genotyping project - make the cr-cutoff arbitrarily low
* Select ProbeSet Summary Table
* Select "Reanalyze"
* Select "Regenerate SNP Metrics"
* Tick the box for "Generate advanced metrics
* Click OK and wait for the advanced metrics to calculate
* Click show/hide columns
* Tick AA.meanX, AAvarX, AB.meanX, BB.meanX, and BB.varX, and n_NC
* Click export -> current table and save the file

> _This is the SNP_statistics_file.txt_

* Click export -> genotyping data
* Tick "Signal"
* Untick everything in "Select Probeset Data Columns to Include" and "Select Annotation Column(s) to Add" 
* Save the file

> _This is the SNP_call_contrast_positions_file.txt_

## Step 2. 
_This step explains how to use the software to create **b-allele plots**_

Clone a git repository to a desired folder 

`git clone https://github.com/dunchained/b_allele_plot.git B allele plot`

Change directory to the created folder
 
`cd B allele plot`

This is how to run the software.

"output" is the name of the newly generated folder that contains b allele plots :)

`python main.py SNP_statistics_file.txt SNP_call_contrast_positions_file.txt output`

For help run:

`python main.py -h`




