import boto3
import json
import _functools
import uuid
from datetime import datetime
from flask import Blueprint, request
from flask_restful import Resource, reqparse, abort
from botocore.exceptions import ClientError
import hashlib

bp = Blueprint('scrap_book', __name__, url_prefix='/scrap_book')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ScrapBook')


def hash_sha256(value):
    return hashlib.sha3_256(value.encode()).hexdigest()


def get_or_abort_404(hash_key):
    try:
        response = table.get_item(Key={'hash_key': hash_key})
        item = response.get('Item')
        if not item:
            abort(404, message="Not found")
        else:
            return item
    except ClientError as e:
        abort(e.response['ResponseMetadata']['HTTPStatusCode'], message=e.response['Error'])


class Content(Resource):
    def get(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('key')
        # args = parser.parse_args()
        # hash_key = hash_sha256(args['key'])
        key = request.args['key']
        hash_key = hash_sha256(key)

        item = get_or_abort_404(hash_key)

        return {'response': item}, 200

    # def post(self):
    #     value = request.form['value']
    #     response = table.put_item(
    #         Item={
    #             # 'uuid': str(uuid.uuid4()),
    #             'hash_key': '',
    #             'value': value,
    #             # 'add_dt': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    #         }
    #     )
    #
    #     return {'response': response['ResponseMetadata']}, 201

    def put(self):
        # uuid = request.form['uuid']
        # title = request.form['title']
        # print(request.data)
        key = request.form['key']
        content = request.form['content']

        response = table.update_item(
            Key={
                'hash_key': hash_sha256(key)
            },
            UpdateExpression="set content=:c, origin_key=:ok",
            ExpressionAttributeValues={
                ':c': content,
                ':ok': key,
            },
            ReturnValues="UPDATED_NEW",
        )
        return {'response': response['ResponseMetadata']}, 201

    def delete(self):
        key = request.form['key']
        response = table.delete_item(
            Key={
                'hash_key': hash_sha256(key)
            },
        )
        return {'response': response['ResponseMetadata']}, 204

# @bp.route('', methods=('GET', 'POST'))
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#
#         response = table.put_item(
#             Item={
#                 'UUID': str(uuid.uuid4()),
#                 'Title': title,
#                 'content': 'test',
#                 'add_dt': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#             }
#         )
#
#         return {'response': response['ResponseMetadata']}
#     else:
#         pass
