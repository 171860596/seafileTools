from urllib import request, parse
import json
import time
from FileOP import FileOP
import logging
import logging.handlers
from tqdm import tqdm


class UrlApi:
    auth_token = ""
    lib_token = ""
    url = ""

    def __init__(self, username, password, lib_token, url="box.nju.edu.cn"):
        # 初始化设置
        logging.basicConfig(level=logging.INFO, format='%(asctime)s|%(name)-12s: %(levelname)-8s %(message)s')
        # 创建
        self.logger = logging.getLogger(username)
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        handler1 = logging.FileHandler("base-log.log", mode="a+")
        handler1.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s|%(name)-12s+ %(levelname)-8s++%(message)s')
        handler1.setFormatter(formatter)

        handler2 = logging.StreamHandler()
        handler2.setLevel(logging.ERROR)

        self.logger.addHandler(handler1)
        self.logger.addHandler(handler2)

        self.url = url
        api_url = 'https://' + self.url + '/api2/auth-token//'
        data = {"username": username, "password": password}
        data = parse.urlencode(data).encode('utf-8')
        headers = {"Accept": "application/json"}
        req = request.Request(api_url, headers=headers, data=data)
        try:
            resp = request.urlopen(req)
            # TODO: 如果响应失败
            if resp.status != 200:
                self.logger.error("wrong username or password!")
            page = resp.read().decode('utf-8')
            self.auth_token = json.loads(page)["token"]
            self.lib_token = lib_token
            self.logger.info("successfully login")
        except:
            self.logger.error("can't log in the account!")
            exit()


    # TODO: 一一创建list里的文件夹
    def createdir(self, dir_list):
        dir_repo_id = {}
        print("Start")
        for i in tqdm(range(0, len(dir_list))):
            dir_name = dir_list[i]
            api_url = 'https://' + self.url + '/api/v2.1/via-repo-token/dir/?path=/'+dir_name
            data = {"operation": "mkdir"}
            data = parse.urlencode(data).encode('utf-8')
            headers = {'Authorization': 'Token '+self.lib_token, "Accept": "application/json"}
            req = request.Request(api_url, headers=headers, data=data)
            try:
                resp = request.urlopen(req)
                # TODO: 如果响应失败
                if resp.status != 200:
                    self.logger.error("create " + parse.unquote(dir_name) + "\'s dir error, wrong response code:" + str(resp.status))
                page = resp.read().decode('utf-8')
                dir_repo_id[dir_name] = json.loads(page)["repo_id"]
                self.logger.info("create dir: "+parse.unquote(dir_name))
            except:
                self.logger.error("create " + parse.unquote(dir_name) + "\'s dir error, can't open url")
        return dir_repo_id

    # TODO: 一一创建对应密码、时间期限的共享链接
    def create_url(self, dir_repo_id, pwd_list, time_list):
        url_list = {}
        dir_list = []
        for dir_name in dir_repo_id:
            dir_list.append(dir_name)
        for i in tqdm(range(0, len(dir_list))):
            dir_name = dir_list[i]
            api_url = 'https://' + self.url + '/api/v2.1/upload-links/'
            data = {"path": "/"+parse.unquote(dir_name)+"/", "repo_id": dir_repo_id[dir_name], "password": pwd_list[dir_name], "expiration_time": time_list[dir_name]}
            data = parse.urlencode(data).encode('utf-8')
            headers = {'Authorization': 'Token ' + self.auth_token, "Accept": "application/json"}
            req = request.Request(api_url, headers=headers, data=data)
            try:
                resp = request.urlopen(req)
                # TODO: 如果响应失败
                if resp.status != 200:
                    self.logger.error("create " + parse.unquote(dir_name) + "\'s uplink url error, wrong response code:" + str(resp.status))
                page = resp.read().decode('utf-8')
                url_list[parse.unquote(dir_name)] = json.loads(page)["link"]
                self.logger.info("create dir: " + parse.unquote(dir_name) + "'s uplink url")
            except:
                self.logger.error("create " + parse.unquote(dir_name) + "\'s uplink url error, can't open url")
        return url_list

    # TODO: 一一删除对应的url
    def del_url(self, dir_list, url_list):
        for i in tqdm(range(0, len(dir_list))):
            dir_name = dir_list[i]
            api_url = 'https://' + self.url + '/api/v2.1/upload-links/'+ url_list[dir_name][-21:-1] + "/"
            headers = {'Authorization': 'Token '+ self.auth_token}
            req = request.Request(api_url, headers=headers, method="DELETE")
            try:
                resp = request.urlopen(req)
                # TODO: 如果响应失败
                if resp.status != 200:
                    self.logger.error("del " + api_url + " error, wrong response code:" + str(resp.status))
                page = resp.read().decode('utf-8')
                if (json.loads(page)["success"]) != True:
                    self.logger.warning("del " + api_url + " warning, can't del url")
                self.logger.info("successfully del " + api_url)
            except:
                # TODO log
                self.logger.error("del " + api_url + " error, can't open url")