
import time
from constants.error_message import CANNOT_EXECUTE_INPUT_CODE
from constants.error_code import BAD_REQUEST


class Excecutor:
    def __init__(self, code, test_cases):
        self.code = code
        self.test_cases = test_cases

    def execute_code_with_test_cases(self):
        results = []
        count_pass_cases = 0
        try:
            exec(self.code)
        except:
            raise Exception("{}: {}".format(BAD_REQUEST, CANNOT_EXECUTE_INPUT_CODE))
        for test_case in self.test_cases:
            params = test_case["input"]
            expected_output = test_case["expected_output"]
            start_time = time.time()
            try:
                actual_output = locals()["execute"](**params)
            except:
                raise Exception("{}: {}".format(BAD_REQUEST, CANNOT_EXECUTE_INPUT_CODE))
            end_time = time.time()
            case_output = {
                "input": params,
                "expected_output": expected_output,
                "execution_time": end_time-start_time,
                "result": "fail"
            }
            if str(actual_output) == expected_output:
                count_pass_cases += 1
                case_output["result"] = "pass"
            results.append(case_output)
        return results, count_pass_cases
