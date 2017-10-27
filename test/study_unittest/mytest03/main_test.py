# coding=utf-8
#设置编码，utf-8可支持中英文

import unittest
import HTMLTestRunner
import time


def creatsuite():
    testunit = unittest.TestSuite()
    # 定义测试文件查找的目录
    test_dir = 'D:/develop/PyCharm-workspace/pythonstudy/studyunittest/test/mytest03'
    # 定义 discover 方法的参数
    discover = unittest.defaultTestLoader.discover(test_dir,
                                                   pattern='test_*.py',
                                                   top_level_dir=None)
    # discover 方法筛选出来的用例，循环添加到测试套件中
    for test_suite in discover:
        for test_case in test_suite:
            testunit.addTests(test_case)
            print testunit
    return testunit


alltestnames = creatsuite()
if __name__ == '__main__':
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = 'C:\\Users\\ybgaoa\\Downloads\\' + now + 'result.html'
    fp = file(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=u'测试报告',
        description=u'用例的执行情况')

    runner.run(alltestnames)
    fp.close()