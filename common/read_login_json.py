import json

from config import BASE_PATH


def get_test_login_data():
    # 打开json文件
    with open(f'{BASE_PATH}/data/data_login.json', 'r', encoding='utf-8') as f:
        #json.load(f) 将 JSON 文件内容解析为 Python 对象
        data= json.load(f)
        data_list=[]
        # 遍历json数据
        for i in data:
            data_list.append((i.get('username'),
                             i.get('password'),
                              i.get('expect'),
                              i.get('type')))
    return data_list

if __name__ == '__main__':
    print(get_test_login_data())