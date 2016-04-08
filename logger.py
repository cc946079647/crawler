import time


class logger:
    def __init__(self):
        self.time_format = '%Y-%m-%d %X'
        pass

    def log(self, level, msg):
        print time.strftime(self.time_format, time.localtime()), "\t", level, msg


if __name__ == '__main__':
    log = logger()
    log.log('war, ', ', test message')
