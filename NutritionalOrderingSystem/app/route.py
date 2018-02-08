# coding: utf-8
from flask import Flask, redirect, render_template, request, session, url_for

from app.db import mysql_oper
from app.entity.instance import INSTANCE
from app.data_calculation import set_standard_value


app = Flask(__name__)
# 加密符，可以忽略
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


# ---------------- #
#   web 请求的响应  #
# ---------------- #
@app.route("/")
@app.route("/index")
def web_index():
    return render_template("index.html", header_title="营养订餐-首页")


@app.route("/login")
def web_login():
    return render_template("login.html", header_title="营养订餐-登录")


@app.route("/register")
def web_register():
    return render_template("register.html", header_title="营养订餐-注册")


@app.route("/account")
def web_account():
    return render_template("account.html", header_title="营养订餐-账户")


@app.route("/analysis")
def web_analysis():
    try:
        set_standard_value(session)
    except BaseException as err:
        print("except: " + str(err))
    return render_template("analysis.html", header_title="营养订餐-分析")


@app.route("/send_meal")
def web_send_meal():
    return render_template("send_meal.html", header_title="营养订餐-送餐")


# ---------------- #
# action 请求的响应 #
# ---------------- #
@app.route("/action/login", methods=['POST'])
def act_login():
    request.charset = "UTF-8"
    username = request.form['username']
    password = request.form['user_pwd']
    if valid_login(username, password):
        # 更新 session
        refresh_all_session(session)
        return redirect(url_for('web_account'))


# 账户验证
def valid_login(username, password):
    INSTANCE.USER = mysql_oper.find_user(username)
    if INSTANCE.USER is not None:
        if password == INSTANCE.USER.password:
            return True
    return False


# 同步session
def refresh_all_session(sess):
    sess['username'] = INSTANCE.USER.username
    sess['nickname'] = INSTANCE.USER.nickname
    sess['address'] = INSTANCE.USER.address
    sess['phoneNumber'] = INSTANCE.USER.phoneNumber
    sess['gender'] = INSTANCE.USER.gender
    sess['age'] = INSTANCE.USER.age
    sess['height'] = INSTANCE.USER.height
    sess['weight'] = INSTANCE.USER.weight
    sess['waist'] = INSTANCE.USER.waist
    sess['BFR'] = INSTANCE.USER.BFR
    sess['BMR'] = INSTANCE.USER.BMR
    return True


# 同步user
def refresh_instance_user(sess):
    INSTANCE.USER.username = sess['username']
    INSTANCE.USER.nickname = sess['nickname'] 
    INSTANCE.USER.addres =  sess['address']
    INSTANCE.USER.phoneNumber = sess['phoneNumber']
    INSTANCE.USER.gender = sess['gender']
    INSTANCE.USER.age = sess['age']
    INSTANCE.USER.height = sess['height']
    INSTANCE.USER.weight = sess['weight']
    INSTANCE.USER.waist = sess['waist']
    INSTANCE.USER.BFR = sess['BFR']
    INSTANCE.USER.BMR = sess['BMR'] 
    return True


@app.route("/action/logout", methods=['POST'])
def act_logout():
    session.clear()
    # flash("Logout")
    return redirect(url_for('web_login'))


@app.route("/action/register", methods=['POST'])
def act_register():
    request.charset = "UTF-8"
    username = request.form['username']
    password = request.form['user_pwd1']
    mysql_oper.insert_user(username, password)
    INSTANCE.USER = mysql_oper.find_user(username)
    refresh_all_session(session)
    return redirect(url_for('web_account'))


@app.route("/action/create_menu", methods=['POST'])
def act_create_menu():
    return redirect(url_for('web_index'))


@app.route("/action/refresh_data", methods=['POST'])
def act_refresh_data():
    # 计算，然后更新数据库更新session
    request.charset = "UTF-8"
    edit_id = request.form["edit-id"]
    # username = request.form["username"]

    value = ""
    if edit_id == "BFR":
        bfr = float()
        if INSTANCE.USER.gender == "女":
            bfr = float((float(INSTANCE.USER.waist) * 0.74 - float(INSTANCE.USER.weight) *
                         0.082 - 34.89) / float(INSTANCE.USER.weight) * 100)
        else:
            bfr = float((float(INSTANCE.USER.waist) * 0.74 - float(INSTANCE.USER.weight) *
                         0.082 - 44.74) / float(INSTANCE.USER.weight) * 100)
        value = ("%.2f" % bfr)
    elif edit_id == "BMR":
        bmr = float()
        if INSTANCE.USER.gender == "男":
            bmr = float(float(INSTANCE.USER.weight) * 13.7 + float(INSTANCE.USER.height) * 0.5
             - 6.8 * float(INSTANCE.USER.age) + 66)
        else:
            bmr = float(float(INSTANCE.USER.weight) * 9.6 + float(INSTANCE.USER.height) * 1.8 
            - 4.7 * float(INSTANCE.USER.age) + 665)
        value = ("%.2f" % bmr)

    # 数据库操作
    # mysql_oper.alter_data(str(session["username"]), edit_id, value)

    # 前端更新
    session[edit_id] = value
    # 同步user
    refresh_instance_user(session)
    return redirect(url_for('web_account'))


@app.route("/action/edit_info", methods=['POST'])
def act_edit_info():
    request.charset = "UTF-8"
    edit_id = request.form["edit-id"]
    value = request.form["edit-value"]

    # 数据库操作
    # mysql_oper.alter_data(str(session["username"]), edit_id, value)

    # 前端更新
    session[edit_id] = value

    return redirect(url_for('web_index'))
