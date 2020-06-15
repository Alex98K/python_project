import math


def get_xingzuo(month, date):
    dates = (21, 20, 21, 21, 22, 22, 23, 24, 24, 24, 23, 22)

    xz = ['摩羯座', '水瓶座', '双鱼座', '白羊座', '金牛座', '双子座',
          '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座']
    if date < dates[month - 1]:
        return xz[month - 1]
    else:
        return xz[month]


dt = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
dd = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
ds = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪']
dp = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子']

years, month, days, time = map(int, input('Input your birthday(EXP:1985-06-11-06):\n').split('-'))
print('你的生日是{}年{}月{}日'.format(years, month, days))
t = (years - 4) % 60 % 10
d = (years - 4) % 60 % 12
p = math.ceil(time / 2)

print('你出生在{}{}年{}时，属{}，你的星座是{}'.format(
    dt[t], dd[d], dp[p], ds[(years - 4) % 12], get_xingzuo(month, days)))







# Tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
# Dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
# Shu = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
# birthday = input("请输入您的出生年月日（格式为：xx.xx.xx）：")
# print("\n")
# bir = birthday.split(".")
# # print(bir)
#
# year = int(bir[0])
# month = int(bir[1])
# day = int(bir[2])
# print(year,month,day)

# def CalTiangan():
#     tian = (year + 7)%10
#     T = Tiangan[tian-1]
#     return T
# def CalDizhi():
#     di = (year + 9)%12
#     D = Dizhi[di-1]
