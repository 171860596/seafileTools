from FileOP import FileOP
from UrlApi import UrlApi
import time


def create_url():
    test = FileOP()
    account = test.get_account()
    dir_list, pwd_list, time_list = test.get_dir()
    tool = UrlApi(username=account["username"], password=account["password"], lib_token=account["token"])
    dir_repo_list = tool.createdir(dir_list)
    url_list = tool.create_url(dir_repo_list, pwd_list, time_list)
    test.save(url_list)
    time.sleep(1)
    print("finish")


if __name__ == "__main__":
    create_url()

