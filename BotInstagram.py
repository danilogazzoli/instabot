# -*- coding: utf-8 -*-

'''
Created in 09/2020
@Author: Danilo https://github.com/danilogazzoli
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from datetime import date
from datetime import datetime
from datetime import timedelta
import os
import csv
from selenium.common.exceptions import NoSuchElementException
import logging
from random import shuffle
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

'''
Esta classe é para ser utilizado como manipulador de eventos
'''
class Event():
	def __init__(self):
		self.__eventhandlers = []

	def __iadd__(self, handler):
		self.__eventhandlers.append(handler)
		return self

	def __isub__(self, handler):
		self.__eventhandlers.remove(handler)
		return self

	def __call__(self, *args, **kwargs):
		for eventhandler in self.__eventhandlers:
			eventhandler(*args, **kwargs)

'''
Esta é a classe principal do Bot
'''
class InstagramBot:

    def __init__(self, username, password, executable_path):
        self.username = username
        self.password = password
        self.count_likes = 0
        if 'geckodriver' in executable_path:
            firefox_capabilities = DesiredCapabilities().FIREFOX
            firefox_capabilities['marionette'] = True
            self.driver = webdriver.Firefox(executable_path=executable_path)
        else:     
            options = webdriver.ChromeOptions()
            ua = requests.Session()
            options.add_argument(f'iser-agent={ua}')
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option('excludeSwitches', ['enable-automation'])
            self.driver = webdriver.Chrome(executable_path=executable_path, chrome_options=options)

        self.OnGetAccountInLikes=Event() 

        self.OnGetFollowAccount=Event() 

        self.OnAfterComment=Event()

        self.selectors = {
          "instagram": "https://www.instagram.com/",
          "home_to_login_button": ".WquS1 a",
          "username_field": "//input[@name='username']",
          "password_field": "//input[@name='password']",
          "button_login": "._0mzm-",
          "search_user": "queryBox",
          "select_user": "._0mzm-",
          "textarea": "textarea",
          "send": "button",
          "like_unlike_button": ".//*[@aria-label='Like' or @aria-label='Unlike']",
          "login": "//a[@href='/accounts/login/?source=auth_switcher']",
          "scroll_to": "window.scrollTo(0, document.body.scrollHeight);",
          "following_button": "/html/body/div[1]/section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button",
          "caption_follow_button": "Seguir",
          "like_button": "/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button",
          "following_number": "/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span",
          "follower_number": "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/div/span",
          "message_button": "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/button",
          "message_box": "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea",
          "send_button_2": "/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/button",
          "send_button":   "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button",
          "send_button_3": "/html/body/div[5]/div/div/div[1]/div/div[2]/div/button",
          "arguments_scroll_to": "arguments[0].scrollIntoView();",
          "share_button": "/html/body/div[4]/div/div/div/div[2]/div/div[1]/div/div",
          "input": "/html/body/div[5]/div/div/div[2]/div[1]/div/div[2]/input",
          "select_user": "/html/body/div[5]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div",
          "like_heart": "//*[contains(@aria-label, 'Curtir')]",
          "load_more": "//*[contains(@aria-label, 'Carregar mais comentários')]",

        }

    def login(self):
        driver = self.driver
        driver.get(self.selectors["instagram"])
        self.countdown(3)

        user_element = driver.find_element(By.XPATH, self.selectors["username_field"])
        user_element.clear()
        self.__randomSleep__(4,6)
        user_element.send_keys(self.username)
        self.__randomSleep__(4,6)
        password_element = driver.find_element(By.XPATH, self.selectors["password_field"])
        password_element.clear()
        password_element.send_keys(self.password)
        self.__randomSleep__(4,6)
        password_element.send_keys(Keys.RETURN)
        self.__randomSleep__(4,6)


    def get_pics_ref(self, scroll_to = 9):
        driver = self.driver
        for i in range(1, scroll_to): 
            driver.execute_script(self.selectors["scroll_to"])
            self.countdown(3)
        
        hrefs = driver.find_element(By.TAG_NAME, "a")
        pic_hrefs = [elem.get_attribute("href") for elem in hrefs]
        hrefs = []
        for href in pic_hrefs:
            if 'instagram.com/p/' in href:
                hrefs.append(href)
        #pic_hrefs = ['instagram.com/p/' in elem for elem in pic_hrefs]        
        return hrefs
    
    def get_pic_from_href(self, pic_href):
        driver = self.driver
        driver.get(pic_href)
        driver.execute_script(self.selectors["scroll_to"])
        
    def curtir_fotos_com_a_hashtag(self, hashtag):
        if (self.count_likes > 0) and (self.count_likes % 200 == 0):
            print('já atingiu o limite de curtidas')
            self.countdown(60 * 10)
            self.count_likes += 1
            return

        driver = self.driver
        driver.get(self.selectors["instagram"] + "explore/tags/" + hashtag + "/")
        self.countdown(5)
        
        pic_hrefs = self.get_pics_ref()

        print(hashtag + " fotos: " + str(len(pic_hrefs)))
        for pic_href in pic_hrefs:
            try:
                pic_href.index(self.selectors["InstagramBot"] + "p")
            except ValueError as err:
                print("pulando link inválido")
                continue
            self.get_pic_from_href(pic_href)
            try:
                self.__randomSleep__(1,2)
                button_seguindo = driver.find_element(By.XPATH, self.selectors['following_button'] )

                print(button_seguindo.text)
                self.curtir_comentarios()
                if button_seguindo.text == self.selectors['caption_follow_button']:
                    self.like_pic()
                    self.count_likes += 1
                    print(f'Curtida nro {self.count_likes}')
                    self.__randomSleep__(19,23)

                else:
                    self.__randomSleep__(5,8)

            except Exception as e:
                print(e)
                self.countdown(5)

    def typephrase(self, comment, field):
        rand_back = random.randint(0, len(comment)-1)
        rand_back_letter = comment[rand_back]

        for letter in comment:  # commentary and lyrics
            field.send_keys(letter)  # type the letter in the field
            if letter == '@':
                self.countdown(1)
            elif letter == rand_back_letter:
                field.send_keys(Keys.BACKSPACE)
                self.countdown(1)
                field.send_keys(letter)
            else:    
                self.__randomSleep__(0,1)

    def countdown(self, segundos):
        if segundos > 10:
            for i in range(segundos, -1, -1):
                print(f"\b\b\b\b\b\b\b\b\b{str(timedelta(seconds=i))} ", end="", flush=True)
                time.sleep(1)
            print('\n')
        else:
            time.sleep(segundos)    

    def like_pic(self):
        driver = self.driver
        panels = driver.find_element(By.CLASS_NAME, 'eo2As')
        div = panels.find_element(By.CLASS_NAME, 'ltpMr')
        buttons = div.find_element(By.CLASS_NAME, 'wpO6b')
        #driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", panels) 
        #buttons[0].click()
        driver.execute_script("arguments[0].click();", buttons[0]) 

    def check_like_buttons(self):
        driver = self.driver
        
        like_buttons = []
        #buttons = driver.find_elements(By.XPATH, "//*[@aria-label='Curtir']")
        buttons = driver.find_elements(By.XPATH, "//*[@type='button']")
        for button in buttons:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", button) 
            if 'Curtir' in button.get_attribute('innerHTML'):
                like_buttons.append(button)
        '''
        for button in buttons:
            if 'aria-label="Curtir"' in button.get_attribute('outerHTML'):
               like_buttons.append(button)
        return like_buttons
        '''
        return like_buttons

    def curtir_comentarios(self):
        driver = self.driver
        
        buttons = self.check_like_buttons()

        #while len(buttons) > 0:
        for button in buttons:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", button) 
            try:
                button.click()
            except:
                pass
            self.countdown(random.randint(1, 3))

            #buttons = self.check_like_buttons()
        
        

    def get_publish_button(self):
        driver = self.driver
        publish_button = None
        buttons = driver.find_element(By.TAG_NAME, 'div')
        for button in buttons:
            if button.text == "Publicar":
               publish_button = button
               break
        return publish_button

    def check_comments_enabled(self):
        driver = self.driver
        inputs = driver.find_element(By.CLASS_NAME, '_7UhW9 ')
        disabled_text = 'Os comentários nesta publicação foram limitados.'
        for input in inputs:
            if disabled_text in input.text:
                return False
        return True        

    def get_text_area(self):
        driver = self.driver
        field = driver.find_element(By.TAG_NAME, 'textarea')
        return field

    def comentar_curtir(self, comentario, pic_href, seguir=True, reload_page=True, cascatear=False, like_comments=False):
        driver = self.driver
        if reload_page:
            driver.get(pic_href)
            self.__randomSleep__(3,5)
        else:
            driver.execute_script(self.selectors["scroll_to"])
        try:
            #self.like_pic()
            if like_comments:
                self.curtir_comentarios()

            if comentario and self.check_comments_enabled():
                #
                #field.click()
                self.__randomSleep__(10,20)
                field = driver.find_element(By.XPATH, ".//*[@aria-label='Adicione um comentário...']")
                #driver.find_element(By.CLASS_NAME, 'Ypffh').click() # click the field to insert comment
                #field = driver.find_element(By.CLASS_NAME, 'Ypffh')
                field.click()
                field = self.get_text_area()
                field.clear()
                

                try:
                    self.typephrase(comentario, field) # insert comment typing each letter
                    publish_button = self.get_publish_button()
                    if publish_button:
                        publish_button.click()
                except Exception as e:
                    print(e)
                    driver.get(pic_href)
                    driver.execute_script(self.selectors["scroll_to"])

                self.OnAfterComment(InstaBot = self, textarea=field, comment=comentario)                                        
                self.__randomSleep__(380,420)

                if cascatear:
                    comments_div = driver.find_element(By.CSS_SELECTOR, '.XQXOT')
                    driver.execute_script(self.selectors["arguments_scroll_to"], comments_div)
                    self.countdown(3)                             
                    button_responder = driver.find_element(By.XPATH, '//button[contains(text(), "Responder")]')
                    button_responder.click()
                    self.countdown(3)
                    field.clear()

        except Exception as e:
            print(e)
            self.countdown(5)

    def text_to_number(self, str_numero):
        str_numero = str_numero.replace(' seguidores', '')
        str_numero = str_numero.replace(' seguindo', '')
        str_numero = str_numero.replace('.', '')
        if ',' in str_numero:
            str_numero = str_numero.replace('mil', '00')
            str_numero = str_numero.replace(',', '')
            str_numero = str_numero.replace('.','')

        str_numero = str_numero.rstrip()
        return int(str_numero)

    def go_to_account_url(self, account_name, sleep=False):
        driver = self.driver
        url = self.selectors["instagram"] + str(account_name)
        if not (url in driver.current_url):
            driver.get(url)
            self.countdown(5) 
        if sleep:
            self.__randomSleep__(3,5)       


    def get_following_followers_number(self, account_name, position):
        driver = self.driver
        self.go_to_account_url(account_name)
        elements = driver.find_element(By.CLASS_NAME, '_ac2a')
        num_seguidores = elements[position].get_attribute('title')
        num_seguidores = self.text_to_number(num_seguidores)
        return num_seguidores, elements[position]

    def get_following_number(self, account_name):
        return self.get_following_followers_number(account_name, 2)
    
    def get_followers_number(self, account_name):
        return self.get_following_followers_number(account_name, 1)

    def check_percentual_engagement(self, account_name):
        num_seguidores = self.get_followers_number(account_name)
        num_seguindo = self.get_following_number(account_name)
  
        return num_seguindo / num_seguidores


    def curtir_foto_perfil(self, account_name, max_count_likes = 1, comentario=None, like_comments = False, check_is_private=True):
        driver = self.driver
        self.go_to_account_url(account_name)
        if check_is_private and self.check_is_private_profile(account_name):
            return 0

        driver.execute_script(self.selectors["scroll_to"])
        self.countdown(3)
        hrefs = driver.find_elements(By.TAG_NAME, "a")
        pic_hrefs = [elem.get_attribute("href") for elem in hrefs]
        numero_fotos = self.count_pics(pic_hrefs)
        print(account_name + " fotos: " + str(numero_fotos))
        if numero_fotos == 0:
            return numero_fotos
            
        count = 0
        if numero_fotos < max_count_likes:
            max_count_likes = numero_fotos
        if max_count_likes > 0:    
            random_coment = random.randint(1, max_count_likes)    
        else: 
            random_coment = 1
        
        total_likes = random.randint(1,max_count_likes)
        for pic_href in pic_hrefs:
            if (not pic_href == None) and (pic_href.find('/p/') > 0) and (count <= total_likes):
                if random_coment == count:
                    self.comentar_curtir(comentario = comentario, pic_href = pic_href, seguir=False, like_comments=like_comments)
                else:
                    self.comentar_curtir(comentario = None, pic_href = pic_href, seguir=False, like_comments=like_comments)
                    self.__randomSleep__(10,20)
                count += 1
                
        return numero_fotos

    def count_pics(self, pic_hrefs):
        count = 0
        for pic_href in pic_hrefs:
            if (pic_href != None) and (pic_href.find('/p/') > 0):
                count += 1
        return count

    def turn_off_notifications(self):
        driver = self.driver
        notNowButton = WebDriverWait(driver, 15).until(
            lambda d: d.find_element(By.XPATH, '//button[text()="Agora não"]')
        )
        notNowButton.click()
        self.__randomSleep__(2,4)


    def enviar_dm_por_account(self, account_name, message):
        driver = self.driver
        self.go_to_account_url(account_name)        
        button = driver.find_element(By.XPATH, self.selectors["message_button"])
        button.click()
        self.__randomSleep__()

        try:   
            message_box = driver.find_element(By.XPATH, self.selectors["message_box"])
            message_box.send_keys(message)
            self.__randomSleep__()
            button_send = driver.find_element(By.XPATH, self.selectors["send_button"])
            button_send.click()
            self.__randomSleep__(5,10)
        except:
            pass

    def spam_post(self, post_url, comment):
        driver = self.driver
        driver.get(post_url)
        self.countdown(3)
        driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/ \
        div/form/textarea').click()
        driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/ \
        div/form/textarea').send_keys(comment)
        driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div/article/div[2]/section \
        [3]/div/form/button').click()
        self.__randomSleep__(17, 23)

    def enviar_pic(self, account_name, pic_href):
        driver = self.driver
        driver.get(pic_href)
        self.__randomSleep__()
        ## 'wp06b'
        send_button = driver.find_element(By.XPATH, self.selectors["send_button_2"])
        send_button.click()
        self.__randomSleep__()
        share_button = driver.find_element(By.XPATH, self.selectors["share_button"])
        share_button.click()
        self.__randomSleep__()
        input = driver.find_element(By.XPATH, self.selectors["input"])
        self.typephrase(account_name, input)  # insert comment typing each letter
        self.__randomSleep__()

        # Select user
        account = driver.find_element(By.XPATH, self.selectors["select_user"])

        account.click()
        self.__randomSleep__()

        send_button = driver.find_element(By.XPATH, self.selectors["send_button_3"])
        send_button.click()

    def unfollow(self, account_name):
        driver = self.driver
        self.go_to_account_url(account_name)        
        try:
            following_button = driver.find_element(By.XPATH, '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button')
        except:
            try:
                following_button = driver.find_element(By.XPATH, '/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button/div/span')
            except:                                             
                following_button = driver.find_element(By.XPATH, '/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button')
        following_button.click()
        self.__randomSleep__(2,10)
        unfollow_button = driver.find_element(By.XPATH, '//button[contains(text(), "Deixar de seguir")]')
        unfollow_button.click()
        self.__randomSleep__()

    def follow(self, account_name):
        driver = self.driver
        self.go_to_account_url(account_name)        
        
        try:
            follow_button = driver.find_element(By.XPATH, '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')
        except:
            try:
                follow_button = driver.find_element(By.XPATH, '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/span/span[1]/button')
            except:
                try:
                    follow_button = driver.find_element(By.XPATH, '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button')
                except:   
                    #follow_button para contas privadas 
                    follow_button = driver.find_element(By.XPATH, '/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button')

        follow_button.click()
        self.__randomSleep__()
    
    def getAccountsfromStringToList(self, string, accounts, page, file_name):
        if page == 'followers':   
            string = string.replace('Seguidores', '')
        else:
            string = string.replace('Seguindo', '')

        listRes = list(string.split("\n"))

        if len(accounts) == 0:
            if (len(listRes) > 0) and (listRes[0] == ''):
                listRes.pop(0)
        i = len(accounts)
        capturar = True
        for elem in listRes:
            if (capturar) and (not elem in accounts):
                elem = str(elem).replace('Seguir', '')
                elem = elem.encode('utf-8').split()
                accounts.append(elem)
                i += 1
                if len(elem) > 0:
                    self.OnGetFollowAccount(InstaBot = self, page = page, file_name = file_name, number=i, account=elem[0])
            capturar = True if elem == 'Seguir' else False
        return accounts



    def get_followers_following(self, account, page, file_name):
        driver = self.driver
        pos = 1 if page == 'followers' else 2
        followers_ing, button = self.get_following_followers_number(account, pos)
        button.click()
        self.countdown(3)
        self.countdown(2)
        accounts_list = []
        num = 0
        while True:
            panels_container = self.driver.find_element(By.CLASS_NAME, '_aano')
            panels = panels_container.find_element(By.TAG_NAME, 'div')
            panels = panels[0]
            panels_labels = panels.text.split('\n')
            idx = 0
            for panel in panels_labels:
                if (panel == 'Seguir'):
                    if not [panels_labels[idx-2], panels_labels[idx-1]] in accounts_list: 
                        num += 1
                        accounts_list.append([panels_labels[idx-2], panels_labels[idx-1]])
                        last_panel = panels_container.find_element(By.XPATH, f"//*[text()='{panels_labels[idx-2]}']")[0]
                        self.OnGetFollowAccount(InstaBot = self, page = page, number=num, account=panels_labels[idx-2], name=panels_labels[idx-1], file_name=file_name)
                        driver.execute_script(self.selectors["arguments_scroll_to"], last_panel) 
                        self.countdown(0.5)
                idx += 1        

            
            self.countdown(10)

            if followers_ing  == num:
                break
        return accounts_list    
        

    def get_followers(self, account, file_name=""):
        self.get_followers_following(account, 'followers', file_name)

    def get_following(self, account, file_name=""):
        self.get_followers_following(account, 'following', file_name)

    def extract_numbers(self, text):
        numbers = [int(word) for word in text.split() if word.isdigit()]
        return numbers[len(numbers)-1]

    def get_mutual_friends_number(self, account_name):
        driver = self.driver
        self.go_to_account_url(account_name)
        mutual = driver.find_element(By.XPATH, '/html/body/div[1]/section/main/div/header/section/div[2]/a/span') #e outras 344 pessoas
        mutual_text = mutual.text
        return self.extract_numbers(mutual_text)

    def get_accounts(self, file, shuffle_=False):
        lines = []
        with open(file, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter = ';')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                lines.append(row["account"])
        if shuffle_:
            shuffle(lines)        
        lines = set(lines)
        return lines

    def write_csv(self, file_name, account):
        account_str = str(account.rstrip())

        file_exists = os.path.isfile(file_name)
        if not file_exists:
            f = open(file_name,'w+') 
            f.write('account')
            f.write(account_str)
            f.close()
        else: 
            with open(file_name, mode='a+') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=';')
                csv_writer.writerow([account_str])
            csv_file.close()    


    def send_group_message(self, users, message):
        driver = self.driver
        logging.info(f'Send group message {message} to {str(users)}')
        try:
            self.turn_off_notifications()
        except:
            pass
        driver.get(self.selectors["instagram"] + 'direct/new/')
        try:
            self.turn_off_notifications()
        except:
            pass

        searchInput = self.driver.find_element(By.NAME, self.selectors['search_user'])
        usersAndMessages = []
        for user in users:
            searchInput.send_keys(user)
            self.__randomSleep__()

            # Select user
            try:
                element=driver.find_element(By.XPATH, f"//div[text()='{user}']")
                user_click=element.click()
            except:
                searchInput.clear()
                pass    
            self.__randomSleep__(2, 4)
        
        # Go to page
        self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div[2]/div/button").click()
        self.__randomSleep__()
        self.driver.find_element(By.XPATH, "*//textarea")[0].send_keys(message)
        self.__randomSleep__()
        buttons = self.driver.find_elements(By.CSS_SELECTOR, self.selectors['send'])
        buttons[len(buttons)-1].click()

        self.__randomSleep__()
        self.driver.get('https://www.instagram.com')


    def __randomSleep__(self, min = 2, max = 5):
        t = random.randint(min, max)
        logging.info('Wait {} seconds'.format(t))
        self.countdown(t)

    def check_is_private_profile(self, account_name):
        driver = self.driver
        self.go_to_account_url(account_name, True)
        private_check = driver.find_elements(By.XPATH, f"//*[text()='Esta conta é privada']")
        return len(private_check) > 0

    def check_is_unavailable(self, account_name):
        driver = self.driver
        self.go_to_account_url(account_name, True)
        unavailable_check = driver.find_elements(By.XPATH, "//*[text()='Esta página não está disponível.']")
        return len(unavailable_check) > 0

    def get_bio(self, account_name):
        driver = self.driver
        self.go_to_account_url(account_name, True)
        bio = ''
        try:                                    
            bio = driver.find_element(By.XPATH, '/html/body/div[1]/section/main/div/header/section/div[2]/span')
            bio = bio.text
        except:
            pass
            
        return bio

    def add_subscribers_for_likes_in_pic(self,objMethod): 
        self.OnGetAccountInLikes += objMethod         

    def remove_subscribers_for_likes_in_pic(self,objMethod): 
        self.OnGetAccountInLikes -= objMethod         

    def add_subscribers_for_follow_accounts(self,objMethod): 
        self.OnGetFollowAccount += objMethod         

    def remove_subscribers_for_follow_accounts(self,objMethod): 
        self.OnGetFollowAccount -= objMethod   

    def add_subscribers_for_after_comment(self,objMethod): 
        self.OnAfterComment += objMethod         

    def remove_subscribers_for_after_comment(self,objMethod): 
        self.OnAfterComment -= objMethod   


    def get_likes_in_pic_href(self, pic_href):
        driver = self.driver
        driver.get(pic_href)
        self.__randomSleep__(10,15)
        nro_curtidas = driver.find_element(By.XPATH, '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div[2]/button/span')
        print(nro_curtidas.text)
        nro_curtidas = int(nro_curtidas.text)
        self.__randomSleep__(10,15)
        button = driver.find_element(By.XPATH, '/html/body/div[1]/section/main/div/div/article/div[3]/section[2]/div/div[2]/button')
        button.click()
        self.__randomSleep__(5,10)
        accounts = []
        controle = 1
        for i in range(1, nro_curtidas):                  
           try:
               scr1 = driver.find_element(By.XPATH, f'/html/body/div[4]/div/div/div[2]/div/div/div[{controle}]')
               driver.execute_script(self.selectors["arguments_scroll_to"], scr1)
               self.countdown(1)
               text = scr1.text
               list = text.encode('utf-8').split()
               account = str(list[0].decode("utf-8"))
               accounts.append(account)
               self.OnGetAccountInLikes(number=i, account=account)               
               controle += 1
               if (controle % 16) == 0:
                   controle = 2
           except NoSuchElementException:
               pass

        return accounts

    def save_accounts_to_file(self, file_name, accounts):
        f = open(file_name,'w')
        f.write('account\n')
        for account in accounts:
            f.write(account)
        f.close()

    def is_blocked(self):
        driver = self.driver
        trylater = driver.find_element(By.CLASS_NAME, "_aacl")
        blocked = False
        for elem in trylater:
            if elem.text == 'Tente novamente mais tarde':
                blocked = True
                break    
        return blocked    




        
