# coding=utf-8
#设置编码，utf-8可支持中英文

import mock
import unittest

from modular import Count

# test Count class
class TestCount(unittest.TestCase):

    def test_add(self):
        #首先，调用被测试类Count()
        count = Count()
        #side_effect参数和return_value是相反的。它给mock分配了可替换的结果，覆盖了return_value。
        ## 简单的说，一个模拟工厂调用将返回side_effect值，而不是return_value。
        #所以，设置side_effect参数为Count类add()方法，那么return_value的作用失效。
        count.add = mock.Mock(return_value=13, side_effect=count.add)
        #这次将会真正的调用add()方法，得到的返回值为16（8+8）。通过print打印结果。
        result = count.add(8, 8)
        print(result)
        #检查mock方法是否获得了正确的参数。
        count.add.assert_called_with(8, 8)
        ##最后，通过assertEqual()方法断言，返回的结果是否是预期的结果16。
        self.assertEqual(result, 16)


if __name__ == '__main__':
    unittest.main()