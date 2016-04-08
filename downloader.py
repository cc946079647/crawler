#coding:utf-8
import urllib2
from urllib2 import URLError, HTTPError
import config
import html_parser
import logger
import urllist
import string
import os
import io

logger = logger.logger()
config = config.Config()


class Downloader:
    def __init__(self, urllist , parser, config):
        self.urllist = urllist
        self.url2page = {}
        self.url2parsed= {}
        self.parser = parser
        self.config = config
        self.working = True

    def start(self):
        headers = {}
        headers['User-Agent'] = self.config['agent']
        while self.working:
            url = self.urllist.get()
            retry = 0
            while retry < 10 and not url:
                url = self.urllist.get()
                retry += 1
            if retry >= 10:
                self.stop()
                continue
            request = urllib2.Request(url, headers=headers)
            try:
                response = urllib2.urlopen(request)
            except HTTPError, err:
                logger.log('Error', 'HTTPError')
                logger.log('Error', err.code)
            except URLError, err:
                logger.log('Error', 'URLError')
                logger.log('Error', err.reason)
            else:
                pagecontent = response.read()
                if self.parser:
                    res = self.parser.parse(pagecontent)
                    self.url2parsed[url] = res
                self.url2page[url] = pagecontent
                logger.log('Info', 'download ' + url)

    def stop(self):
        self.working = False

    def save(self, page_dir='pages\\', parsed_dir='parsed\\'):
        trans_table_list = config['IO']['file_name_tran_table']
        trans_table = string.maketrans(trans_table_list[0], trans_table_list[1])
        if self.config['save_page']:
            if page_dir.find("\\") == -1:
                page_dir += '\\'
            if not os.path.exists(page_dir):
                os.mkdir(page_dir)
            for url, content in self.url2page.items():
                filename = url+".html"
                filename = filename.translate(trans_table)
                print filename
                with open(page_dir + filename, "w+") as f:
                    assert isinstance(content, basestring)
                    f.write(content)
        if self.config['save_parsed']:
            if parsed_dir.find("\\") == -1:
                parsed_dir += '\\'
            if not os.path.exists(parsed_dir):
                os.mkdir(parsed_dir)
            for url, content in self.url2parsed.items():
                filename = url+".txt"
                filename = filename.translate(trans_table)
                print filename
                assert isinstance(content, dict)
                with io.open(parsed_dir + filename, "w+", encoding='utf-8') as f:
                    assert isinstance(content, dict)
                    for tag, value_dict in content.items():
                        f.write(unicode(tag + '\n'))
                        assert isinstance(value_dict, dict)
                        for seek, value_list in value_dict.items():
                            assert isinstance(value_list, list)
                            f.write(unicode(seek + '\n'))
                            for val in value_list:
                                assert isinstance(val, basestring)
                                f.write(unicode(val))
                                f.write(unicode('\n'))

if __name__ == '__main__':
    url = []
    baseurl = "http://bww.yakexi1024.net/pw/thread.php?fid=5"
    parasplit = "&page="
    for page in range(1):
        url.append(baseurl + parasplit + str(page))
    urllist = urllist.UrlList(url)
    p = html_parser.Parser(config['parser'])
    downloader = Downloader(urllist, p, config['downloader'])
    downloader.start()
    downloader.save()
