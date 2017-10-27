# coding=utf-8
#设置编码，utf-8可支持中英文

from mock import patch
import unittest
import function

class MyTestCase(unittest.TestCase):
    """
    patch()装饰/上下文管理器可以很容易地模拟类或对象在模块测试。
    在测试过程中，您指定的对象将被替换为一个模拟（或其他对象），并在测试结束时还原。
　　这里模拟function.py文件中multiply()函数。
    在定义测试用例中，将mock的multiply()函数（对象）重命名为 mock_multiply对象。
    """
    @patch("function.multiply")
    def test_add_and_multiply(self, mock_multiply):
        x = 3
        y = 5
        #设定mock_multiply对象的返回值为固定的15。
        mock_multiply.return_value = 15
        #在此之前已经模拟function文件中multiply方法的返回值为15，因此下面执行过程中addition, multiple的值分别是8和15
        addition, multiple = function.add_and_multiply(x, y)
        #检查ock_multiply方法的输入参数是否与上面方法调用时候function文件中multiply方法的输入参数一致。
        mock_multiply.assert_called_once_with(3, 5)

        self.assertEqual(8, addition)
        self.assertEqual(15, multiple)


if __name__ == "__main__":
    unittest.main()