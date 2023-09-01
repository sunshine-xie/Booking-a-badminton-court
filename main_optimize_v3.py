"""
免责声明：
    本代码仅用做学习使用，切勿用作其他用途
    若因不当使用而违反任何规则，由使用者负责
    开发者不承担任何责任
"""
"""
开始时间
2022/11/17 19:37

下一版本两个优化方向
2022/11/20 15:30:31 
1.使用智能等待
2.使用xpath路径替换
"""
from selenium import webdriver
import datetime
import time
import schedule
from pyvirtualdisplay import Display
import sys


# 打开 登录页，并进行登录
def login(url, user_name, password):
    browser.get(url)

    window_handle = browser.current_window_handle
    print(window_handle)

    time.sleep(2)
    if browser.find_element_by_name("用户名"):
        browser.find_element_by_name("用户名").click()

        browser.find_element_by_name("用户名").send_keys(user_name)

        time.sleep(1)

        browser.find_element_by_name("密码").click()

        browser.find_element_by_name("密码").send_keys(password)

        time.sleep(1)

        browser.find_element_by_class_name("van-button").click()

    time.sleep(1)

    now = datetime.datetime.now()
    print('======login success:', now.strftime('%Y-%m-%d %H:%M:%S'))


# 定位 运动项目
def Locate(slt_item):
    browser.find_elements_by_class_name("van-tabbar-item")[1].click()  # 定位并点击 生活服务
    time.sleep(0.5)

    browser.find_elements_by_class_name("van-grid-item__content")[slt_item].click()  # 定位并点击 _ / _ / _
    time.sleep(0.5)


# 选择 校区
def SelectCampus(slt_campus):
    browser.find_elements_by_class_name("van-cell")[0].click()  # 定位并点击 选择场地
    time.sleep(0.5)

    browser.find_elements_by_class_name("van-cascader__option")[slt_campus].click()  # 定位并点击 __ / __校区
    print("%s" % browser.find_elements_by_class_name("van-cascader__option")[slt_campus].text)
    time.sleep(0.5)


# 选择场地
def SelectPlace(select_item, site, tim, tim_num):
    # site 指定的场地号
    # tim 指定的时间段 数组
    # tim_num 输入的 待抢的 时间段个数
    place_number = []
    time_slot = []  # 可选时间数组
    time_surplus = []  # 对应余量数组

    # 获取场地列表
    place_list = browser.find_elements_by_class_name("van-cascader__options")[1].text  # 获取场地列表 东丽1-7
    place_list = place_list.splitlines()

    # 获取场地列表的编号并存储在 place_number
    for place in place_list:
        print(place)
        place_number.append(int("".join(list(filter(str.isdigit, place)))))
    print(place_number)

    # 如果今天有 号场地,则选择它,如果没有,自动更改
    if site in place_number:
        print('今天有 %s 号场地' % site)
    else:
        print('今天没有 %s 号场地' % site)
        while site not in place_number:
            if site >= 4:
                site = site - 1
            else:
                site = site + 1
        print('自动选择了 %s 号场地' % site)

    time.sleep(0.5)
    # 获取可选择的场地的索引
    place_index = place_number.index(site)
    # 使用索引选择该场地
    browser.find_elements_by_class_name("van-cascader__option")[place_index + 2].click()  # 选择场地
    time.sleep(0.5)

    # 获取该场地下所有可选时间 以及该时间剩余量 存放在 all_time一维数组中
    all_time = browser.find_elements_by_class_name("van-pull-refresh")[0].text.splitlines()
    # 数组长度/2为可选时间段数量
    time_number = int(len(all_time) / 2)
    print(all_time, time_number)

    # 获取所有可算时间段放在 time_slot 一维数组中
    # 获取所有剩余量放在 time_surplus 一维数组中
    # 可改进，使用带步长的数组取值方法
    for i in range(0, time_number):
        time_slot.append(all_time[2 * i])
        time_surplus.append(int(all_time[2 * i + 1]))
    print(time_slot)
    print("剩余时间", time_surplus)

    # 如果选择的时间段有剩余场地,则选择,否则 往后 选择其他时间段
    sig = 0
    for t in tim:
        now = datetime.datetime.now()
        print('当前时间:', now.strftime('%Y-%m-%d %H:%M:%S'))
        if t in time_slot and time_surplus[time_slot.index(t)] != '0':
            time_slot_index = time_slot.index(t)
            browser.find_elements_by_class_name("van-checkbox__icon")[time_slot_index].click()  # 点击选择的时间点
            time.sleep(0.5)
            print('今天有 %s 的场地, 在第 %d 个位置' % (t, time_slot_index + 1))
            now = datetime.datetime.now()
            print('点击时间:', now.strftime('%Y-%m-%d %H:%M:%S'))
        else:
            print('今天没有 %s 的场地' % t)
            sig = sig + 1
    sign = 0
    # 如果待抢的时间段全都不符合，可抢的时间段（包括对余量的判断） >=2 时
    if sig == tim_num and time_number >= 2 and time_surplus.count(1) >= 2:
        browser.find_elements_by_class_name("van-checkbox__icon")[-1].click()
        time.sleep(0.5)

        browser.find_elements_by_class_name("van-checkbox__icon")[-2].click()
        time.sleep(0.5)

    elif sig == tim_num and time_number == 1 and time_surplus.count(1) == 1:
        browser.find_elements_by_class_name("van-checkbox__icon")[-1].click()
        time.sleep(0.5)

    elif sig == tim_num and time_number == 0:
        sign = 1  # 标志位 防止出现 场地存在在上一级选择目录,但是没有时间选择 而导致程序出错的情况
    # 提交订单
    browser.find_elements_by_class_name("van-button")[0].click()
    time.sleep(1)

    if sign == 0:
        browser.find_elements_by_class_name("van-button")[2].click()
        time.sleep(0.5)
        browser.find_elements_by_class_name("van-button")[3].click()
        time.sleep(0.5)
        browser.find_elements_by_class_name("van-tabbar-item")[2].click()  # 定位并点击 生活服务
        time.sleep(0.5)

def job():
    url = 'https://shfwyy.cauc.edu.cn/Life'

    user_name = '2021------'
    password = '26------'

    # user_name = '2021------'
    # password = '09------'

    # user_name = '2021------'
    # password = '27------'

    # user_name = '2021------'
    # password = '06------'

    select_campus = 0  # 0 东丽, 1 宁河
    select_item = 2  # 2 羽毛球, 3 乒乓球, 4 健身房暂时不可用
    select_site = 7  # 场地号 东丽 1-7   宁河 1-12
    select_time_slot = ['19:00 - 20:00', '20:00 - 21:00']
    end_time = datetime.datetime.strptime("06:54:50", "%H:%M:%S")  # 开始时间
    # start_time = ""  # 开始时间
    frequency = 5  # 尝试次数

    if select_item == 2:
        curr_url = 'https://shfwyy.cauc.edu.cn/Badminton'  # 羽毛球
    elif select_item == 3:
        curr_url = 'https://shfwyy.cauc.edu.cn/TableTennis'  # 乒乓球
    else:
        curr_url = 'https://shfwyy.cauc.edu.cn/Gymnasium'  # 健身房

    browser.switch_to.window(window_name=window_handle)  # window_handle

    login(url, user_name, password)

    for i in range(0, frequency):
        print('第 %d 次执行' % (i + 1))
        browser.get(url)
        time.sleep(0.5)
        # 需要定义循环刷新，根据判断条件来判断已经进行了下一步，然后进入选择场地
        while browser.current_url != curr_url:
            Locate(select_item)
            time.sleep(0.5)
            now = datetime.datetime.now()
            # now = datetime.datetime.strptime("06:53:50", "%H:%M:%S")
            if now > end_time:
                sys.exit(0)  # 0：正常退出 1：异常退出
        now = datetime.datetime.now()
        print('可进入时间:', now.strftime('%Y-%m-%d %H:%M:%S'))
        print(browser.current_url)

        SelectCampus(select_campus)
        SelectPlace(select_item, select_site, select_time_slot, tim_num=len(select_time_slot))
        time.sleep(0.5)
    browser.close()
    # display.stop()
    sys.exit(0)  # 0：正常退出 1：异常退出


if __name__ == "__main__":
    # 连接Chrome浏览器
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')  # 忽略证书错误
    chrome_options.add_argument("--incognito")  # 配置隐私模式
    # chrome_options.add_argument('disable-infobars')
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    display = Display(visible=True, size=(800, 800))
    display.start()
    browser = webdriver.Chrome(executable_path=r"D:/chromedriver_win32/chromedriver.exe",
                               options=chrome_options)
    browser.implicitly_wait(1)  # 全局等待加载
    window_handle = browser.current_window_handle
    print(window_handle)
    job()

    # schedule.every().day.at("11:10:50").do(job)
    #
    # while True:
    #     schedule.run_pending()



