from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint
import pandas as pd

# geckodriver_path = '/home/mayank/dev/Bots/geckodriver' 
webdriver = webdriver.Chrome()
sleep(2)
webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(3)

username = webdriver.find_element_by_name('username')
username.send_keys('your-username')
password = webdriver.find_element_by_name('password')
password.send_keys('your_pass')

button_login = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]/button/div')
button_login.click()
sleep(5)
try:
    notnow = webdriver.find_element_by_xpath('/html/body/div[4]/div/div/div[3]/button[2]')
    notnow.click() 
    sleep(3)
except:
    pass

hashtag_list = ['pahadi','kumaun','garhwal','mountains','chopta','pahad']

# prev_user_list = [] #- if it's the first time you run it, use this line and comment the two below
prev_user_list = pd.read_csv('20200419-140346_users_followed_list.csv', delimiter=',').iloc[:,1:2] # useful to build a user log
prev_user_list = list(prev_user_list['0'])

new_followed = []
tag = -1
followed = 0
likes = 0
comments = 0

for hashtag in hashtag_list:
    tag += 1
    webdriver.get('https://www.instagram.com/explore/tags/'+ hashtag_list[tag] + '/')
    sleep(5)
    first_thumbnail = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
    
    first_thumbnail.click()
    sleep(randint(1,5))    
    try:        
        for x in range(1,200):
            username = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/a').text
            
            if username not in prev_user_list:
                # If we already follow, do not unfollow
                if webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':
                    
                    webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
                    sleep(randint(2,5))
                    
                    new_followed.append(username)
                    followed += 1

                    # Liking the picture
                    button_like = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button').click()
                    
                    # button_like.click()
                    likes += 1
                    sleep(randint(10,20))

                    # Comments and tracker
                    comm_prob = randint(1,10)
                    print('{}_{}: {}'.format(hashtag, x,comm_prob))
                    if comm_prob > 1:
                        comments += 1
                        webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[2]/button').click()
                        comment_box = webdriver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/textarea')

                        if (comm_prob < 4):
                            comment_box.send_keys('Nice profile. Please take a look at my page for really awesome content')
                            sleep(1)
                        elif (comm_prob > 6) and (comm_prob < 9):
                            comment_box.send_keys('Nice work :)')
                            sleep(1)
                        elif (comm_prob > 3) and (comm_prob < 7):
                            comment_box.send_keys('Awesome clicks')
                            sleep(1)
                        elif comm_prob == 9:
                            comment_box.send_keys('Nice gallery!!')
                            sleep(1)
                        elif comm_prob == 10:
                            comment_box.send_keys('So cool! :)')
                            sleep(1)
                        # Enter to post comment
                        comment_box.send_keys(Keys.ENTER)
                        sleep(randint(10,20))

                # Next picture
                webdriver.find_element_by_link_text('Next').click()
                sleep(randint(15,30))
            else:
                webdriver.find_element_by_link_text('Next').click()
                sleep(randint(1,5))
    # some hashtag stops refreshing photos (it may happen sometimes), it continues to the next
    except:
        continue

for n in range(0,len(new_followed)):
    prev_user_list.append(new_followed[n])
    
updated_user_df = pd.DataFrame(prev_user_list)
updated_user_df.to_csv('{}_users_followed_list.csv'.format(strftime("%Y%m%d-%H%M%S")))
print('Liked {} photos.'.format(likes))
print('Commented {} photos.'.format(comments))
print('Followed {} new people.'.format(followed))


