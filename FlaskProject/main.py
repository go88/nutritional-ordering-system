# coding: utf-8
from flask import Flask, flash, session, render_template, request, redirect, url_for

import mysql_oper
import user

app = Flask(__name__)
# 加密符，可以忽略
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# 全局变量
g_user = user.User()


# ------------- #
# web 的请求响应 #
# ------------- #


@app.route("/")
@app.route("/index")
def web_index():
    if 'username' in session:
        return render_template("index.html", header_title="营养订餐-首页", username=session['username'])
    return render_template("index.html", header_title="营养订餐-首页", username=None)


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
    except Exception as err:
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
        refresh_session(session)
        return redirect(url_for('web_account'))


# 账户验证
def valid_login(username, password):
    global g_user
    g_user = mysql_oper.find_data(username)
    if g_user is not None:
        if password == g_user.password:
            return True
    return False


# 同步session
def refresh_session(sess):
    sess['username'] = g_user.username
    sess['nickname'] = g_user.nickname
    sess['address'] = g_user.address
    sess['phoneNumber'] = g_user.phoneNumber
    sess['gender'] = g_user.gender
    sess['age'] = g_user.age
    sess['height'] = g_user.height
    sess['weight'] = g_user.weight
    sess['waist'] = g_user.waist
    sess['BFR'] = g_user.BFR
    sess['BMR'] = g_user.BMR
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
    mysql_oper.insert_data(username, password)
    global g_user
    g_user = mysql_oper.find_data(username)
    refresh_session(session)
    return redirect(url_for('web_account'))


@app.route("/action/create_menu", methods=['POST'])
def act_create_menu():
    return redirect(url_for('web_index'))


@app.route("/action/refresh_data", methods=['POST'])
def act_refresh_data():
    # 计算，然后更新数据库更新session
    request.charset = "UTF-8"
    edit_id = request.form["edit-id"]
    username = request.form["username"]

    value = ""
    if edit_id == "BFR":
        bfr = float()
        if g_user.gender == "女":
            bfr = float((g_user.waist * 0.74 - g_user.weight * 0.082 - 34.89) / g_user.weight * 100)
        else:
            bfr = float((g_user.waist * 0.74 - g_user.weight * 0.082 - 44.74) / g_user.weight * 100)
        value = ("%.2f" % bfr)
    elif edit_id == "BMR":
        bmr = float()
        if g_user.gender == "男":
            bmr = float(g_user.weight * 13.7 + g_user.height * 0.5 - 6.8 * g_user.age + 66)
        else:
            bmr = float(g_user.weight * 9.6 + g_user.height * 1.8 - 4.7 * g_user.age + 665)
        value = ("%.2f" % bmr)

    # 数据库操作
    # mysql_oper.alter_data(str(session["username"]), edit_id, value)

    # 前端更新
    session[edit_id] = value
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


# 分析页面标准数据
def set_standard_value(sess):
    gender = sess["gender"]
    # 肥胖指数BMI
    height = float(sess["height"])
    weight = float(sess["weight"])

    bmi = int(weight / (height * height / 10000.0))
    sess["BMI"] = bmi

    if gender == "男":
        # 设置标准BMI
        sess["standardBMI"] = "20 - 25"
        if bmi < 20:
            sess["resultBMI"] = "过轻"
        elif 20 <= bmi < 26:
            sess["resultBMI"] = "适中"
        elif 26 <= bmi < 31:
            sess["resultBMI"] = "过重"
        elif 31 <= bmi < 36:
            sess["resultBMI"] = "偏胖"
        elif bmi >= 36:
            sess["resultBMI"] = "肥胖"
    # 女
    else:
        # 设置标准BMI
        sess["standardBMI"] = "19 - 24"
        if bmi < 19:
            sess["resultBMI"] = "过轻"
        elif 19 <= bmi < 25:
            sess["resultBMI"] = "适中"
        elif 25 <= bmi < 30:
            sess["resultBMI"] = "过重"
        elif 30 <= bmi < 35:
            sess["resultBMI"] = "偏胖"
        elif bmi >= 35:
            sess["resultBMI"] = "肥胖"

    # 体脂率
    bfr = sess["BFR"]
    if gender == "男":
        # 设置标准体脂
        sess["standardBFR"] = "15 - 21%"
        if bfr < 15:
            sess["resultBFR"] = "偏低"
        elif 15 <= bfr < 22:
            sess["resultBFR"] = "健康"
        elif 22 <= bfr < 32:
            sess["resultBFR"] = "偏胖"
        elif bfr >= 32:
            sess["resultBFR"] = "肥胖"
    # 女
    else:
        # 设置标准体脂
        sess["standardBFR"] = "15 - 31%"
        if bfr < 15:
            sess["resultBFR"] = "偏低"
        elif 15 <= bfr < 32:
            sess["resultBFR"] = "健康"
        elif 32 <= bfr < 41:
            sess["resultBFR"] = "偏胖"
        elif bfr >= 42:
            sess["resultBFR"] = "肥胖"

    # 代谢
    age = int(sess["age"])
    bmr = int(sess["BMR"])
    standard_bmr = float()
    if gender == "男":
        if 17 < age <= 30:
            standard_bmr = int(15.3 * weight + 679)
        elif 30 < age <= 60:
            standard_bmr = int(11.6 * weight + 879)
        elif age > 60:
            standard_bmr = int(13.5 * weight + 487)
    # 女
    else:
        if 17 < age <= 30:
            standard_bmr = int(14.7 * weight + 496)
        elif 30 < age <= 60:
            standard_bmr = int(8.7 * weight + 829)
        elif age > 60:
            standard_bmr = int(10.5 * weight + 596)

    sess["standardBMR"] = str(int(0.75 * standard_bmr)) + " ~ " + str(int(1.15 * standard_bmr))

    if (0.75 * standard_bmr) <= bmr <= (1.15 * standard_bmr):
        sess["resultBMR"] = "正常"
    elif bmr < 0.75 * standard_bmr:
        sess["resultBMR"] = "较低"
    elif bmr > 1.15 * standard_bmr:
        sess["resultBMR"] = "较高"
    else:
        sess["resultBMR"] = "异常"


if __name__ == "__main__":
    # app.run()
    # 默认使用
    # app.run(host="0.0.0.0")
    # debug使用
    app.run(debug=True)
