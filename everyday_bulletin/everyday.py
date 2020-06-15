import re
import time
import json


def fetch_text():
    airports = {'首都': 1, '大兴': 2, '天津': 3, '石家庄': 4, '太原': 5, '呼和浩特': 6}
    with open('每日信息.txt', 'r', encoding='UTF-8') as f:
        content = f.readlines()
    contents = re.sub(r'\s', '', ''.join(content)).split('。')  # 按照中文句号进行分割
    str_fang = r'\u653e\u884c.*?\%'  # 放行正常率数字
    str_chu = r'\u51fa\u6e2f.*?\%'   # 出港正常率数字
    str_qi = r'\u8d77\u98de.*?\%'   # 起飞正常率数字
    str_jin = r'\u8fdb\u6e2f.*?\%'   # 进港正常率数字
    str_shi = r'\u59cb\u53d1.*?\%'  # 始发正常率数字
    all_bulletin = {}
    airport_bulletin = {}
    for info in contents:
        if len(info) <= 5:
            continue
        # print(info)
        date_time_struct = time.strptime(re.findall(r'\d{1,2}\u6708\d{1,2}\u65e5', info)[0], '%m月%d日')
        date_chs = '{}年{}月{}日'.format(
            time.localtime(time.time()).tm_year, date_time_struct.tm_mon, date_time_struct.tm_mday)
        fang_num = re.sub(r'[\u4E00-\u9FA5]', '', re.findall(str_fang, info)[0])
        shi_num = re.sub(r'[\u4E00-\u9FA5]', '', re.findall(str_shi, info)[0])
        jin_num = re.sub(r'[\u4E00-\u9FA5]', '', re.findall(str_jin, info)[0])
        chu_num = re.sub(r'[\u4E00-\u9FA5]', '', re.findall(
            str_chu, info)[0] if re.findall(str_chu, info) else re.findall(str_qi, info)[0])
        flight_num = re.findall(r'\u8d77\u964d.*?(\d.*?)\u67b6\u6b21', info)[0]
        airport = re.findall(r"(\u9996\u90fd|\u5927\u5174|\u5929\u6d25|\u77f3\u5bb6\u5e84|\u592a\u539f|\u547c\u548c"
                             r"\u6d69\u7279).*?\u673a\u573a", info)[0]
        airport_bulletin[airport] = {'航班': flight_num, '放行': fang_num, '始发': shi_num, '出港': chu_num, '进港': jin_num}
        all_bulletin[date_chs] = airport_bulletin
        # print('\n', all_bulletin[date_chs])
        all_bulletin[date_chs] = dict(sorted(all_bulletin[date_chs].items(), key=lambda x: airports[x[0]]))
        # print(all_bulletin[date_chs].items())
    return all_bulletin


def read_json(data):
    with open('data.json', 'r+') as f:
        try:
            bulletin = json.load(f)
            return {**data, **bulletin}
        except Exception:
            return data


def write_json(data):
    with open('data.json', 'w+') as f:
        json.dump(data, f, ensure_ascii=False)


def write_txt(all_bulletin, flag='w+'):
    for k_date, v_date in all_bulletin.items():
        str_beijing = '【民航华北局】{}北京两场运行数据\n'.format(k_date)
        str_other = '【民航华北局】{}华北地区其它机场运行数据\n'.format(k_date)
        for k_airport, v_airport in v_date.items():
            str1 = '{}机场：共起降飞机{}架次，放行正常率{}，始发正常率{}，出港正常率{}，进港正常率{}。' .format(
                k_airport, v_airport['航班'], v_airport['放行'], v_airport['始发'], v_airport['出港'], v_airport['进港'])
            if k_airport in ['首都', '大兴']:
                str_beijing += str1
            else:
                str_other += str1
        str_beijing += '【运输处】'
        str_other += '【运输处】'
        if str_beijing or str_other:
            print(str_beijing)
            print(str_other)
            with open('短信.txt', flag, encoding='UTF-8') as f:
                f.write(str_beijing)
                f.write('\n\n')
                f.write(str_other)
                f.write('\n\n')


if __name__ == '__main__':
    text_dic = fetch_text()
    all_data = read_json(text_dic)
    write_json(all_data)
    # print(all_data)
    write_txt(text_dic)
    # write_txt(all_data, flag='a+')
