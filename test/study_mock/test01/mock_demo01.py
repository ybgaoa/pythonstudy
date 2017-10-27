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
        #通过Mock类模拟被调用的方法add()方法，return_value 定义add()方法的返回值。
        count.add = mock.Mock(return_value=13)
        #接下来，相当于在正常的调用add()方法，传两个参数8和5，然后会得到相加的结果13。然后，13的结果是我们在上一步就预先设定好的。
        result = count.add(8,5)
        #最后，通过assertEqual()方法断言，返回的结果是否是预期的结果13。
        self.assertEqual(result,13)


if __name__ == '__main__':
    unittest.main()