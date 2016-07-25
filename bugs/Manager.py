# -*- coding:utf-8 -*-
import threading
import Queue
import datatool
import json


class TaskManager():
    def __init__(self, maxqueue, maxtaskWorker, task, start, city_name, job_name):
        self._threads = []
        self._maxqueue = maxqueue
        self._maxtaskWorker = maxtaskWorker
        self._city_name = city_name
        self._job_name = job_name
        self._cout = start
        self._queue = Queue.Queue()
        self.initTask(task)
        self.initThreads()

    def initTask(self, _t):
        for mtask in _t:
            self._queue.put(mtask)

    def initThreads(self):
        for i in range(self._maxtaskWorker):
            self._threads.append(TaskWorker(self._queue, self._cout, self._maxqueue, self._city_name, self._job_name))

    def run(self):
        for t in self._threads:
            t.setDaemon(True)
            t.start()

    def complete(self):
        self._queue.join()


class TaskWorker(threading.Thread):
    def __init__(self, wokerTask, count, max, city_name, job_name):
        threading.Thread.__init__(self)
        self._wokerTask = wokerTask
        self._count = count
        self._max = max
        self._city_name = city_name
        self._job_name = job_name

    def run(self):
        while True:
            if not self._wokerTask.empty():
                self._count += 1
                url = self._wokerTask.get()
                pay_list = []
                for page in range(1, 4):
                    p = 'p' + str(page) + '/'
                    c_url = url + p
                    res = datatool.gethtml(c_url, 0)
                    if res is not None:
                        temp_list = datatool.analyze_data(res, u'[0-9]+-[0-9]+/月')
                    else:
                        temp_list = []
                    if len(temp_list) > 0:
                        pay_list.extend(temp_list)
                    else:
                        break
                if len(pay_list) > 0:
                    min_wage = []
                    max_wage = []
                    for wage_rang in pay_list:
                        wage_rang = wage_rang[0:-2].split('-')
                        min_wage.append(int(wage_rang[0]))
                        max_wage.append(int(wage_rang[1]))
                    value = str(sum(min_wage) / len(min_wage)) + '-' + str(sum(max_wage) / len(max_wage))
                    url = url[22:].split('/')
                    city_key = 'http://jobs.51job.com/' + url[0] + '/'
                    city = self._city_name[city_key]
                    job_key = url[1] + '/'
                    job = self._job_name[job_key]
                    key = city + '/' + job
                    result = {key: value}
                    name = '../bugs/average_wage.json'
                    fo = open(name, 'a')
                    fo.write(json.dumps(result, ensure_ascii=False))
                    fo.close()
                loop_count = '../bugs/loop_count.txt'
                fo = open(loop_count, 'a')
                fo.write('1')
                print(str(self._count) + '/' + str(self._max))
