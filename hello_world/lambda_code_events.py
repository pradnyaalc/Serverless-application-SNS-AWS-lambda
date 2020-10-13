import redis
import os
import json
import jsonschema
from jsonschema import validate

print('loading function')


def lambda_handler(event, context):
    with open('schema_for_weekly_messages.json', 'r') as file:
        schema = json.load(file)

    message = event['Records'][0]['Sns']['Message']
    json_msg = json.loads(message)

    print("Message from SNS event source::", json_msg)

    try:
        validate(instance=json_msg, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        err = "Given JSON data is InValid"
        return err

    redis_endpoint = os.environ['Redis_host']
    try:
        redis_conn = redis.StrictRedis(host=redis_endpoint, port=6379, db=0)
        module_id = json_msg['moduleid']
        attempts = int(json_msg['attempts'])
        redis_conn.set(module_id, attempts)
        print(module_id + "::" + str(attempts))

    except:
        print("failed to connect to redis")
        return {
            'statusCode': 500
        }

    return message