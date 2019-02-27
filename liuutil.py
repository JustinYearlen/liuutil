# --*-- coding = utf-8 --*--

"""
Author: liu
date:2019-02-27
将符合条件的字符串转换成 yyyy年mm月dd日的形式
"""


def convert_chinese_to_number(chinese_date):
    # 不处理非字符串类型
    if isinstance(chinese_date, str):
        result = ''
        CN = ['〇', '一', '二', '三', '四', '五', '六', '七', '八', '九', '零']
        number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        numberToCN = dict(zip(CN, number))
        #     print (type(chinese_date))
        for i, s in enumerate(chinese_date):
            # 处理数字十
            if s == '十' and (i > 0 & i < len(chinese_date)):
                next_str = chinese_date[i + 1]
                preview_str = chinese_date[i - 1]
                # 十前后都有数字不用处理，舍去
                if (next_str in CN) and (preview_str in CN):
                    pass
                elif next_str in CN:
                    result = result + '1'
                elif preview_str in CN:
                    result = result + '0'
                else:
                    result = result + '10'
            elif s in CN:
                result = result + numberToCN[s]
            else:
                result = result + s
        return result
    else:
        return chinese_date


if __name__ == '__main__':
    print(convert_chinese_to_number('二零一八年十月二十一日'))
