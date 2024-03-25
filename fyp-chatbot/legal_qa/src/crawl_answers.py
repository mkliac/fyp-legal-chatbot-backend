# coding: utf-8

from crawler.crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler(sleep_time=15)

    # load to-crawl list
    import json
    with open('to_crawl_questions/queries_from_contract_iter3.json') as f:
        to_crawl_list = json.loads(f.read())

    # start crawling process
    crawler.crawlList_multiProc(to_crawl_list[630000:], sublist_size=4, n_proc=8, 
                            save_per=512,
                            sleep_after_save=30,
                            save_dir='/data/jchengaj/contract_iter3_cpu3')
