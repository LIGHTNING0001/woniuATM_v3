# -*- coding: utf-8 -*-

"""
数据模型层
实体：Account, Atm
Account : username, password, card_id, balance, today_money
Atm: a_id, version, a_balance
"""
import types
from functools import wraps


class Atm:

    def __init__(self, a_id, version, a_balance):
        self.__a_id = a_id
        self.__version = version
        self.__a_balance = a_balance

    @property
    def a_id(self):
        return self.__a_id

    @a_id.setter
    def a_id(self, value):
        if isinstance(self.__a_id, str):
            self.__a_id = value
        else:
            print("error：输入类型与预设类型不一致")


class Account:

    def __init__(self, username, password, card_id, balance, today_money):
        self.__username = username
        self.__password = password
        self.__card_id = card_id
        self.__balance = balance
        self.__today_money = today_money


#
# def a_new_decorator(a_func):
#
#     def wrapTheFunction():
#         print("I am doing some boring work before executing a_func()")
#
#         a_func()
#
#         print("I am doing some boring work after executing a_func()")
#
#     return wrapTheFunction
#
#
# @a_new_decorator
# def a():
#     print('正在处理')
#
# a()


import time


# 装饰器
def log(*, content='', path='./../data/logs.txt'):
    def func_decorator(func):
        @wraps(func)
        def wrap_function(username, money):
            mgs = ''
            flag = False
            if func(username, money):
                msg = '成功'
                flag = True
            else:
                msg = '失败'
            logs = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + \
                   '\t =====> {0} {1} {2} {3}'.format(username, content, money, msg)
            with open(path, 'a') as f:
                f.write(logs + '\r\n')
            return flag

        return wrap_function

    return func_decorator


def log_1(*, arg1='who', content='do',  arg2='things', path='./../data/logs.txt'):
    def func_decorator(func):
        @wraps(func)
        def wrap_function(*args, **kargs):
            mgs = ''
            flag = False
            if func(*args, **kargs):
                msg = '成功'
                flag = True
            else:
                msg = '失败'
            logs = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + \
                   '\t =====> {0} {1} {2} {3}'.format(arg1, content, arg2, msg)
            with open(path, 'a') as f:
                f.write(logs + '\r\n')
            return flag

        return wrap_function

    return func_decorator


# 取款功能，谁在哪台ATM机上取了多少钱
@log(content='取款')
def draw(username, money):
    """ 这是一个取款功能 """
    if True:
        return True
    else:
        return False


@log(content='存款')
def deposit(username, money):
    """ 这是一个存款功能 """
    if True:
        return True
    else:
        return False


@log_1(arg1='test1', content='转账', arg2=100, path='./../data/logs_1.txt')
def transfer():
    if True:
        return True
    else:
        return False


transfer()


class Profiled:
    def __init__(self, func):
        wraps(func)(self)
        self.ncalls = 0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.__wrapped__(*args, **kwargs)

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


@Profiled
def add(x, y):
    return x + y


print(add(3, 4))
print(add(4, 5))


# print(draw.__doc__)
# print(draw('test01', 1000))
# print(deposit('test01', 100))

if __name__ == '__main__':
    pass
    # deposit()
    # atm = Atm('sichuan_001', 'v1', 1000000)

# import time
# print(time.localtime())
# st_time = time.localtime()
# print(st_time.tm_year)
# print(st_time.tm_mon)
# print(st_time.tm_hour)












