import json
import redis
import os
import jsonschema
from jsonschema import validate
import boto3
import time

print('loading function')


def lambda_handler(event, context):
    with open('schema_for_daily_events.json', 'r') as file:
        schema = json.load(file)

    message = event['Records'][0]['Sns']['Message']
    json_msg = json.loads(message)
    print("Message from SNS::", json_msg)

    try:
        validate(instance=json_msg, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        err = "Given JSON data is InValid"
        return err

    redis_endpoint = os.environ['Redis_host']
    sns_topic = os.environ['sns_topic']
    try:
        redis_conn = redis.StrictRedis(host=redis_endpoint, port=6379, db=0)
        module_id = json_msg['moduleid']
        tx_attempts = int(json_msg['tx_attempts'])

        attempts = redis_conn.get(module_id)
        attempts = int.from_bytes(attempts, byteorder='big')
        print("attempts::", attempts)

        success_rate = 0
        if attempts!=0:
            success_rate = tx_attempts / attempts
            print("success rate:", success_rate)

    except:
        print("failed to connect to redis")
        return {
            'statusCode': 500
        }

    pub_msg = dict()
    pub_msg['moduleid'] = module_id
    pub_msg['timestamp'] = int(time.time())
    pub_msg['success_rate'] = success_rate

    client = boto3.client('sns')

    print("publishing.....")

    response = client.publish(
        TopicArn=sns_topic,
        Message=json.dumps({'default': json.dumps(pub_msg)}),
        MessageStructure='json')

    # Print out the response
    print("response::", response)

    return response