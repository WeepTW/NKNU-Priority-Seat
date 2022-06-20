import os
from RPA.Browser.Selenium import Selenium
import pandas as pd
import datetime
from selenium.common.exceptions import WebDriverException as ex
from mod import captcha1
#from mod import captcha2
lib = Selenium()
dirname = os.path.dirname(os.path.realpath(__file__))
path = dirname+ r'\captcha.png'

def log(id):
    user = []
    df = pd.read_excel(dirname + r'\Info.xlsx',index_col=0)
    if id in list(df.index):
        friends = []
        for i in range(1,6):
            if  not pd.isna(df.at[id,i]):
                friends.append(str(df.at[id,i]))
        user =  {'account':df.at[id,'account'],'password':df.at[id,'password'],'reservation':df.at[id,'token'],'friends':friends} 
    else:
        return user
    lib.open_available_browser('https://sso.nknu.edu.tw/NewLayout/Ex2/page2.aspx?catagoryId=4')
    notLogIn = True
    while notLogIn:
        lib.screenshot('xpath://*[@id="ssoLogin"]/table/tbody/tr[3]/td[2]/span/span/img', path)
        lib.input_text('uLoginID',str(user['account']))
        lib.input_text('uPassword',str(user['password']))
        lib.input_text('uAuthorizationCodeInput', captcha1())
        #lib.click_button('uLogin') 不知道為什麼不用這個就會自己登入了
        notLogIn = lib.is_alert_present('驗證碼輸入不正確！')
        link = lib.get_element_attribute('xpath://*[@id="ctl00_phMain_divMenu2"]/div[2]/div[2]/div[10]/div/div/a','href')
    lib.go_to(link)
    return [user['account'],user['reservation'],user['friends'],link]

def __countblock(hour,min):
    if lib.does_page_contain_element(f'xpath://*[@id="owl-example"]/div[1]/div/div/div/table[2]/tbody/tr[2]/th'): page = ''
    elif lib.does_page_contain_element(f'xpath://*[@id="owl-example"]/div[1]/div/div[1]/div/table[2]/tbody/tr[2]/th'): page = '[1]'
    else: return 0
    startblock = 2
    while(lib.does_page_contain_element(f'xpath://*[@id="owl-example"]/div[1]/div/div{page}/div/table[2]/tbody/tr[{startblock}]/th')):
        t = lib.get_text(f'xpath://*[@id="owl-example"]/div[1]/div/div{page}/div/table[2]/tbody/tr[{startblock}]/th').split('~')[0].split(':')
        if hour < int(t[0]): return 2
        elif hour == int(t[0]):
            if min < int(t[1]): startblock -= 1
            elif min > int(t[1]): startblock += 1
            break
        else: startblock += 2
    return startblock

def __summit(colIndex,pageIndex,startblock,titular = []):
    #set xpath index
    if startblock < 2: return False
    if pageIndex == 0 :
        page = ''
    else:
        lib.click_element(f'xpath://*[@id="owl-example"]/div[2]/div[1]/div[{pageIndex}]/span')
        page = f'[{pageIndex}]'
    if colIndex == 0: col = ''
    else: col = f'[{colIndex}]'
    for i in range(startblock,startblock +2): #check whether there are at least 1 hours to rent(must more)
        if not (lib.does_page_contain_element(f'xpath://*[@id="owl-example"]/div[1]/div/div{page}/div/table[2]/tbody/tr[{i}]/td{col}/span') and lib.get_element_attribute(f'xpath://*[@id="owl-example"]/div[1]/div/div{page}/div/table[2]/tbody/tr[{i}]/td{col}/span','class') == 'btn'):
            return False
    unsent = True #reserving
    buttonIndex = 2
    tryTime = 1
    if len(titular) > 0:
        buttonIndex = 3
        if titular != [1,1]:
            for friend in titular:
                lib.input_text('xpath://*[@id="expire_vue"]/div[2]/div/form/div[2]/div/div/div/input',friend)
                lib.click_element('xpath://*[@id="expire_vue"]/div[2]/div/form/div[2]/div/div/div/span[2]/span')
                lib.click_element_when_visible('xpath://*[@id="member_vue"]/div/div/div[3]/button[1]')
    while unsent:
        try:
            lib.click_element_when_visible(f'xpath://*[@id="owl-example"]/div[1]/div/div{page}/div/table[2]/tbody/tr[{startblock}]/td{col}/span')
        except ex:
            lib.scroll_element_into_view(f'xpath://*[@id="owl-example"]/div[1]/div/div{page}/div/table[2]/tbody/tr[{tryTime}]/th')
            if lib.does_page_contain_element(f'xpath://*[@id="owl-example"]/div[1]/div/div{page}/div/table[2]/tbody/tr[{tryTime+2}]/th'): tryTime += 2
            else: lib.scroll_element_into_view('id:head_vue')
            continue
        except:
            return False
        lib.screenshot('id=input-captcha-pic', path)
        lib.input_text(f'xpath://*[@id="expire_vue"]/div[2]/div/form/div[{buttonIndex}]/div/div/input', captcha2())
        lib.click_button(f'xpath://*[@id="expire_vue"]/div[2]/div/form/div[{buttonIndex +1}]/div[2]/button')
        if lib.does_page_contain_button('xpath:/html/body/div[4]/div/div[3]/button[2]'):
            lib.click_button('xpath:/html/body/div[4]/div/div[3]/button[2]')
        elif buttonIndex == 3 and lib.does_page_contain_element('xpath://*[@id="expire_vue"]/div[2]/div/form/div[2]/div/div[2]/label'):
            return False
        unsent = not lib.is_alert_present('申請成功送出，請等候系統處理!')
    return lib.does_page_contain_button(f'xpath://*[@id="history_vue"]/div/div/table/tbody/tr[1]/td[9]/div/button[2]')

def cancel(id):
    if log(id) == []:
        return ['PermissionError']
    lib.go_to('https://lend.nknu.edu.tw/semac/service/history')
    i = 0
    for i in range(1,16):
        if lib.does_page_contain_button(f'xpath://*[@id="history_vue"]/div/div/table/tbody/tr[{i}]/td[9]/div/button[2]'):
            lib.click_button_when_visible(f'xpath://*[@id="history_vue"]/div/div/table/tbody/tr[{i}]/td[9]/div/button[2]')
            lib.is_alert_present('確定要取消嗎?')
            lib.is_alert_present('取消成功!')
        else:
            i -= 1
            break
    lib.close_all_browsers() #close in here to pervent full of memory
    if i == 0: return 'No reservation'
    if i == 1: return 'A room was cancelled'
    return f'{i} rooms were cancelled successfully'

def record(id): #default to show the lastest, max of n is 15
    if log(id) == []:
        return ['PermissionError']
    lib.go_to('https://lend.nknu.edu.tw/semac/service/history')
    s = ''
    while(lib.get_element_attribute('xpath://*[@id="history_vue"]/div/div/div[1]/div[3]/div/button[2]','disable') != ''):
        for i in range(1,15): #max of a page is 
            if lib.does_page_contain_button(f'xpath://*[@id="history_vue"]/div/div/table/tbody/tr[{i}]/td[9]/div/button[2]'):
                s += f'Reservation No.{i}:'
                + '/nArea' + lib.get_text(f'xpath://*[@id="history_vue"]/div/div/table/tbody/tr[{i}]/td[1]/a') 
                + '/nroom:' + lib.get_text(f'xpath://*[@id="history_vue"]/div/div/table/tbody/tr[{i}]/td[3]/a')
                + '/ntime:' + lib.get_text(f'xpath://*[@id="history_vue"]/div/div/table/tbody/tr[{i}]/td[4]')
            else:
                lib.close_all_browsers() #close in here to pervent full of memory
                if s == '': s = 'No record'
                return s
        lib.click_button('xpath://*[@id="history_vue"]/div/div/div[1]/div[3]/div/button[2]')
    return 'PageError'

def reservation(id,token,days = 0,hour = datetime.datetime.now().hour, min = datetime.datetime.now().minute):
    #torch & script太大 沒辦法用 QQ
    return '已經幫您處理了'
    #check input
    if token == 0: token = user[1]
    if token in [5,6,7,8,26,26,27,32]:
        if not days in range(8): return 'DaysError'
    elif token in [19,23]:
        if not days in range(4): return 'DaysError'
    else: return 'TokenError'
    if not(type(hour) == type(1) and type(min) == type(1)): return 'TimeError:Chaos'
    hour = int(hour)
    min = int(min)
    if 0 < hour < 23 and 0 <= min < 60: 'TimeError:WrongType'
    if 0 < min <= (28 if days==0 else 30): min = 30
    elif min >= 58 and days == 0: hour += 1; min= 30
    else: hour += 1; min = 0
    user = log(id)
    if user == []: return 'PermissionError'
    lib.go_to('https://lend.nknu.edu.tw/semac/service/index')
    lib.go_to(f'https://lend.nknu.edu.tw/semac/service/expire2/{8 if token in [5,6,7,8] else token}_{datetime.date.today() + datetime.timedelta(days=days)}')
    if lib.get_location() == 'https://lend.nknu.edu.tw/semac/service/index': return 'SystemException'
    if not lib.does_page_contain_button('xpath://*[@id="expire_vue"]/div[2]/div/form/div[4]/div[2]/button') ^ lib.does_page_contain_button('xpath://*[@id="expire_vue"]/div[2]/div/form/div[3]/div[2]/button'): return 'TimeError:SystemExpection'
    #room ordering
    startblock = __countblock(hour,min)
    xpath = 'xpath://*[@id="history_vue"]/div/div/table/tbody/tr[1]/td[4]'
    if token in [5,6,7,8] and __summit(token-4,0,startblock,titular=user[2][0:2]): lib.get_text(xpath) #燕-小型團體討論室(2A:5 2B:6)、欣賞室(2A:7 2B:8)
    elif token == 19: #燕-研究小間(14)
        for page in range(3):
            for col in range( 4 if page == 0 else 5):
                if __summit(col+1,3-page,startblock): return lib.get_text(xpath)
    elif token == 32: #燕-討論室(1A 1B 1C 1D 1E 1F)
        if __summit(0,2,startblock,titular=user[2][0:2]): return lib.get_text(xpath)
        for i in range(5):
            if __summit(i+1,1,startblock,titular=[1,1]): return lib.get_text(xpath)
    elif token == 23: #和-研究小間(30)
        for page in range(6):
            for i in range(5):
                if __summit(i+1,page+1,startblock): return lib.get_text(xpath)
     #和-小型團體(4F、5F)
    elif token in [26,27] and __summit(1,0,startblock,titular=user[2][0:2]): return lib.get_text(xpath)
    lib.close_all_browsers() #close in here to pervent full of memory
    return 'Alert:Closed or FullHouse'
