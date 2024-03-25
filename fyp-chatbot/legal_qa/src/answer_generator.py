# coding: utf-8

# An answer generator object based on GenQA (BART-large finetuned on MSMARCO v2.1)

import os
import json
import torch
from transformers import (
    AutoConfig,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    pipeline
)

# set this param to change using gpu/cpu
device = 0 if torch.cuda.is_available() else -1

class AnswerGenerator:
    def __init__(self, LM_checkpoint_path=''):
        assert os.path.exists(LM_checkpoint_path)

        config = AutoConfig.from_pretrained(
            LM_checkpoint_path,
            cache_dir=None,
            revision='main',
            use_auth_token=None,
        )
        tokenizer = AutoTokenizer.from_pretrained(
            LM_checkpoint_path,
            cache_dir=None,
            use_fast=True,
            revision='main',
            use_auth_token=None,
        )
        model = AutoModelForSeq2SeqLM.from_pretrained(
            LM_checkpoint_path,
            from_tf=bool(".ckpt" in LM_checkpoint_path),
            config=config,
            cache_dir=None,
            revision='main',
            use_auth_token=None,
        )
        model.resize_token_embeddings(len(tokenizer))

        # get pipeline for text-to-text summarizer
        self.LMAG = pipeline('text2text-generation', model=model, tokenizer=tokenizer, config=config, device=device)

    def __call__(self, source_text, max_length=128, num_beams=4):
        return self.LMAG(source_text, max_length=max_length, num_beams=num_beams)



if __name__ == '__main__':
    ans_gen = AnswerGenerator('/data/jchengaj/gen-qa-summarization/checkpoint-151000/')


    # ans_gen("<question>\n. what is a corporation?\n<passages>\nA company is incorporated in a specific nation, often within the bounds of a smaller subset of that nation, such as a state or province. The corporation is then governed by the laws of incorporation in that state. A corporation may issue stock, either private or public, or may be classified as a non-stock corporation. If stock is issued, the corporation will usually be governed by its shareholders, either directly or indirectly.\nToday, there is a growing community of more than 2,100 Certified B Corps from 50 countries and over 130 industries working together toward 1 unifying goal: to redefine success in business. Join the Movement\nCorporation definition, an association of individuals, created by law or under authority of law, having a continuous existence independent of the existences of its members, and powers and liabilities distinct from those of its members. See more.\nExamples of corporation in a Sentence. 1  He works as a consultant for several large corporations. 2  a substantial corporation that showed that he was a sucker for all-you-can-eat buffets.\n1: a government-owned corporation (as a utility or railroad) engaged in a profit-making enterprise that may require the exercise of powers unique to government (as eminent domain) — called also government corporation, publicly held corporation")

    # # [{'generated_text': 'CorCorporation is an association of individuals, created by law or under authority of law'}]
    # # "summary": "A corporation is a company or group of people authorized to act as a single entity and recognized as such in law."



    # ans_gen("<question>\ncan you burn your lawn with fertilizer\n<passages>\nVerify the reason for the lawn burn. Grass will turn yellow due to an over application of high nitrogen fertilizer. The lawn will also turn yellow when it goes dormant in the fall. Rake the lawn to remove as much dead grass as possible. Remove several inches of soil if the herbicide was not a high nitrogen type.\nThese spots are generally caused by a buildup of nitrogen in the soil. Although nitrogen is required to make the lawn green, a lawn burn is a case of too much of a good thing. The nitrogen buildup may be caused by over-fertilizing your lawn, or it may be caused by urine deposits left by pets. No matter what the source of nitrogen burn marks, fixing the discolored lawn is relatively easy.\nPosition the sprinkler over the portion of overfertilized lawn. Turn on the sprinkler and allow it to run until the soil below the grass becomes fully saturated. Allow the water to drain down through the soil, carrying the excess fertilizer with it. Apply 1 inch of water per day for the next seven days.\nWhen fertilizing start with a dry lawn. Using either a broadcast or drop spreader, apply one-half of the recommended amount in one direction then spread the remaining half at right angles to the first. After fertilizing, it is necessary to water your lawn to wash the material off the grass and into the soil.\nFertilizing Tips. Watering and mowing alone will not make a healthy lawn. It must be fertilized. We have included a starter fertilizer in the mixture applied, but it is only sufficient to supply enough nutrients for about 30 to 45 days. It is important for the development of a healthy lawn that a fertilization program be started at this time.")

    # # [{'generated_text': 'Yes burning your lawn with fertilizer.'}]
    # # "summary": "Yes, over fertilizing can burn lawn."



