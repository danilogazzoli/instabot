from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
from pyvirtualdisplay import Display
from selenium.webdriver.support.ui import WebDriverWait
from datetime import date
from datetime import datetime
from datetime import timedelta
import os
import csv
from selenium.common.exceptions import NoSuchElementException
import logging
from random import shuffle

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
        self.display = None
        self.count_likes = 0
        self.driver = webdriver.Firefox(executable_path=executable_path)  # Coloque o caminho para o seu geckodriver aqui

        self.OnGetAccountInLikes=Event() 

        self.OnGetFollowAccount=Event() 

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
          "follower_number": "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span",
          "message_button": "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/button",
          "message_box": "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea",
          "send_button_2": "/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/button",
          "send_button":   "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]/button",
          "send_button_3": "/html/body/div[5]/div/div/div[1]/div/div[2]/div/button",
          "arguments_scroll_to": "arguments[0].scrollIntoView();",
          "share_button": "/html/body/div[4]/div/div/div/div[2]/div/div[1]/div/div",
          "input": "/html/body/div[5]/div/div/div[2]/div[1]/div/div[2]/input",
          "select_user": "/html/body/div[5]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div",


        }


    def display_start(self):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()

    def display_stop(self):
        self.display.stop()

    def login(self):
        driver = self.driver
        driver.get(self.selectors["instagram"])
        self.countdown(3)
        try:
            login_button = driver.find_element_by_xpath(self.selectors["login"] )
            login_button.click()
        except:
            pass

        user_element = driver.find_element_by_xpath(self.selectors["username_field"])
        user_element.clear()
        self.__randomSleep__(4,6)
        user_element.send_keys(self.username)
        self.__randomSleep__(4,6)
        password_element = driver.find_element_by_xpath(self.selectors["password_field"])
        password_element.clear()
        password_element.send_keys(self.password)
        self.__randomSleep__(4,6)
        password_element.send_keys(Keys.RETURN)
        self.__randomSleep__(4,6)

    def curtir_fotos_com_a_hashtag(self, hashtag):
        if (self.count_likes > 0) and (self.count_likes % 200 == 0):
            print('já atingiu o limite de curtidas')
            self.countdown(60 * 10)
            self.count_likes += 1
            return

        driver = self.driver
        driver.get(self.selectors["instagram"] + "explore/tags/" + hashtag + "/")
        self.countdown(5)
        for i in range(1, 9):  # Altere o segundo valor aqui para que ele desça a quantidade de páginas que você quiser: quer que ele desça 5 páginas então você deve alterar de range(1,3) para range(1,5)
            driver.execute_script(self.selectors["scroll_to"])
            self.countdown(3)
        hrefs = driver.find_elements_by_tag_name("a")
        pic_hrefs = [elem.get_attribute("href") for elem in hrefs]
        print(hashtag + " fotos: " + str(len(pic_hrefs)))

        for pic_href in pic_hrefs:
            try:
                pic_href.index(self.selectors["instagram"] + "p")
            except ValueError as err:
                print("pulando link inválido")
                continue
            driver.get(pic_href)
            driver.execute_script(self.selectors["scroll_to"])
            try:
                self.__randomSleep__(1,2)
                button_seguindo = driver.find_element_by_xpath(self.selectors['following_button'] )

                print(button_seguindo.text)
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

        like_button = driver.find_element_by_xpath(self.selectors["like_button"])
        if 'aria-label="Curtir"' in like_button.get_attribute("innerHTML"):
            like_button.click()

    def comentar_curtir(self, comentario, pic_href, seguir=True, reload_page=True, cascatear=False):
        driver = self.driver
        if reload_page:
            driver.get(pic_href)
        driver.execute_script(self.selectors["scroll_to"])
        try:
            #driver.find_element_by_class_name('v1Nh3').click()  # click on photo to open and upload

            self.like_pic()

            if comentario:
                driver.find_element_by_class_name('Ypffh').click() # click the field to insert comment
                field = driver.find_element_by_class_name('Ypffh')
                field.clear()

                try:
                    self.typephrase(comentario, field) # insert comment typing each letter
                    driver.find_element_by_xpath('//button[contains(text(), "Publicar")]').click() # click the post 'comment' button element
                except Exception as e:
                    print(e)
                    driver.get(pic_href)
                    driver.execute_script(self.selectors["scroll_to"])
                
                self.__randomSleep__(380,420)

                if cascatear:
                    comments_div = driver.find_element_by_css_selector('.XQXOT')
                    driver.execute_script(self.selectors["scroll_to"], comments_div)
                    self.countdown(3)                             
                    button_responder = driver.find_element_by_xpath('//button[contains(text(), "Responder")]')
                    button_responder.click()
                    self.countdown(3)
                    field.clear() 

        except Exception as e:
            print(e)
            self.countdown(5)
            raise

    def text_to_number(self, str_numero):
        if ',' in str_numero:
             str_numero = str_numero.replace('mil', '00')
             str_numero = str_numero.replace(',', '')
        str_numero = str_numero.replace('.','')

        str_numero = str_numero.rstrip()
        return int(str_numero)

    def go_to_account_url(self, account_name):
        driver = self.driver
        url = self.selectors["instagram"] + str(account_name)
        if driver.current_url != url:
            driver.get(url)
        self.countdown(5)    

    def get_following_number(self, account_name):
        driver = self.driver
        self.go_to_account_url(account_name)
        try:
            seguindo = driver.find_element_by_xpath(self.selectors["following_number"])
            num_seguindo = seguindo.text
        except:
            num_seguindo = '0'

        num_seguindo = self.text_to_number(num_seguindo)
        return num_seguindo
    
    def get_followers_number(self, account_name):
        driver = self.driver
        self.go_to_account_url(account_name)
        seguidores = driver.find_element_by_xpath(self.selectors["follower_number"]) 
        num_seguidores = seguidores.get_attribute('title')
        num_seguidores = self.text_to_number(num_seguidores)
        return num_seguidores
    
    def check_percentual_engagement(self, account_name):
        num_seguidores = self.get_followers_number(account_name)
        num_seguindo = self.get_following_number(account_name)
  
        return num_seguindo / num_seguidores


    def curtir_foto_perfil(self, account_name, max_count_likes = 1, comentario=None):
        driver = self.driver
        self.go_to_account_url(account_name)
        driver.execute_script(self.selectors["scroll_to"])
        self.countdown(3)
        hrefs = driver.find_elements_by_tag_name("a")
        pic_hrefs = [elem.get_attribute("href") for elem in hrefs]
        numero_fotos = len(pic_hrefs)
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
            if (pic_href.find('/p/') > 0) and (count <= total_likes):
                if random_coment == count:
                    self.comentar_curtir(comentario = comentario, pic_href = pic_href, seguir=False)
                else:
                    self.comentar_curtir(comentario = None, pic_href = pic_href, seguir=False)    
                count += 1
                self.__randomSleep__(10,20)
        return numero_fotos

    def turn_off_notifications(self):
        driver = self.driver
        notNowButton = WebDriverWait(driver, 15).until(
            lambda d: d.find_element_by_xpath('//button[text()="Agora não"]')
        )
        notNowButton.click()
        self.__randomSleep__(2,4)


    def enviar_dm_por_account(self, account_name, message):
        driver = self.driver
        self.go_to_account_url(account_name)        
        button = driver.find_element_by_xpath(self.selectors["message_button"])
        button.click()
        self.__randomSleep__()

        try:   
            message_box = driver.find_element_by_xpath(self.selectors["message_box"])
            message_box.send_keys(message)
            self.__randomSleep__()
            button_send = driver.find_element_by_xpath(self.selectors["send_button"])
            button_send.click()
            self.__randomSleep__(5,10)
        except:
            pass

    def spam_post(self, post_url, comment):
        driver = self.driver
        driver.get(post_url)
        self.countdown(3)
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/ \
        div/form/textarea').click()
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section[3]/ \
        div/form/textarea').send_keys(comment)
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[2]/section \
        [3]/div/form/button').click()
        self.__randomSleep__(17, 23)

    def enviar_pic(self, account_name, pic_href):
        driver = self.driver
        driver.get(pic_href)
        self.__randomSleep__()
        ## 'wp06b'
        send_button = driver.find_element_by_xpath(self.selectors["send_button_2"])
        send_button.click()
        self.__randomSleep__()
        share_button = driver.find_element_by_xpath(self.selectors["share_button"])
        share_button.click()
        self.__randomSleep__()
        input = driver.find_element_by_xpath(self.selectors["input"])
        self.typephrase(account_name, input)  # insert comment typing each letter
        self.__randomSleep__()

        # Select user
        account = driver.find_element_by_xpath(self.selectors["select_user"])

        account.click()
        self.__randomSleep__()

        send_button = driver.find_element_by_xpath(self.selectors["send_button_3"])
        send_button.click()

    def unfollow(self, account_name):
        driver = self.driver
        self.go_to_account_url(account_name)        
        try:
            following_button = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button')
        except:
            try:
                following_button = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button/div/span')
            except:                                             
                following_button = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button')
        following_button.click()
        self.__randomSleep__(2,10)
        unfollow_button = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[1]')
        unfollow_button.click()
        self.__randomSleep__()

    def follow(self, account_name):
        driver = self.driver
        self.go_to_account_url(account_name)        
        
        try:
            follow_button = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button')
        except:
            try:
                follow_button = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/span/span[1]/button')
            except:
                try:
                    follow_button = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/div/span/span[1]/button')
                except:   
                    #follow_button para contas privadas 
                    follow_button = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div/button')

        follow_button.click()
        self.__randomSleep__()

    def get_followers_following(self, account, page, count, file_name):
        self.turn_off_notifications
        self.countdown(3)
        driver = self.driver
        driver.get(self.selectors["instagram"] + account)
        self.countdown(2)
        driver.find_element_by_xpath('//a[contains(@href, "%s")]' % page).click()
        scr2 = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a')
        self.countdown(2)
        text1 = scr2.text
        print(text1)
        x = datetime.now()
        print(x)
        for i in range(1,count):                  
            try:                                   
               scr1 = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/ul/div/li[%s]' % i)
               driver.execute_script(self.selectors["arguments_scroll_to"], scr1)
               self.countdown(1)
               text = scr1.text
               list = text.encode('utf-8').split()
               account = str(list[0].decode("utf-8"))
               self.OnGetFollowAccount(number=i, account=account)  

            except NoSuchElementException:
               pass


    def get_followers(self, account, count, file_name=""):
        self.get_followers_following(account, 'followers', count, file_name)

    def get_following(self, account, count, file_name=""):
        self.get_followers_following(account, 'following', count, file_name)

    def extract_numbers(self, text):
        numbers = [int(word) for word in text.split() if word.isdigit()]
        return numbers[len(numbers)-1]

    def get_mutual_friends_number(self, account_name):
        driver = self.driver
        self.go_to_account_url(account_name)
        mutual = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[2]/a/span') #e outras 344 pessoas
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
            f.open(file_name,'w') 
            f.write(account_str)
            f.close()
        else: 
            with open(file_name, mode='a') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=';')
                csv_writer.writerow([account_str])


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

        searchInput = self.driver.find_element_by_name(self.selectors['search_user'])
        usersAndMessages = []
        for user in users:
            searchInput.send_keys(user)
            self.__randomSleep__()

            # Select user
            try:
                element=driver.find_element_by_xpath(f"//div[text()='{user}']")
                user_click=element.click()
            except:
                searchInput.clear()
                pass    
            self.__randomSleep__(2, 4)
        
        # Go to page
        self.driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/div/div[2]/div/button").click()
        self.__randomSleep__()
        self.driver.find_elements_by_xpath("*//textarea")[0].send_keys(message)
        self.__randomSleep__()
        buttons = self.driver.find_elements_by_css_selector(self.selectors['send'])
        buttons[len(buttons)-1].click()

        self.__randomSleep__()
        self.driver.get('https://www.instagram.com')


    def __randomSleep__(self, min = 2, max = 5):
        t = random.randint(min, max)
        logging.info('Wait {} seconds'.format(t))
        self.countdown(t)

    def check_is_private_profile(self, account_name):
        driver = self.driver
        self.go_to_account_url(account_name)
        try:
            private_check = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/article/div[1]/div/h2')
            return private_check.text == 'Esta conta é privada'
        except:
            return False


    def get_bio(self, account_name):
        driver = self.driver
        self.go_to_account_url(account_name)
        bio = ''
        try:                                    
            bio = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/div[2]/span')
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

    def get_likes_in_pic_href(self, pic_href):
        driver = self.driver
        driver.get(pic_href)
        self.__randomSleep__(10,15)
        nro_curtidas = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div[2]/button/span')
        print(nro_curtidas.text)
        nro_curtidas = int(nro_curtidas.text)
        self.__randomSleep__(10,15)
        button = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/article/div[3]/section[2]/div/div[2]/button')
        button.click()
        self.__randomSleep__(5,10)
        accounts = []
        controle = 1
        for i in range(1, nro_curtidas):                  
           try:
               scr1 = driver.find_element_by_xpath(f'/html/body/div[4]/div/div/div[2]/div/div/div[{controle}]')
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




        