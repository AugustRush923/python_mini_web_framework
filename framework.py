import time

route_list = [
    # ('/index.html', index),
    # ('/center.html', center)
]


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
    data = time.ctime()
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
    data = time.ctime()
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
    else:
        result = notfound()
        return result
