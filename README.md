# b_allele_plot
A software for generating b allele plots from Axiom data.
(Requires input files generated in Axiom Analysis Suite Software) 

# what's new
New...

# how to use
Visit www.motherlandia.org for details.

Step 1. This step involves preparing the input files in the Axiome Analysis Suite  Software.

Run a new Genotyping project - make the cr-cutoff arbitrarily low

Select ProbeSet Summary Table
Select "Reanalyze"
Select "Regenerate SNP Metrics"
Tick the box for "Generate advanced metrics
Click OK and wait for the advanced metrics to calculate
Click show/hide columns
Tick AA.meanX, AAvarX, AB.meanX, BB.meanX, and BB.varX, and n_NC
Click export -> current table and save the file
This is the "SNP statistics file" (UPISATI EKSTENZIJU)
  
  Click export -> genotyping data
  Tick "Signal"
  Untick everything in "Select Probeset Data Columns to Include" and "Select Annotation Column(s) to Add"
  Save the file
  This is the "SNP call contrast positions file"  (UPISATI EKSTENZIJU)

Step 2. 

Use the "SNP statistics file" and "SNP call contrast positions file" as input ... 
.. ovo cu znat kad Mirza naklika softver
