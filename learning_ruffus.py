
# coding: utf-8

# # Learning ruffus
# 
# Computational pipelines transform your data in stages until the final result is produced. One easy way to understand pipelines is by imagining your data flowing across a series of pipes until it reaches its final destination. Even quite complicated processes can be broken into simple stages. Of course, it helps to visualise the whole process.
# 
# Ruffus is a way of automating the plumbing in your pipeline: You supply the python functions which perform the data transformation, and tell Ruffus how these pipeline task functions are connected up. Ruffus will make sure that the right data flows down your pipeline in the right way at the right time.
# 
# ### First example: a FASTA to statistics pipeline
# 
# Start loading the package and defining the functions:

# In[8]:

from ruffus import *


# Generate some datasets:
#     

# In[10]:

starting_files = ["a.fasta", "b.fasta", "c.fasta"]

for ff in starting_files:
    open(ff, "w")


# Ruffus makes exactly the same function calls on your behalf. However, first, we need to tell Ruffus what the arguments should be for each of the function calls.
# 
# - The Input is easy: This is either the starting file set (*.fasta) or whatever is produced by the previous stage.
# - The Output file name is the same as the Input but with the appropriate extension.
# 
# These are specified using the Ruffus @transform decorator as follows:

# In[13]:

#
#   STAGE 1 fasta->sam
#
@transform(starting_files,                     # Input = starting files
            suffix(".fasta"),                  #         suffix = .fasta
            ".sam")                            # Output  suffix = .sam
def map_dna_sequence(input_file,
                    output_file):
    ii = open(input_file)
    oo = open(output_file, "w")

#
#   STAGE 2 sam->bam
#
@transform(map_dna_sequence,                   # Input = previous stage
            suffix(".sam"),                    #         suffix = .sam
            ".bam")                            # Output  suffix = .bam
def compress_sam_file(input_file,
                      output_file):
    ii = open(input_file)
    oo = open(output_file, "w")

#
#   STAGE 3 bam->statistics
#
@transform(compress_sam_file,                  # Input = previous stage
            suffix(".bam"),                    #         suffix = .bam
            ".statistics",                     # Output  suffix = .statistics
            "use_linear_model")                # Extra statistics parameter
def summarise_bam_file(input_file,
                       output_file,
                       extra_stats_parameter):
    """
    Sketch of real analysis function
    """
    ii = open(input_file)
    oo = open(output_file, "w")


# Now we can run the pipeline with the Ruffus function pipeline_run:

# In[7]:

pipeline_run()


# In[ ]:



