# coding: utf-8

import suggests


# queries =[ ['is it', 'what is', 'will it be', 'would it be', 'should it be'], ['legal', 'illegal']]
queries =[['what is', 'will it be', 'should it be'], ['legal', 'illegal']]

all_fn = 'all.json' # 固定接下来所有爬取都将对应爬下来的数据写到同一个文件里

# s = suggests.get_suggests('does legal', source='google', sleep=1, cp=0)

for engine in ['google']:
    for prefix_a in queries[0]:
        for prefix_b in queries[1]:
            query = prefix_a + ' ' + prefix_b
            save_to = query.replace(' ', '_') + '_' + engine + '.json'
            s = suggests.get_suggests_tree(query, source=engine, sleep=0.5, max_depth=10, save_to=save_to, all_fn=all_fn)
# print(s['suggests'], s)
# print(s)
