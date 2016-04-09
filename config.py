#coding:utf-8
import string

class Config(dict):
    def __init__(self):
        dict.__init__(self)
        self._map_ = {}
        #downloader configuration
        self._map_['downloader'] = {}
        down_config = self._map_['downloader']
        down_config['agent'] = 'Mozilla/5.0'
        down_config['save_page'] = True
        down_config['save_parsed'] = True
        #parser configuratiion
        self._map_['parser'] = {}
        parser_config = self._map_['parser']
        parser_config['method'] = 'css'
        #parser_config['a'] = {}
        #a_config = parser_config['a']
        #a_config['text'] = '合集'
        #a_config['seek'] = 'href'
        parser_config['a'] = []
        a_config = parser_config['a']
        a_config.append('h3 > a')
        a_config.append('href')
        a_config.append('all')
        #a_config.append('text')
        #IO config
        self._map_['IO'] = {}
        io_config = self._map_['IO']
        io_config['file_name_tran_table'] = []
        io_config['file_name_tran_table'].append('/\\?:')
        io_config['file_name_tran_table'].append('____')

    def getConfig(self, key):
        return self._map_.get(key)

    def setConfig(self, key, value):
        if not isinstance(value, dict):
            raise 'config should be a dict!'
        self._map_[key] = value

    def __getitem__(self, item):
        return self._map_[item]

if __name__ == '__main__':
    table = string.maketrans('/\\?', '___')

    str = 'cbww/wed\\cecwce?cwc'
    res = str.translate(table)
    print str
    print res