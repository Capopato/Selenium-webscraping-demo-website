from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

website = 'http://automationpractice.com/'
PATH = '/Users/tom/Desktop/Chrome_driver_(Python selenium)/chromedriver'  # Path to the chromedriver file
driver = webdriver.Chrome(PATH)
driver.maximize_window()


class Auto_Script:
    def enter_details (self):
        # information
        fn = 'Willlem'
        ln = 'Inhuis'
        e = 'test123424655432342344@gmail.com'
        pasw = 'test12345'
        add = 'teststraat 1'
        cit = 'Amsterdam'
        pc = '10000'
        mp = '0612345678'

        # Open website
        driver.get(website)

        # Click on sign-up button to either login or sign-up
        # driver.implicitly_wait(5)

        wait_sign_up = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@class='login']"))
        )
        sign_up = driver.find_element(By.XPATH, "//a[@class='login']")
        sign_up.click()
        # driver.implicitly_wait(5)

        # Fill in email details
        # wait_email_create = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.ID, 'email_create'))
        # )
        email_create = driver.find_element(By.ID, 'email_create')
        email_create.send_keys(e)
        create_button = driver.find_element(By.ID, 'SubmitCreate')
        create_button.click()

        # If load to next page means no account exist with the email adres.
        # Auto fill sign-up page
        try:
            # driver.implicitly_wait(10)
            # wait_gender = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.ID, 'id_gender1'))
            # )
            gender = driver.find_element(By.ID, 'id_gender1')
            first_name = driver.find_element(By.ID, 'customer_firstname')
            first_name.send_keys(fn)
            last_name = driver.find_element(By.ID, 'customer_lastname')
            last_name.send_keys(ln)
            password = driver.find_element(By.ID, 'passwd')
            password.send_keys(pasw)

            # Date of birth
            dropdown_day = Select(driver.find_element(By.ID, 'days'))
            dropdown_day.select_by_value('14')
            dropdown_month = Select(driver.find_element(By.ID, 'months'))
            dropdown_month.select_by_value('8')
            dropdown_year = Select(driver.find_element(By.ID, 'years'))
            dropdown_year.select_by_value('1995')

            # Adress
            firstname = driver.find_element(By.ID, 'firstname')
            firstname.send_keys(fn)
            lastname = driver.find_element(By.ID, 'lastname')
            lastname.send_keys(ln)
            adress = driver.find_element(By.ID, 'address1')
            adress.send_keys(add)
            city = driver.find_element(By.ID, 'city')
            city.send_keys(cit)
            dropdown_county = Select(driver.find_element(By.ID, 'id_country'))
            dropdown_county.select_by_value('21')
            dropdown_state = Select(driver.find_element(By.ID, 'id_state'))
            dropdown_state.select_by_value('32')
            postcode = driver.find_element(By.ID, 'postcode')
            postcode.send_keys(pc)
            phone = driver.find_element(By.ID, 'phone_mobile')
            phone.send_keys(mp)
            adress_2 = driver.find_element(By.ID, 'alias')
            adress_2.send_keys(add)
            register = driver.find_element(By.ID, 'submitAccount')
            register.click()

        # If error is raised that account already exist.
        # Use login information to login.
        except NoSuchElementException:
            account_exists = driver.find_element(By.XPATH, "//div[@class='alert alert-danger']")
            login_email = driver.find_element(By.ID, 'email')
            login_email.send_keys(e)
            login_passwd = driver.find_element(By.ID, 'passwd')
            login_passwd.send_keys(pasw)
            submitlogin = driver.find_element(By.ID, 'SubmitLogin')
            submitlogin.click()


    def products(self):
        # Go to product page
        wait_product_page = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@title='Women']"))
        )
        to_product_page = driver.find_element(By.XPATH, "//a[@title='Women']")
        to_product_page.click()

        # Make list of all products (for index)
        wait_products = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='right-block']"))
        )
        products = []
        products = driver.find_elements(By.XPATH, "//div[@class='right-block']")

        index = 0  # Set index for list

        # Variables for database
        name = []
        reference = []
        condition = []
        description = []
        price = []

        while index < 7:
            for product in products:
                if index < 7:
                    # Click on product
                    click_to_product = driver.find_elements(By.XPATH, "//a[@class='button lnk_view btn btn-default']")[
                        index]
                    click_to_product.click()

                    # Get information
                    # print(index)
                    name.append(driver.find_element(By.TAG_NAME, 'h1').text)
                    # pr  Faded Short Sleeve T-shirts  ...  $16.51
                    # 1                       Blouse  ...  $27.00
                    # 2                Printed Dress  ...  $26.00
                    # 3                Printed Dress  ...  $50.99
                    # 4         Printed Summer Dress  ...  $28.98
                    # 5         Printed Summer Dress  ...  $30.50
                    # 6int(name)
                    reference.append(driver.find_element(By.XPATH, "//span[@itemprop='sku']").text)
                    # print(reference)
                    condition.append(driver.find_element(By.ID, "product_condition").text)
                    # print(condition)
                    description.append(driver.find_element(By.XPATH, "//div[@itemprop='description']").text)
                    # print(description)
                    price.append(driver.find_element(By.ID, 'our_price_display').text)
                    # print(price)
                    driver.back()
                    index += 1
                    continue
                else:
                    break
            break

        driver.quit()

        df = pd.DataFrame(
            {'Name': name, 'Reference': reference, 'Condition': condition, 'Description': description, 'Price': price})
        df.to_csv('test.csv', index=False)
        print(df)