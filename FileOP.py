from urllib import request, parse
import json
import csv
import time, datetime
import logging


class FileOP:
    account_file = ""
    dir_file = ""
    save_file = ""
    err_file = ""
    del_file = ""

    def __init__(self, account_file="account.csv", dir_file="dir.csv", save_file="url.csv", err_file="err.csv", del_file="del.csv"):
        self.account_file = account_file
        self.dir_file = dir_file
        self.save_file = save_file
        self.err_file = err_file
        self.del_file = del_file

    def get_account(self):
        account = {}
        with open(self.account_file, "r") as f:
            reader = csv.reader(f)
            data = []
            for row in reader:
                data.append(row)
            account["username"] = data[1][0]
            account["password"] = data[1][1]
            account["token"] = data[1][2]
        return account

    def get_dir(self):
        dir_names = []
        passwords = {}
        times = {}
        with open(self.dir_file, "r") as f:
            reader = csv.reader(f)
            data = []
            for row in reader:
                break
            for row in reader:
                data.append(row)
            for i, row in enumerate(data):
                dir_name = parse.quote(row[0])
                dir_names.append(dir_name)
                passwords[dir_name] = row[1]
                times[dir_name] = row[2] + "+08:00"
        return dir_names, passwords, times

    def save(self, url_list):
        dir_list = []
        for dir_name in url_list:
            dir_list.append(dir_name)
        with open(self.save_file, "w") as f:
            csv_writer = csv.writer(f)
            data = [["dirName", "url"]]
            for i, dir_name in enumerate(dir_list):
                data.append([parse.unquote(dir_name), url_list[i]])
            csv_writer.writerows(data)

    def err(self, dir_name, err_type):
        with open(self.err_file, "a+") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([dir_name, err_type])

    def get_url(self):
        dir_names = []
        urls = {}
        with open(self.del_file, "r") as f:
            csv_reader = csv.reader(f)
            data = []
            for row in csv_reader:
                break
            for row in csv_reader:
                data.append(row)
            for i, row in enumerate(data):
                dir_name = row[0]
                dir_names.append(dir_name)
                urls[dir_name] = row[1]
        return dir_names, urls

    def log_index(self, operation, status):
        with open(self.log_file, "a+") as f:
            now = int(time.time())
            timeArray = time.localtime(now)
            otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
            csv_writer = csv.writer(f)
            csv_writer.writerow([operation, status, otherStyleTime])


if __name__ == "__main__":
    print("test")



