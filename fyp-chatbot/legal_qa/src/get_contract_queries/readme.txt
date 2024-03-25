This file describes the functions and sequences of the codes in the folder.

(1) extract_svo_kwd_ety.py
This file defines the process to extract SVO tuples, keywords and entities from contract texts. It should be run at first so as to extract all the information needed. After running it, a folder with all the data will be genereated.

(2) aggregate_and_clean.py
This code helps aggregate all the extracted files in the previous stage. Since there might be repetitions and noisy phrases, the job is to clean these noises and eliminate repeated items. It will generate a single output containing all the SVO tuples, keywords and entities.

(3) get_queries.py
This code uses templates to generate queries from the information extracted in the previous codes. It operates directly based on the info given by aggregate_and_clean.py. And generates an output of queries to crawl.
