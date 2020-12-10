import time
from pymysql import connect

route_list = [
    # ('/index.html', index),
    # ('/center.html', center)
]


class SqlConnect:
    def __init__(self, database, user, password, host='localhost', port=3306, charset='utf8'):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.charset = charset

    def __enter__(self):
        self.conn = connect(host=self.host, port=self.port, database=self.database, user=self.user,
                            password=self.password, charset=self.charset)
        self.cur = self.conn.cursor()
        return self.conn, self.cur

    def __exit__(self, *args):
        self.cur.close()
        self.conn.close()


def router(path):
    def wrapper(func):
        route_list.append((path, func))

        def inner():
            result = func()
            return result

        return inner

    return wrapper


@router('/index.html')
def index():
    # 状态信息
    status = '200 OK'
    # 响应头信息
    response_header = [('Server', 'PWS /1.1')]
    with open('templates/index.html', 'r') as file:
        file_data = file.read()
    # web处理后的数据
    with SqlConnect(database='stock_db', user='root', password='zhd19980923') as (conn, cur):
        cur.execute("select * from info")
        items = cur.fetchall()
        data = ''
        for item in items:
            # noinspection SpellCheckingInspection
            data += f'''<tr>
                    <th>{item[0]}</th>
                    <th>{item[1]}</th>
                    <th>{item[2]}</th>
                    <th>{item[3]}</th>
                    <th>{item[4]}</th>
                    <th>{item[5]}</th>
                    <th>{item[6]}</th>
                    <th>{item[7]}</th>
                    <th><input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s"></th>
                </tr>'''

    # conn = connect(host='localhost', port=3306, database='stock_db', user='root',
    #                password='zhd19980923', charset='utf8')
    # cur = conn.cursor()
    # cur.execute("select * from info")
    # items = cur.fetchall()
    # data = ''
    # for item in items:
    #     data += f'''<tr>
    #             <th>{item[0]}</th>
    #             <th>{item[1]}</th>
    #             <th>{item[2]}</th>
    #             <th>{item[3]}</th>
    #             <th>{item[4]}</th>
    #             <th>{item[5]}</th>
    #             <th>{item[6]}</th>
    #             <th>{item[7]}</th>
    #             <th><input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s"></th>
    #         </tr>'''
    # cur.close()
    # conn.close()
    # data = str(items)
    # 返回数据
    response_body = file_data.replace('{%content%}', data)

    return status, response_header, response_body


@router('/center.html')
def center():
    # 状态信息
    status = '200 OK'
    # 响应头信息
    response_header = [('Server', 'PWS /1.1')]
    with open('templates/center.html', 'r') as file:
        file_data = file.read()
    # web处理后的数据
    with SqlConnect(database='stock_db', user='root', password='zhd19980923') as (conn, cur):
        cur.execute(
            'select i.code,i.short,i.chg,i.turnover,i.price,i.highs,note_info from focus inner join info i on '
            'focus.info_id = i.id;')
        items = cur.fetchall()
        data = ''
        for item in items:
            # noinspection SpellCheckingInspection
            data += f'''
            <tr>
                    <th>{item[0]}</th>
                    <th>{item[1]}</th>
                    <th>{item[2]}</th>
                    <th>{item[3]}</th>
                    <th>{item[4]}</th>
                    <th>{item[5]}</th>
                    <th>{item[6]}</th>
                    <th>
                        <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> 
                            <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 
                        </a>
                    </th> 
                    <th> <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s"></th>
            </tr>
            '''
    # conn = connect(host='localhost', port=3306, database='stock_db', user='root', password='zhd19980923',
    #                charset='utf8')
    # cur = conn.cursor()
    # cur.execute(
    #     'select i.code,i.short,i.chg,i.turnover,i.price,i.highs,note_info
    #     from focus inner join info i on focus.info_id = i.id;')
    # items = cur.fetchall()
    # data = ''
    # for item in items:
    #     data += f'''
    #     <tr>
    #             <th>{item[0]}</th>
    #             <th>{item[1]}</th>
    #             <th>{item[2]}</th>
    #             <th>{item[3]}</th>
    #             <th>{item[4]}</th>
    #             <th>{item[5]}</th>
    #             <th>{item[6]}</th>
    #             <th><a type="button" class="btn btn-default btn-xs" href="/update/%s.html">
    #             <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a></th>
    #             <th> <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s"></th>
    #     </tr>
    #     '''
    # cur.close()
    # conn.close()
    # 返回数据
    response_body = file_data.replace('{%content%}', data)

    return status, response_header, response_body


def notfound():
    # 状态信息
    status = '404 Not Found'
    # 响应头信息
    response_header = [('Server', 'PWS /1.1')]
    # web处理后的数据
    data = 'Not Found'
    # 返回数据
    return status, response_header, data


# 处理动态资源请求
def handle_request(env):
    # 获取动态的资源请求路径
    request_path = env["request_path"]
    print('动态资源请求的地址是：', request_path)
    # 判断当前动态资源请求路径，提供指定函数解析
    # if request_path == '/index.html':
    #     result = index()
    #     return result
    # elif request_path == '/center.html':
    #     result = center()
    #     return result
    # else:
    #     # 如果没找对应资源则返回404
    #     result = notfound()
    #     return result

    #  路由匹配
    for path, func in route_list:
        if request_path == path:
            result = func()
            return result

    result = notfound()
    return result
