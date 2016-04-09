import re

from bs4 import BeautifulSoup

import logger

logger = logger.logger()


class Parser:
    def __init__(self, config):
        if not isinstance(config, dict):
            raise 'Parser condigure is a dict!'
        self._config_ = dict(config)
        if self._config_.has_key('encoding'):
            self._encoding_ = self._config_.get('encoding')
        else:
            self._encoding_ = 'utf-8'
        if self._config_.has_key('method'):
            self.method = self._config_['method']
            self._config_.pop('method')
        else:
            self.method = 'css'

    def parse(self, content):
        if self.method == 'css':
            return self.parse_css(content)
        elif self.method == 'tag':
            return self.parse_tag(content)
        else:
            raise 'unknwon parsing method!'

    def parse_css(self, content):
        res = {}
        for tag, constraints in self._config_.items():
            if not isinstance(constraints, list):
                raise 'constraints should be a list'
            constraints = list(constraints)
            ##constraints:[css, seek...]
            if len(constraints) < 2:
                raise 'consteaints should contain at least a css expression and a seek!'
            css_exp = constraints[0]
            seeks = constraints[1:]

            res[tag] = {}
            for seek in seeks:
                res[tag][seek] = []
            #print self._encoding_
            soup = BeautifulSoup(content, 'html.parser')
            findings = soup.select(css_exp)

            for finding in findings:
                #print finding
                if len(finding.contents) != 1:
                    logger.log('warn', 'finding has embedded tags!')
                for seek in seeks:
                    if seek == 'all':
                        res[tag][seek].append(finding)
                    elif seek == 'text':
                        res[tag][seek].append(finding.get_text())
                    else:
                        res[tag][seek].append(finding.get(seek))
        return res

    def parse_tag(self, content):
        res = {}
        for tag, constraints in self._config_.items():
            if not isinstance(constraints, dict):
                raise 'constraints should be a dict!'
            constraints = dict(constraints)
            #no interested value
            if not constraints.has_key('seek'):
                continue
            seeks = None
            if not isinstance(constraints['seek'], list):
                seeks = list()
                seeks.append(constraints['seek'])
            else:
                seeks = constraints['seek']
            res[tag] = {}
            for seek in seeks:
                res[tag][seek] = []

            attr = None
            text = None

            if constraints.has_key('attr'):
                value = constraints.get('attr')
                attr = value
            if constraints.has_key('text'):
                value = constraints.get('text')
                text = value
            soup = BeautifulSoup(content, 'html.parser', from_encoding=self._encoding_)
            if not attr and not text:
                findings = soup.findAll(tag, attr=attr, text=text)
            elif attr:
                findings = soup.findAll(tag, attr=attr)
            elif text:
                findings = soup.findAll(tag, text=re.compile(text))
            else:
                findings = soup.findAll(tag)

            for finding in findings:
                if len(finding.contents) != 1:
                    logger.log('warn', 'finding has embedded tags!')
                for seek in seeks:
                    if seek == 'all':
                        res[tag][seek].append(finding)
                    elif seek == 'text':
                        res[tag][seek].append(finding.get_text())
                    else:
                        res[tag][seek].append(finding.get(seek))
        return res


