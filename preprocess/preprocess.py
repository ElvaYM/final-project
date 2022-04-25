# if you already install bson, please  uninstall bson install pymongo
import bson # this package is from pymongo
import os
import json
from util import download_file, extract_data, print_schema
import pandas as pd

url = "http://ghtorrent-downloads.ewi.tudelft.nl/mongo-daily/mongo-dump-2019-06-30.tar.gz"

# download the zipped file from the original source
if os.getcwd().split("/")[-1] == "preprocess":
    os.chdir("/".join(os.getcwd().split("/")[:-1]))
file_name = download_file(url)
raw_data_path = "resources/raw_data/"
processed_data_path = "resources/data/"
schema_path = "resources/schema/"

if not os.path.exists(raw_data_path):
    extract_data(raw_data_path, file_name)

if not os.path.exists(processed_data_path):
    os.mkdir(processed_data_path)

if not os.path.exists(schema_path):
    os.mkdir(schema_path)

print("processing pull_request_comments.bson")
data_generator = bson.decode_file_iter(open(raw_data_path + "dump/github/pull_request_comments.bson", "rb"))
data = {}
for d in data_generator:
    if d["created_at"].split("T")[0] != "2019-06-30":
        continue
    data[d["id"]] = {"user_id": d["user"]["login"], "author_association": d["author_association"],
                     "created_at": d["created_at"], "body": d["body"], "url": d["html_url"], "repo": d["repo"]}   
with open("{}pull_request_comments.txt".format(schema_path), "w") as f:
    f.write("Total records: {} \nSchema: \n".format(len(data)))
    f.write(print_schema(d))   
    f.write("Example json:\n")
    d["_id"] = str(d["_id"])
    f.write(json.dumps(d, indent = 2))  

(pd.DataFrame
.from_dict(data,orient='index')
.sample(n=10**4, random_state=5293)
.to_csv(processed_data_path + "pull_request_comments.csv", index_label="id"))
print("successfully processed pull_request_comments.bson and stored it in {}".format(processed_data_path + "pull_request_comments.csv"))

data = {}
print("processing issue_comments.bson")
data_generator = bson.decode_file_iter(open(raw_data_path + "dump/github/issue_comments.bson", "rb"))
for d in data_generator:
    if d["created_at"].split("T")[0] != "2019-06-30":
        continue
    data[d["id"]] = {"user_id": d["user"]["login"], "author_association": d["author_association"],
                     "created_at": d["created_at"], "body": d["body"], "url": d["html_url"], "repo": d["repo"]}

with open("{}issue_comments.txt".format(schema_path), "w") as f:
    f.write("Total records: {} \nSchema: \n".format(len(data)))
    f.write(print_schema(d))   
    f.write("Example json:\n")
    d["_id"] = str(d["_id"])
    f.write(json.dumps(d, indent = 2))  
(pd.DataFrame
.from_dict(data,orient='index')
.sample(n=10**4, random_state=5293*2)
.to_csv(processed_data_path + "issue_comments.csv", index_label="id"))

print("successfully processed issue_comments.bson and stored it in {}".format(processed_data_path + "issue_comments.csv"))

print("processing commits.bson")
data_generator = bson.decode_file_iter(open(raw_data_path + "dump/github/commits.bson", "rb"))
data = {}
for d in data_generator:
    user = d["author"]["login"] if d["author"] else ""
    stats = d["stats"] if "stats" in d else ""
    if d["commit"]["committer"]["date"].split("T")[0] != "2019-06-30":
        continue
    data[d["sha"]] = {"user": user, "author": d["commit"]["author"]["name"],
                      "committer": d["commit"]["committer"]["name"],
                      "time": d["commit"]["committer"]["date"], 'message': d["commit"]["message"], 
                      "stats": stats, "url": d["html_url"]} 
with open("{}commits.txt".format(schema_path), "w") as f:
    f.write("Total records: {} \nSchema: \n".format(len(data)))
    f.write(print_schema(d))     
    f.write("Example json:\n")
    d["_id"] = str(d["_id"])
    f.write(json.dumps(d, indent = 2))  
(pd.DataFrame
.from_dict(data,orient='index')
.sample(n=10**4, random_state=5293*3)
.to_csv(processed_data_path + "commits.csv", index_label="sha"))
print("successfully processed commits.bson and stored it in {}".format(processed_data_path + "commits.csv"))