from qiangguo_shuafen import QiangGuoFuZhu
import time


class DownTiaoZhanTiKu(QiangGuoFuZhu):
    def main_do(self, test=False):
        # self.pp.screen_on()
        self.pp.unlock()
        if self.unlock_password and self.pp(text='输入密码').exists(timeout=3):
            for k in self.unlock_password:
                self.pp(description=k).click()
                time.sleep(0.1)
            self.pp(text='输入密码').wait_gone()
        if test:
            self.test_pro()
        if 'cn.xuexi.android' in self.pp.app_list_running():
            self.pp.app_stop('cn.xuexi.android')
        self.pp.app_start('cn.xuexi.android')
        # 这个不能删，等待控件出现后再消失
        self.pp(resourceId='cn.xuexi.android:id/tvv_video_render').wait()
        self.pp(resourceId='cn.xuexi.android:id/tvv_video_render').wait_gone()
        # 检测是否登陆，如果没有登录就进行登录
        if self.pp(text='我的').click_exists(timeout=5):
            self.pp(resourceId='cn.xuexi.android:id/my_setting').click_exists(timeout=3)
            self.pp(text='退出登录').click_exists(timeout=3)
            self.pp(text='确认').click_exists(timeout=3)
        self.pp(text='登录').wait()
        self.pp(resourceId='cn.xuexi.android:id/et_phone_input').set_text(self.username)
        time.sleep(1)
        self.pp(resourceId='cn.xuexi.android:id/et_pwd_login').set_text(self.password)
        self.pp.xpath('//*[@resource-id="com.huawei.secime:id/char_keyboard_hide_btn"]').click_exists(timeout=1)
        self.pp(text='登录').click(timeout=2)
        self.pp(text='登录').wait_gone(timeout=5)
        if self.pp(text='连接失败，请检查你的网络后重试!').exists:
            print('网络不好，请重新连接网络')
            raise
        self.pp(text='我的').click_exists(timeout=20)
        time.sleep(1)
        print('开始获取题库了')
        try:
            self.run_challenge(ti_num=1300)
        except Exception:
            self.pp.screenshot('error.jpg')
        self.pp(resourceId='cn.xuexi.android:id/my_setting').click_exists(timeout=3)
        self.pp(text='退出登录').click_exists(timeout=3)
        self.pp(text='确认').click_exists(timeout=3)
        self.pp(text='登录').wait(timeout=20)
        self.pp.app_stop('cn.xuexi.android')
        time.sleep(1)
        self.pp.press('home')


if __name__ == '__main__':
    # 要在对象创建时传入参数tesseract_path，表示pytesseract.pytesseract.tesseract_cmd的路径，
    # 否则使用默认值r'C:/Program Files/Tesseract-OCR/tesseract.exe'
    phone_unlock_password = '850611'  # 手机锁屏的解锁码
    user_list = [
        ['18810810611', 'jiajia0611'],
        # ['18611001824', 'nopass.123'],
    ]
    for index_u, user in enumerate(user_list):
        do = DownTiaoZhanTiKu(username=user[0], password=user[1], unlock_password=phone_unlock_password)
        do.main_do()
        # do.main_do(test=True)
        #     do.recycle_main_do(cl_screen=True)
        # else:
        #     do.recycle_main_do(cl_screen=False)
