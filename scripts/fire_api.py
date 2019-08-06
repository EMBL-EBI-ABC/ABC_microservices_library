"""This script will provide proxy to work with Fire API"""
import json
import subprocess
import sys
from decouple import config
from argparse import ArgumentParser


class FireAPI:
    def __init__(self, username, password, archive_name, api_endpoint, filename,
                 path):
        self.username = username
        self.password = password
        self.archive_name = archive_name
        self.api_endpoint = api_endpoint
        self.filepath = filename
        self.filename = filename.split('/')[-1]
        self.path = path

    def upload_object(self):
        """This function will upload object to Fire database"""
        cmd = f"curl {self.api_endpoint}/objects " \
            f"-F file=@{self.filepath} " \
            f"-H 'x-fire-path: {self.path}/{self.filename}' " \
            f"-H 'x-fire-publish: true' " \
            f"-u {self.username}:{self.password}"
        proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        print("Public link is:")
        self.get_public_link()

    def get_public_link(self):
        """This function will return public link to uploaded file"""
        link = f"{self.api_endpoint}/public/" \
            f"{self.archive_name}/{self.path}/{self.filename}"
        print(link)

    def list_objects(self):
        """This function will list all objects in archive"""
        cmd = f"curl {self.api_endpoint}/objects " \
            f"-u {self.username}:{self.password}"
        proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        out = json.loads(out.decode('utf-8'))
        print(f"{'File path':150}\t{'Published':10}\t{'FireOId':30}")
        for file in out:
            if file['filesystemEntry']:
                print(f"{file['filesystemEntry']['path']:150}\t"
                      f"{file['filesystemEntry']['published']}\t"
                      f"{file['fireOid']:30}")

    def delete_objects(self, fire_id):
        """This function will delete object from Fire database"""
        cmd = f"curl {self.api_endpoint}/objects/{fire_id} " \
            f"-u {self.username}:{self.password} " \
            f"-X DELETE"
        proc = subprocess.Popen([cmd], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        self.list_objects()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-a", "--action", dest="action", help="Which function to use, could be "
                                              "'upload_object', "
                                              "'get_public_link', "
                                              "'list_objects' and "
                                              "'delete_object'")
    parser.add_argument(
        "-f", "--filename", dest="filename", help="Path to the file you want "
                                                  "to upload to Fire API")
    parser.add_argument(
        "-p", "--path", dest="path", help="Path that will be used for public "
                                          "access inside Fire API")
    parser.add_argument(
        "-id", "--fireOId", dest="id",
        help="Fire API id of object (optional, will be used only to delete "
             "object)")
    args = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    fire_api_object = FireAPI(config('USERNAME'), config('PASSWORD'),
                              config('ARCHIVE_NAME'), config('API_ENDPOINT'),
                              args.filename, args.path)
    if args.action == 'list_objects':
        fire_api_object.list_objects()
    elif args.action == 'upload_object':
        fire_api_object.upload_object()
    elif args.action == 'get_public_link':
        fire_api_object.get_public_link()
    elif args.action == 'delete_object':
        fire_api_object.delete_objects(args.id)
    else:
        print("Please provide correct action, it could only be "
              "'upload_object', 'get_public_link', 'list_objects', "
              "'delete_object'")
