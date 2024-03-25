# coding: utf-8

import textacy
from nltk.tokenize import sent_tokenize

# extract SVO triples, keywords, entities from contract texts.

class term_extractor:
    def __init__(self, lang='en_core_web_sm'):
        self.lang = textacy.load_spacy_lang(lang)

    def sent_tokenize(self, txt):
        return sent_tokenize(txt)

    def to_doc(self, txt):
        return textacy.make_spacy_doc(txt, self.lang)

    def __call__(self, txt):
        sents = self.sent_tokenize(txt)

        all_svos, all_kwds, all_etys = [], set(), set()
        for sent in sents:
            doc = self.to_doc(sent)

            svos = self.get_svo(doc)
            kwds = self.get_keywrd(doc)
            etys = self.get_entity(doc)

            all_svos += svos
            all_kwds.update(kwds)
            all_etys.update(etys)
        all_kwds = list(all_kwds)
        all_etys = list(all_etys)
        print(all_svos)
        print(all_kwds)
        print(all_etys)

        return dict(svo=all_svos, kwd=all_kwds, ety=all_etys)


    def get_svo(self, doc):
        tmp = [[[k.text for k in i] for i in tuple(n)] for n in textacy.extract.triples.subject_verb_object_triples(doc)]
        return tmp
        # for ..in ret: print(..)
    
    def get_keywrd(self, doc):
        ret = set()

        try:
            kwds = textacy.extract.keyterms.yake(doc)
        except:
            return ret
        for i in kwds:
            ret.add(i[0])
        return ret
    
    def get_entity(self, doc):
        tmp = textacy.extract.basics.entities(doc, exclude_types='NUMERIC')
        ret = set()
        for i in tmp:
            ret.add(i.text)
        return ret


if __name__ == '__main__':
    # text = 'Provider shall maintain complete and accurate records relating to the provision of the Services under this Agreement, in such form as Recipient shall approve.'
    
    import os
    import json
    input_dir = '/home/data/jchengaj/law/CUAD/CUAD_v1/full_contract_txt'

    output_dir = '/home/data/jchengaj/law/CUAD/CUAD_v1/contract_svo_kwd_ety'
    if not os.path.exists(output_dir): os.mkdir(output_dir)

    extractor = term_extractor()
    for fn in os.listdir(input_dir):
        print('Processing: ', fn)
        tmp_fn = os.path.join(input_dir, fn)
        with open(tmp_fn) as fr:
            text = fr.read()

        get = extractor(text)

        with open(os.path.join(output_dir, fn), 'w')  as fw:
            fw.write(json.dumps(get, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ':')))
        
    print(get)


