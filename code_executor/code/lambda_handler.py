from executor import Excecutor
from constants.error_code import BAD_REQUEST, NOT_FOUND
from constants.error_message import INVALID_INPUT_CODE, NOT_FOUND_CHALLENGE
import boto3

def lambda_handler(event, context):
    input_code = event.get("inputCode")
    if not input_code:
        raise Exception("{}: {}".format(BAD_REQUEST, INVALID_INPUT_CODE))
    challenge_id = event.get("challengeId")
    dynamodb = boto3.resource("dynamodb")
    challenge_table = dynamodb.Table("code_challenge")
    response = challenge_table.get_item(
        Key={
            "challenge_id": challenge_id
        },
        AttributesToGet=["test_cases"]
    )
    if "Item" not in response:
        raise Exception("{}:{}".format(NOT_FOUND, NOT_FOUND_CHALLENGE))
    test_cases = response.get("Item")["test_cases"]
    executor = Excecutor(input_code, test_cases)
    test_cases_results, count_pass_cases = executor.execute_code_with_test_cases()
    result = {
        "passCases": count_pass_cases,
        "numberOfTestCases": len(test_cases),
        "results": test_cases_results
    }
    return result