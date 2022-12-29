import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

chrome_options = Options()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
url = 'https://www.linkedin.com/jobs/search/?currentJobId=3404030355&f_AL=true&geoId=103644278&keywords=python%20developer&location=United%20States&refresh=true'
driver.get(url)


def sign_in():
    sign_in_button = driver.find_element(By.XPATH, '/html/body/div[1]/header/nav/div/a[2]')
    ActionChains(driver).move_to_element(sign_in_button).click(sign_in_button).perform()
    email_input = driver.find_element(By.XPATH, '//*[@id="username"]')
    email_input.send_keys(os.environ['EMAIL'])
    pass_input = driver.find_element(By.XPATH, '//*[@id="password"]')
    pass_input.send_keys(os.environ['PASSWORD'])
    enter_button = driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')
    enter_button.click()


def gather_jobs():
    job_list = driver.find_elements(By.CSS_SELECTOR, '.job-card-container--clickable div')
    for job in job_list[0:1]:
        # click link
        ActionChains(driver).move_to_element(job).click(job).perform()
        # click apply
        # apply_button = driver.find_element(By.CSS_SELECTOR, '.jobs-apply-button button')


        # in case recommended skills - click done
        try:
            time.sleep(2)
            done_button = driver.find_element(By.CSS_SELECTOR, '.jobs-skill-match-modal__footer button')
            ActionChains(driver).move_to_element(done_button).click(done_button).perform()
        except NoSuchElementException:
            print("done button not found")
            pass

        # fill out actual application
        # requires the following pop-ups in order
        # Contact Info -> Resume -> Review
        try:
            time.sleep(2)
            apply_button = driver.find_element(By.CSS_SELECTOR, '.jobs-s-apply div')
            ActionChains(driver).move_to_element(apply_button).click(apply_button).perform()
            time.sleep(3)
            # click next
            next_button = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[2]/form/footer/div[2]/button')
            ActionChains(driver).move_to_element(next_button).click(next_button).perform()
            # choose resume
            choose_button = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[2]/form/div/div/div/div[1]/div/div[2]/div/div[2]/button[1]/span')
            ActionChains(driver).move_to_element(choose_button).click(choose_button).perform()
            # review application
            review_button = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[2]/form/footer/div[2]/button[2]/span')
            ActionChains(driver).move_to_element(review_button).click(review_button).perform()
            # submit application
            submit_button = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div[2]/div/footer/div[3]/button[2]/span')
            ActionChains(driver).move_to_element(submit_button).click(submit_button).perform()
        except NoSuchElementException:
            print("non standard format, passed")
            pass


# Perform function
sign_in()
gather_jobs()
