# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import re


class JiefangjunPipeline(object):
    def process_item(self, item, spider):
        cat_no = item['category_no']
        cat_no_str = ('0' + str(cat_no)) if cat_no < 10 else str(cat_no)
        article_no = item['article_no']
        article_no_str = ('0' + str(article_no)) if article_no < 10 else str(article_no)
        SAVE_DIR = 'results/{}{}{}/{}'.format(
            item['year'], item['month'], item['day'], cat_no_str
        )
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        filename = article_no_str + '.txt'
        cat = re.search(r'(\d+)版：(.*)', item['category'])
        category = cat.group(1) + '-' + cat.group(2)

        prefix = '{}{}{}-{}-{}-{}'.format(
            item['year'], item['month'], item['day'], cat_no_str, category,
            article_no_str
        )
        text = ['{}-{}-{}'.format(prefix, '00', item['title'])]
        if item.get('introtitle'):
            text.append('{}-{}-{}'.format(prefix, '+1', item['introtitle']))
        if item.get('subtitle'):
            text.append('{}-{}-{}'.format(prefix, '-1', item['subtitle']))
        if item.get('author'):
            text.append('{}-{}-{}'.format(prefix, '+9', item['author']))
        for i, p in enumerate(item['ps'], start=1):
            if i < 10:
                i_str = '0' + str(i)
            else:
                i_str = str(i)
            text.append('{}-{}-{}'.format(prefix, i_str, p))
        text = '\n'.join(text) + '\n'
        with open(os.path.join(SAVE_DIR, filename), 'w') as f:
            f.write(text)
        return item
