# coding: utf-8

import os
import re
import json
import tqdm
from nltk.stem import WordNetLemmatizer

# clean the extracted files from extract_svo_kwd_ety.py, and aggregate them to the output file.
# the input are a folder of files in form {ety: list, svo: list, kwd: list}, and the output is a single file of the similar format.


class DataCleaner:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def clean_item(self, input_fn):
        with open(input_fn) as f:
            raw_data = json.loads(f.read())

        def _cln_str(string, len_threshold=5):
            ''' Clean single string. 
            Return the cleaned string if cleanable. (by removing extra lexicons in the front and back.) 
            Else return None'''
            string = string.strip('\" \n,')
            string = re.sub(r'(\'s)$', '', string)

            # filter out those too-short strings
            if len(string) < len_threshold: 
                return None

            tmp_string = re.sub(r'[cC][oO]\.|,? [lL][tT][dD]\.|,? [iI][nN][cC]\.|\'s| [A-Z]\.|[a-zA-Z](-)[a-zA-Z]', '', string)
            
            # whether irrelevant characters still exist in the string
            if re.search(r'[^ a-zA-Z]|\s{2,}', tmp_string):
                return None
            return string
        
        def _cln_tup(tuple):
            ''' Clean a svo tuple extracted by the textacy toolkit '''
            subject, verb, object = tuple
            subject = _cln_str(' '.join(subject), len_threshold=0)
            if not subject: return None
            object = _cln_str(' '.join(object), len_threshold=0)
            if not object: return None

            # verb, active/passive voice; tenses
            for wrd in ['be', 'been', 'is', 'are', 'am', 'was', 'were']:
                if wrd in verb:
                    prefix = 'be'
                    break
            else:
                prefix = ''
            
            vb = verb[-1]
            if prefix: 
                return (subject, prefix+' '+vb, object)
            else:
                vb = self.lemmatizer.lemmatize(vb, pos='v')
                return (subject, vb, object)

        def _cln_ety(ety_list):
            ''' Clean entities (or keywords). 
            For each in the list, if it is cleanable then put the cleaned in the new list; if not, discard it. '''
            new_list = []
            for ety in ety_list:
                new_ety = _cln_str(ety)
                if new_ety: new_list.append(new_ety)
            return new_list
        
        def _cln_svo(svo_list):
            ''' Clean SVO tuples.
            In addition to routine cleansing, also decomposite the tuples into desired pairs.
            '''
            new_svo_list = []
            for svo in svo_list:
                cln_svo = _cln_tup(svo)
                if cln_svo: new_svo_list.append(cln_svo)
            return new_svo_list

        ety_list, kwd_list, svo_list = raw_data['ety'], raw_data['kwd'], raw_data['svo']

        ret_ety_list = _cln_ety(ety_list)
        ret_kwd_list = _cln_ety(kwd_list)
        ret_svo_list = _cln_svo(svo_list)

        return {'ety': ret_ety_list, 'kwd': ret_kwd_list, 'svo': ret_svo_list}



    def clean_dir(self, input_dir, output_dir='.', output_fn='ety_kwd_svo.json'):
        ''' Clean all the data within the input directory and output to file. '''
        assert os.path.exists(input_dir)
        dir_fns = os.listdir(input_dir)

        all_data = {'ety': set(), 'kwd': set(), 'svo': set()}
        for fn in tqdm.tqdm(dir_fns):
            full_fn = os.path.join(input_dir, fn)
            ret = self.clean_item(full_fn)
            for key in all_data:
                all_data[key].update(set(ret[key]))
        
        all_data = {key: list(all_data[key]) for key in all_data}
        with open(os.path.join(output_dir, output_fn), 'w') as f:
            f.write(json.dumps(all_data, ensure_ascii=False))
        




if __name__ == '__main__':
    input_dir = '/home/data/jchengaj/law/CUAD/CUAD_v1/contract_svo_kwd_ety/'
    cleaner = DataCleaner()
    cleaner.clean_dir(input_dir, output_dir=input_dir)
    # cleaner.clean_item('/home/data/jchengaj/law/CUAD/CUAD_v1/contract_svo_kwd_ety/WOMENSGOLFUNLIMITEDINC_03_29_2000-EX-10.13-ENDORSEMENT AGREEMENT.txt')

