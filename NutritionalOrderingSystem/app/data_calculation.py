# coding: utf-8
# 分析页面标准数据


def set_standard_value(sess):
    gender = sess["gender"]
    height = float(sess["height"])
    weight = float(sess["weight"])
    age = int(sess["age"])

    # 算BMI返回比较情况
    sess["BMI"], sess["standardBMI"], sess["resultBMI"] = calc_bmi(gender, height, weight)

    # 返回体脂率比较情况
    bfr = int(float(sess["BFR"]))
    sess["standardBFR"], sess["resultBFR"] = calc_bfr(bfr, gender)

    # 代谢
    bmr = float(sess["BMR"])
    sess["standardBMR"], sess["resultBMR"] = calc_bmr(bmr, gender, weight, age)


def calc_bmi(gender, height, weight):
    bmi = int(weight / (height * height / 10000.0))
    standard_bmi = ""
    result_bmi = ""
    if gender == "男":
        # 设置标准BMI
        standard_bmi = "20 - 25"
        if bmi < 20:
            result_bmi = "过轻"
        elif 20 <= bmi < 26:
            result_bmi = "适中"
        elif 26 <= bmi < 31:
            result_bmi = "过重"
        elif 31 <= bmi < 36:
            result_bmi = "偏胖"
        elif bmi >= 36:
            result_bmi = "肥胖"
    # 女
    else:
        # 设置标准BMI
        standard_bmi = "19 - 24"
        if bmi < 19:
            result_bmi = "过轻"
        elif 19 <= bmi < 25:
            result_bmi = "适中"
        elif 25 <= bmi < 30:
            result_bmi = "过重"
        elif 30 <= bmi < 35:
            result_bmi = "偏胖"
        elif bmi >= 35:
            result_bmi = "肥胖"
    return bmi, standard_bmi, result_bmi


def calc_bfr(bfr, gender):
    standard_bfr = ""
    result_bfr = ""
    if gender == "男":
        # 设置标准体脂
        standard_bfr = "15 - 21%"
        if bfr < 15:
            result_bfr = "偏低"
        elif 15 <= bfr < 22:
            result_bfr = "健康"
        elif 22 <= bfr < 32:
            result_bfr = "偏胖"
        elif bfr >= 32:
            result_bfr = "肥胖"
    # 女
    else:
        # 设置标准体脂
        standard_bfr = "15 - 31%"
        if bfr < 15:
            result_bfr = "偏低"
        elif 15 <= bfr < 32:
            result_bfr = "健康"
        elif 32 <= bfr < 41:
            result_bfr = "偏胖"
        elif bfr >= 42:
            result_bfr = "肥胖"
    return standard_bfr, result_bfr


def calc_bmr(bmr, gender, weight, age):
    standard_bmr = ""
    result_bmr = ""
    float_bmr = float()
    if gender == "男":
        if 17 < age <= 30:
            float_bmr = int(15.3 * weight + 679)
        elif 30 < age <= 60:
            float_bmr = int(11.6 * weight + 879)
        elif age > 60:
            float_bmr = int(13.5 * weight + 487)
    # 女
    else:
        if 17 < age <= 30:
            float_bmr = int(14.7 * weight + 496)
        elif 30 < age <= 60:
            float_bmr = int(8.7 * weight + 829)
        elif age > 60:
            float_bmr = int(10.5 * weight + 596)

    standard_bmr = str(int(0.75 * float_bmr)) + \
                              " ~ " + str(int(1.15 * float_bmr))

    if (0.75 * float_bmr) <= bmr <= (1.15 * float_bmr):
        result_bmr = "正常"
    elif bmr < 0.75 * float_bmr:
        result_bmr = "较低"
    elif bmr > 1.15 * float_bmr:
        result_bmr = "较高"
    else:
        result_bmr = "异常"

    return standard_bmr, result_bmr
