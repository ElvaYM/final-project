import urllib.request
import datetime
import os
import tarfile

def convert_size(byte):
    kb = byte / 1024
    if kb < 1024:
        return str(round(kb, 2)) + "kb"
    mb = kb / 1024
    if mb < 1024:
        return str(round(mb, 2)) + "mb"
    gb = mb / 1024
    if gb < 1024:
        return str(round(gb, 2)) + "gb"
# download the zipped file from url
def download_file(url):
    # extract the file from the url
    file_name = url.split("/")[-1]
    # if the file is already downloaded
    if os.path.exists(file_name):
        print("{} is already downloaded!".format(file_name))
        return file_name
    
    connection = urllib.request.urlopen(url)
    info = connection.info()
    file_size = int(info["Content-Length"])

    file = open(file_name, 'wb')

    print("Downloading: %s Bytes: %s" % (file_name, file_size))

    file_size_dl = 0
    block_sz = 8192
    start_time = datetime.datetime.now()
    # provide a progress bar
    while True:
        # read 8kb block
        buffer = connection.read(block_sz)
        if not buffer:
            break
        downloaded_per = (file_size_dl / file_size) 
        used_time = datetime.datetime.now() - start_time
        needed_time = (1 - downloaded_per) * used_time / downloaded_per if downloaded_per != 0 else "NA"
        file_size_dl += len(buffer)
        file.write(buffer)
        
        status = "downloaded_size:{}, percentage: {:.2f}% used time/needed time: {}/{}".format(convert_size(file_size_dl), 
        downloaded_per * 100, used_time, needed_time)

        print(status, end='\r')

    file.close()

    return file_name

def extract_data(raw_data_path, file_name):
    prefix_path = "dump/github/"
    extracted_files = ["issue_comments.bson", "pull_request_comments.bson", "commits.bson"]
    file =  tarfile.open(file_name)
    for file in extracted_files:
        if os.path.exists(os.path.join(raw_data_path, prefix_path, file)):
            continue
        print("extracting {}...".format(file))
        file.extract(os.path.join(prefix_path, file), raw_data_path)


        

def print_schema(_json: dict) -> str:
    def print_schema_helper(data: dict, indent: int, result):
        for key, value in data.items():
            result += indent * " " + "|-- {}:\t".format(key)
            if isinstance(value, dict):
                result += "\n"
                result = print_schema_helper(value, indent + 5, result)
            else: 
                result += str(type(value)) + "\n"
        return result

    result = print_schema_helper(_json, 1, "root: \n")
    return result