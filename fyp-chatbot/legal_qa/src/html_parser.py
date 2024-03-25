import re
from bs4 import BeautifulSoup
from bs4.builder import HTMLTreeBuilder

class HtmlParser:
    def __init__(self):
        self.timestamp_pat = re.compile(r'^.{0,16}· ')

    def parse(self, html_cont):
        if html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'lxml')
        new_data = self._get_new_data(soup)
        return new_data


    def _get_new_data(self, soup):
        # Collect 4 parts of data. 
        # The feature snippets (if exists), questions other people have asked, normal search results, and related search
        def _get_info(soup):
            # For collecting the feature snippets and normal search results.

            if soup is None: return None

            if ' '.join(soup['class']) == 'ZINbbc xpd O9g5cc uUPGi':
                # when soup is the target element
                info_box = soup
            else:
                info_box = soup.find('div', class_='ZINbbc xpd O9g5cc uUPGi')

            if info_box is None: return None
            if info_box.find('div', class_='BNeawe uEec3 AP7Wnd') is None:
                is_featured_snippet = False
            else:
                is_featured_snippet = True

            text_info = info_box.find('div', class_='BNeawe s3v9rd AP7Wnd')
            short_ans = ''
            if not text_info:
                return None
            else:
                if is_featured_snippet:
                    short_ans_blk = text_info.find('span', class_='atOwb UMOHqf')
                    if short_ans_blk: 
                        short_ans = short_ans_blk.get_text()
                text_info = text_info.get_text()


            # remove the timestamp of the website if it exists
            find_timestamp = self.timestamp_pat.search(text_info)
            timestamp = None
            if find_timestamp:
                timestamp = find_timestamp.group()
                text_info = text_info[len(timestamp):]
                timestamp = timestamp[:len(timestamp)-3]


            addr_hierarchy = info_box.find('div', class_='BNeawe UPmit AP7Wnd')
            if addr_hierarchy: addr_hierarchy = addr_hierarchy.get_text()
            src_site_name = info_box.find('div', class_='BNeawe vvjwJb AP7Wnd')
            if src_site_name: src_site_name = src_site_name.get_text()
            url = info_box.find('a')
            if url: url = url['href']
            return {'text': text_info,
                    'short_answer': short_ans,
                    'addr_hierarchy': addr_hierarchy,
                    'src_site_name': src_site_name,
                    'url': url[7:] if url else None,
                    'timestamp': timestamp,
                    'is_featured_snippet': is_featured_snippet}
    
        def _get_related(soup):
            # For collecting questions other also asked and related searches

            if soup is None: return None

            if soup.find('div', class_='Lt3Tzc') is not None:
                # 'Others also'
                info_boxes = soup.find_all('div', class_='Lt3Tzc')
                info = [i.get_text() for i in info_boxes]
                flag = 'others'

            else:
                # "related search"
                info_boxes = soup.find_all('div', class_='gGQDvd iIWm4b')
                info = [i.get_text() for i in info_boxes] if info_boxes is not None else None
                flag = 'related'

            return {'type': flag, 'info': info}

        # Get main info block
        infoboxes = soup.find_all('div', class_='ZINbbc xpd O9g5cc uUPGi')
        featured_snippet, search_results, collaborative_questions, related_searches = None, [], None, None
        for item in infoboxes:
            if item.find('div', class_='kCrYT'):
                # featured snippet / search results
                info = _get_info(item)
                if info is None: continue

                if info['is_featured_snippet'] is True:
                    featured_snippet = info
                else:
                    search_results.append(info)
            else:
                # questions other have asked / related searches
                info = _get_related(item)
                if info is None: continue
                
                if info['type'] == 'related':
                    related_searches = info
                else:
                    collaborative_questions = info
        
        res_data={'featured_snippet': featured_snippet,
                    'search_results': search_results,
                    'collaborative_questions': collaborative_questions,
                    'related_searched': related_searches}

        return res_data 




if __name__ == '__main__':
    import requests

    res = requests.get("https://www.google.com/search?q=is flag burning illegal?")
    soup = BeautifulSoup(res.text, 'lxml')

    parser = HtmlParser()
    print(parser._get_new_data(soup))