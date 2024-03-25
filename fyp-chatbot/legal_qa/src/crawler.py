# coding: utf-8

import os
import re
import json
import multiprocessing as mp
from time import time, sleep
from html_parser import HtmlParser as Parser
from downloader import Downloader


class Crawler:
    def __init__(self, sleep_time=1):
        self.downloader = Downloader()
        self.parser = Parser()
        self.manager = mp.Manager()
        self.baseurl = "https://www.google.com/search?q={}"

        self.sleep_time = sleep_time

        self.crawledData = []

    def crawlUnit(self, url, crawled_dict={}):
        ''' Crawl one page of information, if retr_new_urls is set to True, return the 
            corresponding polysemantics urls and downstream urls '''
        response = self.downloader.download(url)

        if response:
            data = {}

            content = response.text
            if content:
                main_data = self.parser.parse(content)
                data.update(main_data)
            return data

        return None
        

    def crawlOne(self, url, crawled_dict, future_dict, result_list):
        ''' Crawl One page '''
        # query like 'is it legal to burn flags'

        # check whether the url has been crawled
        if url in crawled_dict:
            return
        
        # crawl the root page
        result = self.crawlUnit(self.baseurl.format(url))
        sleep(self.sleep_time)

        if result:
            # normal response, continue on polysemantics
            # data, new_urls = result
            try:
                result_list.append({'question': url, 'result': result})
                crawled_dict[url] = 1 

                if url in future_dict:
                    del future_dict[url]
            except:
                print('Error occurred at query:', url)
            
            collaborative_questions = result['collaborative_questions']
            if collaborative_questions is not None:
                for question in collaborative_questions['info']:
                    if question not in crawled_dict:
                        future_dict[question] = 1

        else:
            # error response, return None
            return 

    def crawlList_submp(self, url_list, crawled_dict, future_dict, result_list):
        ''' Sub-func for crawling data in parallel. '''
        for url in url_list:
            self.crawlOne(url, crawled_dict, future_dict, result_list)
            

    def crawlList_multiProc(self, url_list, sublist_size=4, n_proc=8, save_per=1000, sleep_after_save=0, save_dir='data'):
        ''' Crawl data from the given list of urls and save to file per "save_per" items. Run in parallel.

        Args:
            url_list <list of str>: list of urls to be crawled from websites
            sublist_size <int>:     length of sublist to be assigned to each process
            n_proc <int>:           number of processes
            save_per <int>:         when the length of crawled data exceeds this threshold, save to file
            save_dir <str>:         target directory to put all the saved data
        '''
        if not os.path.exists(save_dir): 
            os.mkdir(save_dir)
            save_fn_index = 1
        else:
            fn_list = list(os.walk(save_dir))[0][2]
            num_list = [int(fn) for fn in fn_list if not fn.endswith('json')]
            save_fn_index = (1 + max(num_list)) if len(num_list) > 0 else 1

        span_size = sublist_size * n_proc
        crawled_fn = os.path.join(save_dir, 'crawled.json')
        crawled_dict = self.manager.dict()  # record crawled urls, either failed or success
        if os.path.exists(crawled_fn):
            with open(crawled_fn, 'r') as f:
                crawled_names = json.loads(f.read())
            crawled_dict.update(crawled_names)

        future_dict = self.manager.dict()   # record urls to be crawled in the future
        future_fn = os.path.join(save_dir, 'future.json')
        if os.path.exists(future_fn):
            with open(future_fn, 'r') as f:
                future_items = json.loads(f.read())
            future_dict.update(future_items)

        result_list = self.manager.list()
        result_list_len_bias = 0
        last_i = 0

        st = time()
        for i in range(0, len(url_list), span_size):
            jobs = []
            for n in range(n_proc):
                sub_url_list = url_list[i+n*sublist_size: i+(n+1)*sublist_size]
                job = mp.Process(target=self.crawlList_submp, args=(sub_url_list, crawled_dict, future_dict, result_list))
                job.start()
                jobs.append(job)
            for job in jobs:
                job.join()

            print('Time elapsed: {:.2f}s, Processed(Success)/Total：{}({})/{}'.format(time()-st, \
                i+span_size, len(result_list) + result_list_len_bias, len(url_list)), end='\r')

            if len(result_list) > save_per:
                this_i = i + span_size
                fn = os.path.join(save_dir, '{}'.format(save_fn_index))

                # save to file
                self.saveToFile(list(result_list), fn)
                save_fn_index += 1

                self.saveToFile(dict(crawled_dict), crawled_fn)
                self.saveToFile(dict(future_dict), future_fn)

                # sleep after saving to file
                sleep(sleep_after_save)

                # reallocate result list, update params
                result_list_len_bias += len(result_list)
                last_i = this_i
                result_list = self.manager.list()

        self.saveToFile(dict(crawled_dict), crawled_fn)
        if len(result_list) > 0:
            this_i = len(url_list)
            fn = os.path.join(save_dir, '{}'.format(save_fn_index))
            self.saveToFile(list(result_list), fn)
            result_list_len_bias += len(result_list)
            self.saveToFile(dict(crawled_dict), crawled_fn)
            self.saveToFile(dict(future_dict), future_fn)



    def saveToFile(self, data, to_filename, mode='w'):
        ''' Save data to file in json format.
        '''
        with open(to_filename, mode) as f:
            f.write(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':')))




if __name__ == '__main__':
    crawler = Crawler()
    # get = crawler.crawlUnit('https://www.google.com/search?q=is it legal to burn flags')
    # get = crawler.crawlOne('is it legal to burn flags', {}, {}, [])
    crawler.crawlList_multiProc(['is it legal to burn flags', 'is it legal to kill people'])
    # print(get)
    exit()

    # crawler = Crawler()
    # crawler.crawlList_multiProc(['/item/永生之酒'])
    # exit()

    # print(crawler.crawlOne('永生之酒'))
    # print(crawler.crawlOne(r'http://zhishi.me/hudongbaike/resource/%E8%BF%AA%E5%BD%A9'))
    # print(crawler.crawlOne(r'http://zhishi.me/hudongbaike/resource/%E5%BA%84%E5%9F%B9%E5%87%AF'))


    with open('/data/cjy/json_for_extract/zhishime_json/baidubaike/home/wl/zhishime2/baidubaike/baidubaike_instance_types_zh.json') as f:
        import json
        urls = json.loads(f.read())
        urls = [item['@id'] for item in urls]

    # crawler.crawlList(urls)
    if not os.path.exists('newdir'): os.mkdir('newdir')
    crawler.crawlList_multiProc(urls, save_per=500, save_dir='newdir')
