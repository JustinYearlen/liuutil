# --*-- coding = utf-8 --*--
"""
Author: liu
date:2019-02-27

"""
import re


def convert_chinese_to_number(chinese_date):
    """
    将符合条件的字符串转换成 yyyy年mm月dd日的形式
    """

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


def chntonum(chn, errors='ignore'):
    """

    :param chn: 中文格式字符例如：二十万元 或者20万元 最后必须以万结尾
    :param errors: ignore \ceocer
    :return:cur 以元为单位，带两位小数点的数字
    """
    # 设置数字集合处理纯数字型字符串
    lcn = set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '万', '元'])

    CN = ['〇', '一', '二', '三', '四', '五', '六', '七', '八', '九',
          '零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
    number = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
              0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    dct_chntonum = dict(zip(CN, number))
    cnunit = ['十', '佰', '千', '万', '亿', '元', '百', '仟', '拾']
    unit = [10, 100, 1000, 10000, 100000000, 1, 100, 1000, 10]
    dct_unit = dict(zip(cnunit, unit))
    cur = 0.0
    if isinstance(chn, str):
    #处理数字型123.09元 或者 123.09万元
        if not set(chn)-lcn:
            if chn.endswith('万元'):
                return float(chn[0:-2])*10000
            if chn.endswith('元'):
                return float(chn[0:-1])
        else:
                # 处理以“十”开头的字符串
            if chn[0] == '十':
                cur = cur + 10
                chn = chn[1:]
            for n in chn:
                if n in CN:
                    cur = cur + dct_chntonum[n]
                elif n in cnunit:
                    cur = cur * dct_unit[n]
                else:
                    raise Exception("含有非数字型文字!")
            return cur

    else:
        if errors == 'ignore':
            return chn
        else:
            raise Exception("非字符串，格式不正确!")


def penalty_tran(result_penalty):
    """
    处理中国银行保险监督管理委员会行政处罚信息公开表的“行政处罚决定”字段
    :param result_penalty:行政处罚决定内容
    :return:penalty_type 1:行政处罚类型；fee 2:罚款金额；confiscation 3:没收违反所得金额；
            lasting 4:取消任职资格年限（字符型有永久）
    penalty_category :['1-警告','2-罚款','3-没收违反所得','5-取消任职资格','7-其他']
    """
    penalty_category = {'1': '警告', '2': '罚款', '3': '没收违法所得', '5': '取消任职资格', '7': '其他'}

    penalty_type = []
    fee = ''
    confiscation = ''
    lasting = ''

    if isinstance(result_penalty, str):
        if re.search(pattern='警告', string=result_penalty):
            penalty_type.append('警告')
        a = re.search(pattern='罚款', string=result_penalty)
        # 匹配数字
        b = re.findall(pattern='[0-9\.〇一二三四五六七八九十零壹贰叁肆伍陆柒捌玖拾佰]{1,10}[千万亿]?元', string=result_penalty)
        if a and len(b) > 0:
            penalty_type.append('罚款')
            fee = b[0]
        res = re.search(pattern=r'没收', string=result_penalty) and len(b) > 0
        if res:
            penalty_type.append('没收违法所得')
            if len(b) == 2:
                confiscation = b[0]
                fee = b[1]
        if re.search(pattern=r'取消.*任职资格', string=result_penalty):
            penalty_type.append('取消任职资格')
            c = re.search(pattern='[0-9\.〇一二三四五六七八九十零壹贰叁肆伍陆柒捌玖拾]{1,2}?年|终身', string=result_penalty)
            if c:
                lasting = c.group()
        return ','.join(penalty_type) if penalty_type else '其他', fee, confiscation, lasting
    else:
        return ','.join(penalty_type), fee, confiscation, lasting


if __name__ == '__main__':
    # print(convert_chinese_to_number('二零一八年十月二十一日'))
    #print(penalty_tran('警告,没收违法所得769.37元，并处以罚款人民币50万元。取消2年任职资格'))
    ls = ['五万元', '10万元', '', '20万元', '30万元', '二十万元', '三十万元', '5万元', '八万元',
       '1080万元', '一万元', '二万元', '十万元', '420万元', '40万元', '80万元', '1万元',
       '50万元', '六十万元', '15万元', '150万元', '8万元', '35万元', '5000元', '55万元',
       '3万元', '四十五万元', '18000元', '三万元', '210万元', '2万元', '353697.22元',
       '9万元', '25万元', '五十万元', '六万元', '3000元', '4359.58元', '24706元',
       '4146.85元', '104784元', '9175.40元', '14670.14元', '50000元',
       '38395.5元', '9328.16元', '1000元', '51200元', '七万元', '10000元',
       '30072元', '49263.5元', '3360元', '20790元', '24000元', '12400元', '4万元',
       '二十五万元', '105万元', '壹拾万元']
    for each in ls:
        print(chntonum(each))
