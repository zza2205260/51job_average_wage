# -*- coding:utf-8 -*-
import datatool
import Manager

using_url = []
job_list = []
city_codetoname = {}
job_codetoname = {}
# get average wage
# area - hy - job - page(10)
res = datatool.gethtml('http://jobs.51job.com/', 0)
city_job = datatool.analyze_data(res, 'http://jobs.51job.com/[A-Za-z]+/">.+?<')
city_list = city_job[0:70]
job_list = city_job[71:]

for job_url in job_list:
    job_url = job_url.split('"')
    key = job_url[0].split('http://jobs.51job.com/')
    job_codetoname[key[1]] = job_url[1][1:-1]

for url in city_list:
    url = url.split('"')
    key = url[0]
    value = url[1][1:-1]
    city_codetoname[key] = value
    res = datatool.gethtml(key, 0)
    if res is not None:
        temp = datatool.analyze_data(res, 'http://jobs.51job.com/[A-Za-z]+/">.+?<')
        if temp is not None or len(temp) > 0:
            using_url.extend(temp)

using_url = list(set(using_url))
for city_url in using_url:
    city_url = city_url.split('"')
    if city_codetoname.has_key(city_url[0]) is False:
        city_codetoname[city_url[0]] = city_url[1][1:-1]


# ---- get average_wage---------
count = 0
start = 0
go_url = []
for url in city_codetoname:
    for job_url in job_codetoname:
        c_url = url + job_url
        go_url.append(c_url)
try:
    name = '../bugs/loop_count.txt'
    fo = open(name, 'r')
    txt = fo.read()
    start = len(txt)
    fo.close()
except:
    print('没有历史文件,将从头开始进行数据爬虫')
all_count = len(go_url)
go_url = go_url[start:]

task = Manager.TaskManager(all_count, 20, go_url, start, city_codetoname, job_codetoname)
task.run()
task.complete()
