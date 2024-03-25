# coding: utf-8

import json


def analyze(fn):
    ''' Compute desired statistics of the designated dataset. '''
    print('Current file:', fn)
    n_questions = 0
    n_answers = 0
    n_featured_snippets = 0
    n_short_answers = 0

    question_lengths = []
    featured_snippet_lengths = []
    short_answer_lengths = []
    answer_lengths = []

    with open(fn) as f:
        for line in f:
            d = json.loads(line)
            n_questions += 1
            n_answers += len(d['result']['search_results']) + 1
            if d['result']['featured_snippet'] is not None:
                n_featured_snippets += 1
                featured_snippet_lengths.append(len(d['result']['featured_snippet']['text'].split(' ')))
                if d['result']['featured_snippet']['short_answer']:
                    n_short_answers += 1
                    short_answer_lengths.append(len(d['result']['featured_snippet']['short_answer'].split(' ')))

            question_lengths.append(len(d['question'].split(' ')))
            
            for ans in d['result']['search_results']:
                answer_lengths.append(len(ans['text'].split(' ')))
    
    mean = lambda x: sum(x)/len(x)
    print('# Questions: {}\n# Answers: {}\n# Featured snippets: {}\n# Short answers in featured snippets: {}\n------\nAvg. length of\n-> questions: {}\n-> answers: {}\n-> featured snippets: {}\n-> short answers in featured snippets: {}'\
            .format(n_questions, n_answers, n_featured_snippets, n_short_answers, mean(question_lengths), mean(answer_lengths), mean(featured_snippet_lengths), mean(short_answer_lengths)))


if __name__ == '__main__':
    analyze('/home/data/jchengaj/crawled_question_answers/contract_iter3_output/all.txt')
