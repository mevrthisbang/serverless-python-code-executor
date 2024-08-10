from constants.error_code import NOT_FOUND
from constants.error_message import NOT_FOUND_CHALLENGE
import boto3

def lambda_handler(event, context):
    challenge_id = event.get("challengeId")
    dynamodb = boto3.resource("dynamodb")
    challenge_table = dynamodb.Table("code_challenge")
    response = challenge_table.get_item(
        Key={
            "challenge_id": challenge_id
        },
        AttributesToGet=["input_code", "requirement"]
    )
    if "Item" not in response:
        raise Exception("{}:{}".format(NOT_FOUND, NOT_FOUND_CHALLENGE))
    code_challenge = response.get("Item")
    return code_challenge