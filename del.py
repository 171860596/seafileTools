from FileOP import FileOP
from UrlApi import UrlApi
from time import sleep


def del_url():
    test = FileOP()
    account = test.get_account()
    dir_list, url_list = test.get_url()
    tool = UrlApi(username=account["username"], password=account["password"], lib_token=account["token"])
    tool.del_url(dir_list, url_list)
    sleep(1)
    print("finish")


if __name__ == "__main__":
    del_url()
