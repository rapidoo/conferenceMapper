import chalice
from chalice import NotFoundError
import boto3
from boto3.dynamodb.conditions import Key

from random import randint

app = chalice.Chalice(app_name="conference")
app.debug = True

dynamodb = boto3.resource("dynamodb")
conference_table = dynamodb.Table("conference")


@app.route("/conferenceMapper", methods=["GET"], cors=True)
def map():

    id = app.current_request.query_params.get('id')
    conf = app.current_request.query_params.get('conference')

    if id:
        print('request by id', id)
        exist_conf = get_conference_by_id(id)
        print(exist_conf)
        if exist_conf:
            return exist_conf
        else:
            raise NotFoundError("Id not exist")

    if conf:
        print('request by conf', conf)
        res_conf = get_id_by_conference(conf)
        newid = None
        if res_conf is not None:
            newid = res_conf['id']
        else:
            newid = randint(10000000, 99999999)
            while get_conference_by_id(f"newid"):
                newid = randint(100000, 999999)

        put_item(newid, conf)
        return {
            "message": "Successfully retrieved conference mapping",
            "id": int(newid),
            "conference": conf
        }

    print('FLB')


def put_item(id, conference):
    try:
        item = {
            "id": f"{id}",
            "conference": conference
        }
        p_resp = conference_table.put_item(Item=item)
        return p_resp
    except TypeError as e:
        print("Error: on", e)
        print(f"id: {id}")


def get_conference_by_id(id):
    try:
        resp = conference_table.query(
            KeyConditionExpression=Key("id").eq(id)
        )
        if resp['Count'] == 0:
            return False

        item = resp['Items'][0]
        return {
            "message": "Successfully retrieved conference mapping",
            "id": int(item['id']),
            "conference": item['conference']
        }
    except TypeError as e:
        print("Error: on", e)
        print(f"id: {id}")


def get_id_by_conference(conference):
    try:
        resp = conference_table.query(
            IndexName="conference-index", KeyConditionExpression=Key("conference").eq(conference)
        )
        if resp['Count'] == 0:
            return None
        return resp['Items'][0]
    except TypeError as e:
        print("Error: on", e)
        print(f"id: {id}")


#put_item(332423434, "Fred")
# print(get_conference_by_id("332423434"))
# get_id_by_conference("Fred")
