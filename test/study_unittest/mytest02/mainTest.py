# coding=utf-8
#设置编码，utf-8可支持中英文
#导入unittest模块
import unittest
from studyunittest.test.mytest02 import Baidu_Test
from studyunittest.test.mytest02 import Youdao_Test
'''
web测试用例：通过测试套件TestSuite来组装多个测试用例。
'''
suite = unittest.TestSuite()
suite.addTest(Baidu_Test.BaiduTest('test_baidu'))
suite.addTest(Youdao_Test.YoudaoTest('test_youdao'))

if __name__=='__main__':
    #执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)