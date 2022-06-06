from argparse import Action
from lib2to3.pgen2 import driver
from RPA.Browser.Selenium import Selenium
from selenium.webdriver import ActionChains
#ＲＥＡＤＭＥ！需要五秒驗證碼輸入，卡在關不掉借用畫面的checkbox
import time
lib = Selenium()
lib.auto_close = "False"
user = {'account':'410731220','password':'otter520','friend1':'410831143','friend2':'410731212','order':1}
rentDay = '2022-06-06'

def log():

    lib.open_available_browser('https://sso.nknu.edu.tw/NewLayout/Ex2/page2.aspx?catagoryId=4')
    notLogIn = True
    while notLogIn:
        lib.input_text('uLoginID',user['account'])
        lib.input_text('uPassword',user['password'])
        lib.input_text('uAuthorizationCodeInput','') #圖片在這'xpath://*[@id="ssoLogin"]/table/tbody/tr[3]/td[2]/span/span/img'
        time.sleep(5) #驗證碼暫時手輸
        lib.click_button('id:uLogin')
        notLogIn = lib.is_alert_present('驗證碼輸入不正確！')
    lib.go_to(lib.get_element_attribute('xpath://*[@id="ctl00_phMain_divMenu2"]/div[2]/div[2]/div[10]/div/div/a','href'))
    lib.go_to('https://lend.nknu.edu.tw/semac/service/index')
    '''
    actions = webdriver.ActionChains('id:proclamation')
    lib.wait_until_element_is_visible('id:check_read')
    actions.move_to_element('id:check_read')
    actions.click('id:check_read')
    actions.perform()
    actions.move_to_element('id:close_modal')
    actions.click('id:close_modal')
    actions.perform()
    driver.execute_script('id:proclamation.click();', 'id:check_read')
    看不懂的參考 https://stackoverflow.com/questions/58808856/element-click-intercepted-error-while-trying-to-click-on-checkbox
    '''
    lib.click_element('id:check_read',action_chain=True)
    lib.click_element('id:close_modal',action_chain=True)
    
def reservation():
    lib.select_from_list_by_index('xpath://*[@id="expire_vue"]/div/div/div[2]/div[1]/div/div/div/div/ul',1)
    lib.input_text('input_date',rentDay)
    lib.click_button('id:button_go')
    #用table attribute('id:{%d}-{%d}','background-color')
    #cancel
    if user['room'] == 1:
        pass
    else:

        return('Undefined (@_@);')
    return('OK')
def cancel():
    lib.go_to('https://lend.nknu.edu.tw/semac/service/history')
    lib.click_button_when_visible('xpath://*[@id="history_vue"]/div/div/table/tbody/tr[1]/td[9]/div/button[2]')
    lib.is_alert_present('確定要取消嗎?')
#記得刪掉下面
log()
cancel()
reservation()
'''前端需求:依次一個帳號只能借用一個
和平
1.研究小間 三天前
2.小型團體討論室(4F、5G)、學習室、共享室及會議室等空間預約借用(3人) 七天前
3.3F中型團體討論室(2F、3F)、
燕巢
1.研究小間 三天前
2.

2.教職員、研究生一次6小時為限，大學部學生、助理、校友一次4小時為限。借用時間以30分鐘為單位。

(二)小型團體討論室、學習室、共享室及會議室等空間預約借用(3人以上，主借者另計)：
1.限本校教職員生(含校友)七天前可預約借用，預約次數以單次為限。一次使用完，可進行下一次預約。當天可續借乙次，不接受整學期預約。
'''