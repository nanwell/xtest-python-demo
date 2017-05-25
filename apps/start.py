import unittest

import time

from apps.base.units import BaseApi
from apps.xtest_cfg import project_id, app_id, app_key
from apps.hello_test import MyTestDemo
from xtest.sdk import dict_encode_test_results, TestReport, get_case_list_from_cls

if __name__ == '__main__':
    # 1. 使用Pyunit框架可以构建一个如下的测试结果字典
    # 2. 然后上传到服务器即可

    start_time = time.time()  # 测试启动的时刻点

    test_case_list = get_case_list_from_cls([
        MyTestDemo,
        BaseApi,
        # todo 在项目里面再定义别的测试类，然后装载进来即可
    ])  # 装载测试用例

    test_suit = unittest.TestSuite()
    test_suit.addTests(test_case_list)  # 使用测试套件并打包测试用例

    test_result = unittest.TextTestRunner().run(test_suit)  # 运行测试套件，并返回测试结果

    # 下面的部分，全部是和xtest系统进行对接的内容
    total_time = time.time() - start_time  # 测试过程整体的耗时
    test_res_dict = dict_encode_test_results(
        test_result,
        run_time=total_time,
        pro_id=project_id,
        pro_version='2.17.5.5.1'  # 当前被测试的系统的版本号,依据目前系统的信息，如果服务端提供接口，则可以做成自动化的
    )

    # 下面的内容是将测试报告的结果上传到服务器
    test_report = TestReport()
    auth_res = test_report.get_api_auth(
        app_id=app_id,
        app_key=app_key
    )
    if auth_res:
        test_report.post_unit_test_data(test_res_dict)
    else:
        print('auth error...')