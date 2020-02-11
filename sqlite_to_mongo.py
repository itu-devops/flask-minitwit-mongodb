import csv
from datetime import datetime
from pymongo import MongoClient


client = MongoClient("localhost", 27017)
db = client.test

print("use test;")
print("db.dropDatabase();")

with open("user.csv") as fp:
    csv.reader(fp)
    csvreader = csv.reader(fp, delimiter=",", quotechar='"')

    next(csvreader)

    for row in csvreader:

        print(
            f"""db.user.insertOne({{'user_id': {int(row[0])},
                  'username': "{row[1]}",
                  'email': "{row[2]}",
                  'pw_hash': "{row[3]}"}});"""
        )

        db.user.insert_one(
            {
                "user_id": int(row[0]),
                "username": row[1],
                "email": row[2],
                "pw_hash": row[3],
            }
        )

with open("message.csv") as fp:
    csv.reader(fp)
    csvreader = csv.reader(fp, delimiter=",", quotechar='"')

    next(csvreader)

    for row in csvreader:

        user = db.user.find_one(
            {"user_id": int(row[1])}, {"email": 1, "username": 1}
        )

        print(
            f"""db.message.insertOne({{"author_id": {user["_id"]},
                    "email": "{user["email"]}",
                    "username": "{user["username"]}",
                    "text": "{row[2]}",
                    "pub_date": {int(row[3])}}});"""
        )

        db.message.insert_one(
            {
                "author_id": user["_id"],
                "email": user["email"],
                "username": user["username"],
                "text": row[2],
                "pub_date": datetime.utcfromtimestamp(int(row[3])),
            }
        )

with open("follower.csv") as fp:
    csv.reader(fp)
    csvreader = csv.reader(fp, delimiter=",", quotechar='"')

    next(csvreader)

    for who, whom in csvreader:

        who_doc = db.user.find_one({"user_id": int(who)})
        whom_doc = db.user.find_one({"user_id": int(whom)})

        print(
            f"""db.follower.updateOne({{"who_id": {who_doc["user_id"]}}},
            {{"$push": {{"whom_id": {whom_doc["user_id"]}}}}}, upsert=True);"""
        )

        db.follower.update_one(
            {"who_id": who_doc["user_id"]},
            {"$push": {"whom_id": whom_doc["user_id"]}},
            upsert=True,
        )


# use test
# switched to db test
# > db.dropDatabase();

# mongodump
