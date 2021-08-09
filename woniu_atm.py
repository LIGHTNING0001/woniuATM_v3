# -*- coding: utf-8 -*-
import time
from typing import TextIO

import pymysql

# 保存账户信息 登录状态
account = {'name': '', 'card_id': '', 'balance': 0, 'today_money': 0}

# 定义最大取款金额
MAX_MONEY = 5000.00

# 定义最大存款金额
MAX_DEPOSIT = 100000

# 定义最大转账金额
MAX_TRANSFER = 20000

# 最小金额
MIN_MONEY = 0.0

# 初始化值
INIT_VALUE = -1

# 确认
ACK = 'yes'

# 取消
NO = 'no'

# 用户文件
user_path = './data/userinfo.txt'

# 流水文件
log_data = './data/logs.txt'

# 单日取款最高金额
TODAY_MONEY = 20000

# 数据库连接
conn = pymysql.connect(user='woniu', password='123456', database='woniu_atm', charset='utf8')
cursor = conn.cursor()


def welcome():
    print('*' * 20, '欢迎来到woniuATM', '*' * 20)
    print('*' * 20, '请选择操作菜单', '*' * 20)
    print('*' * 10, '1. 注册   2. 登录  3. 退卡', '*' * 10)


def main_menu():
    print('*' * 20, '请选择操作菜单', '*' * 20)
    print('1. 查询    2. 取款   3. 存款   4. 转账   5. 流水   6. 返回   7. 退卡')


def sign_up():
    """ 注册"""
    card_id = ''
    flag = False
    for i in range(3):
        card_id = input('请输入卡号：')
        if len(card_id) == 0:
            print('卡号不能为空')
            print(f'你还有{2 - i}次机会')
            continue
        else:
            sql = f'select count(1) from account where card_id="{card_id}"'
            cursor.execute(sql)
            result = cursor.fetchone()
            if result[0] == 1:
                print('卡号已存在')
            else:
                flag = True
                break
    if not flag:
        return False
    end = 0
    name = input('请输入用户名：')
    while len(name) == 0:
        end += 1
        print('用户名不能为空')
        name = input('请输入用户名：')
        if end >= 3:
            print('输入次数超过3次')
            return False
    end = 0
    password = input('请输入密码：')
    while len(password) == 0:
        end += 1
        print('密码不能为空')
        password = input('请输入密码：')
        if end >= 3:
            print('输入次数超过3次')
            return False
    balance = 0
    sql = f'insert into account(name, password, card_id, balance) \
          values ("{name}", "{password}", "{card_id}", "{balance}")'
    cursor.execute(sql)
    conn.commit()
    print('注册成功')


def login():
    """登录"""
    for i in range(3):
        username = input('请输入用户名：')
        password = input('请输入密码：')
        sql = f'select name, password, card_id, balance from account where name="{username}" and password="{password}"'
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            account['name'] = result[0]
            account['password'] = result[1]
            account['card_id'] = result[2]
            account['balance'] = result[3]
            sql = f'update account set today_money = 0 where card_id = {result[2]}'
            cursor.execute(sql)
            conn.commit()
            print('恭喜你登录成功')
            return True
        else:
            print('用户名不存在或密码错误')
        print(f'登录失败，你还有{2 - i}次机会')
    return False


def logout():
    """退出登录"""
    print('退卡成功')
    exit(0)


def show_info():
    """查询个人用户"""
    print(f'用户名：{account.get("name")}')
    print(f'密码：{account.get("password")}')
    print(f'卡号：{account.get("card_id")}')
    print(f'余额：{account.get("balance"):.2f}')
    print(f'单日取款金额：{account.get("today_money")}')


def draw():
    """ 取款"""
    if account['today_money'] >= TODAY_MONEY:
        print(f'您的当日取款金额已经达到最高限度{TODAY_MONEY}')
        return False
    money = input('请输入取款金额：')
    if not money.isdecimal():
        print('输入的金额只能是正整数')
        return False
    money = int(money)
    if money % 100 != 0:
        print('输入金额只能是100的倍数')
        return False
    if money <= MIN_MONEY:
        print('输入的金额必须大于零')
        return False
    if money > MAX_MONEY:
        print(f'最大取款金额为{MAX_MONEY}')
        return False
    if account.get('balance') < money:
        print('余额不足')
        return False

    print(f'您输入的取款金额为：{money}')

    end = 0
    while True:
        ack = input('是否继续进行，请输入yes/no：')
        if ack == ACK:
            break
        if ack == NO:
            return False
        end += 1
        if end >= 3:
            print('您的输入次数超过3次，取款失败')
            return False
    account['balance'] -= money
    account['today_money'] += money
    sql = f'update account set balance = {account["balance"]}, today_money = {account["today_money"]} \
          where card_id = {account["card_id"]}'
    cursor.execute(sql)
    conn.commit()
    print(f'取款成功，你的余额为：{account["balance"]}')
    f = ''
    try:
        f = open('./data/logs.txt', 'a')
        log_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '=======' + f'取款: {money}'
        f.writelines(log_str + '\n')
    except:
        print('打开日志文件异常')
    finally:
        f.close()
    return True


def deposit():
    """ 存款 """
    while True:
        money = input('请输入存款金额：')
        if not money.isdecimal():
            print('输入的金额只能是正整数')
            continue
        money = int(money)
        if money % 100 != 0:
            print('输入金额只能是100的倍数')
            continue
        if money <= MIN_MONEY:
            print('输入的金额必须大于零')
            continue
        if money > MAX_DEPOSIT:
            print(f'最大存款金额为：{MAX_DEPOSIT}')
        print(f'您的存款金额为：{money}')
        end = 0
        while True:
            ack = input('是否继续进行，请输入yes/no：')
            if ack == ACK:
                break
            if ack == NO:
                return False
            end += 1
            if end >= 3:
                print('您的输入次数超过3次，存款失败')
                return False
        account['balance'] += money
        sql = f'update account set balance = {account["balance"]} where card_id = {account["card_id"]}'
        cursor.execute(sql)
        conn.commit()
        print(f'存款成功，你的余额为：{account["balance"]}')
        f = ''
        try:
            f = open('./data/logs.txt', 'a')
            log_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '=======' + f'存款: {money}'
            f.writelines(log_str + '\n')
        except:
            print('打开日志文件异常')
        finally:
            f.close()
        return True


def transfer():
    """ 转账 """
    flag = False
    to_username = ''
    transfer_money = ''
    for i in range(3):
        card_id = input('请输入转账的卡号：')
        sql = f'select name, card_id from account where card_id = {card_id}'
        cursor.execute(sql)
        result = cursor.fetchone()
        to_username = result[0]
        if result:
            print(f'你好转账的用户名：{to_username}， 卡号：{result[1]}')
            flag = True
            break
        else:
            print('不存在该用户')
        print(f'你还有{2 - i}次机会')
    if not flag:
        return False
    flag = False
    for i in range(3):
        transfer_money = input('请输入转账金额：')
        if not transfer_money.isdecimal():
            print('输入的金额只能是数字')
            print(f'你还有{2 - i}次机会')
            continue
        transfer_money = int(transfer_money)
        if transfer_money <= MIN_MONEY:
            print('输入的金额必须大于零')
            print(f'你还有{2 - i}次机会')
            continue
        if transfer_money > MAX_TRANSFER:
            print('最大转账金额为20000')
            print(f'你还有{2 - i}次机会')
            continue
        if transfer_money > account.get('balance'):
            print(f'你还有{2 - i}次机会')
            print('余额不足')
            continue
        flag = True
        break
    if not flag:
        return False
    sql = f'update user set balance = {transfer_money} where card_id = {account["card_id"]}'
    cursor.execute(sql)
    cursor.commit()
    print(f'转账成功，向{to_username}转账{transfer_money}')
    f = ''
    try:
        f = open('./data/logs.txt', 'a')
        log_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '=======' + f'向{to_username}转账{transfer_money}'
        f.writelines(log_str + '\n')
    except:
        print('打开日志文件异常')
    finally:
        f.close()


def check_welcome_id():
    while True:
        menu_id = input('请输入：')
        if menu_id.isdecimal() and int(menu_id) in (1, 2, 3):
            break
        else:
            print('请正确输入编号')
    return int(menu_id)


def check_menu_id():
    while True:
        menu_id = input('请输入操作编号：')
        if not menu_id.isdecimal():
            print('请正确输入编号')
            continue
        menu_id = int(menu_id)
        if menu_id > 7 or menu_id < 1:
            print('请正确输入编号')
            continue
        return menu_id


def show_logs():
    try:
        f = open('./data/logs.txt', 'r')
        line = f.readline()
        while line:
            print(line, end='')
            line = f.readline()
        print()
    except:
        print('打开日志文件异常')
    finally:
        f.close()


def main():
    """ 程序入口"""
    while True:
        welcome()
        main_id = check_welcome_id()
        if main_id == 1:
            sign_up()
        elif main_id == 2:
            if not login():
                continue
            while True:
                main_menu()
                menu_id = check_menu_id()
                if menu_id == 1:
                    show_info()
                elif menu_id == 2:
                    draw()
                elif menu_id == 3:
                    deposit()
                elif menu_id == 4:
                    transfer()
                elif menu_id == 5:
                    show_logs()
                elif menu_id == 6:
                    break
                elif menu_id == 7:
                    logout()
        elif main_id == 3:
            logout()


if __name__ == '__main__':
    main()
