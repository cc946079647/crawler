import Queue


class ConcurrencyUrlList:
    def __init__(self, seed):
        self.waiting = Queue.Queue(1024)
        if isinstance(seed, list):
            for url in list:
                if isinstance(url, basestring):
                    self.waiting.put(url)
        elif isinstance(seed, basestring):
            self.put(seed)

    def get(self):
        url = self.waiting.get()
        return url

    def finish(self,url):
        pass

    def put(self, url):
        if isinstance(url, list):
            for str in url:
                self.waiting.put(str)
        elif isinstance(url ,basestring):
            self.waiting.put(url)

    def waitingsize(self):
        return self.waiting.qsize()

    def finishedsize(self):
        return self.finished.qsize()

    def printwaiting(self):
        for url in self.waiting:
            print url


class SequentialUrlList:
    def __init__(self,seed):
        self.waiting = []
        self.finished = []
        if isinstance(seed, list):
            for url in seed:
                if isinstance(url, basestring):
                    self.waiting.append(url)
        elif isinstance(seed, basestring):
            self.waiting.append(seed)

    def get(self):
        if not len(self.waiting) == 0:
            return self.waiting.pop()
        else:
            return None

    def finish(self, url):
        pass

    def put(self, url):
        if isinstance(url, list):
            for one in url:
                if isinstance(one, basestring):
                    self.waiting.append(one)
        elif isinstance(url, basestring):
            self.waiting.append(url)

    def waitingsize(self):
        return len(self.waiting)

    def finishedsize(self):
        return len(self.finished)

    def printwaiting(self):
        for url in self.waiting:
            print url


class UrlList:
    def __init__(self, seed, concurrency=False):
        self.concurrency = concurrency

        if concurrency:
            self._list_ = ConcurrencyUrlList(seed)
        else:
            self._list_ = SequentialUrlList(seed)

    def put(self, url):
        self._list_.put(url)

    def get(self):
        return self._list_.get()

    def waitingcount(self):
        return self._list_.waitingsize()

    def finishedcount(self):
        return self._list_.finishedsize()

    def printwaiting(self):
        self._list_.printwaiting()

if __name__=='__main__':
    url = []
    baseurl = "http://dtt.pirate1024.name/pw/thread.php?fid=3"
    parasplit = "&page="

    for page in range(6):
        url.append(baseurl + parasplit + str(page))
    urllist = UrlList(url)
    urllist.printwaiting()