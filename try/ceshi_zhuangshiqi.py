import uiautomator2

pp = uiautomator2.connect_usb()
top_y = pp.xpath('//android.webkit.WebView/android.view.View[1]/android.view.View[1]/'
                 'android.view.View[1]').get(timeout=5).bounds[3]
down_y = pp.xpath('//android.webkit.WebView/android.view.View[1]/android.view.View[1]/'
                  'android.view.View[2]').get(timeout=5).bounds[3]

while True:
    pp(scrollable=True).scroll(steps=90)
    print((pp(text='您已经看到了我的底线').exists and
                    down_y > pp(text='您已经看到了我的底线').bounds()[1] > top_y and
                    pp(text='您已经看到了我的底线').bounds()[3] - pp(text='您已经看到了我的底线').bounds()[1] > 5))
# pp(scrollable=True).swipe("up", steps=60)
