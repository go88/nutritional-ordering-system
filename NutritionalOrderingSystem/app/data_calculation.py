# coding: utf-8
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