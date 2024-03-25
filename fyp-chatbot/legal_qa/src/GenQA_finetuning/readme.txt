This folder contains codes for finetuning seq-to-seq transformers (BART-large currently) on MSMARCO dataset.
The settings mainly follow steps from ACL 2021 findings paper "Answer Generation for Retrieval-based Question Answering Systems".
Finetuned checkpoints can serve as query+passages summarizer to generate natural answers from search results.

--First, run preprocess.py to transform the MSMARCO into format that can be comprehended by the transformers.
--Then, run finetune.sh to start the finetuning.

The other .sh files are for preliminary experiments or generating test results. 
All the scripts are ad-hoc and can only work as examplar codes.

After finishing finetuning, manually saving the checkpoints is needed.