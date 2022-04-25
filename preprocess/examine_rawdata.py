import bson # this package is from pymongo
import os
import json
from utility import print_schema

filenames = [filename for filename in os.listdir("dump/github")if filename.split(".")[-1] == "bson"]
schema_path = "resources/schema/"
for filename in filenames:
    print("processing {}".format(filename))
    data_generator = bson.decode_file_iter(open("dump/github/{}".format(filename), "rb"))
    try:
        d = next(data_generator)
        with open("{}{}.txt".format(schema_path, filename.split(".")[0]), "w") as f:
            f.write("Total records: {} \nSchema: \n".format(len(list(data_generator)) + 1))
            f.write(print_schema(d))   
            f.write("Example json:\n")
            d["_id"] = str(d["_id"])
            f.write(json.dumps(d, indent = 2))  
    except:
        pass
    