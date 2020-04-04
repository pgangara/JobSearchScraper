import selenium

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import numpy as np
import os
os.chdir(r"Directory")

def pull_jobs(url,num_jobs):
    jobs = []
    while len(jobs)< num_jobs:
        driver.get(url)
        time.sleep(10)# to load the page
        try:
            driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(10)

        try:
            #wait = driver.WebDriverWait(driver,10).until(EC.presence_of_element_located(By.CLASS_NAME,'ModalStyle__xBtn___29PT9'))
            driver.find_element_by_xpath('//*[@id="JAModal"]/div/div[2]/span/svg').click()  #clicking to the X.
        except NoSuchElementException:
            pass
        time.sleep(10)
        job_buttons = driver.find_elements_by_class_name("jl")
        for job_button in job_buttons:
            if len(jobs)>= num_jobs:
                break
            job_button.click()
            time.sleep(1)
            collected_successfully = False

            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
                    location = driver.find_element_by_xpath('.//div[@class="location"]').text
                    job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                salary_estimate = driver.find_element_by_xpath('.//span[@class="gray small salary"]').text
            except NoSuchElementException:
                salary_estimate = -1
            try:
                rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
            except NoSuchElementException:
                rating = -1

            jobs.append({"Job Title" : job_title,
                        "Salary Estimate" : salary_estimate,
                        "Job Description" : job_description,
                        "Rating" : rating,
                        "Company Name" : company_name,
                        "Location" : location})
        try:
            driver.find_element_by_xpath('.//li[@class="next"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)

if __name__ == '__main__':
  options = webdriver.ChromeOptions()
  driver = webdriver.Chrome(executable_path=r"chromedriver.exe", options=options)
  driver.set_window_size(1120, 1000)
  url_format = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword={}&sc.keyword={}&locT=C&locId={}&jobType=all&fromAge=1"
  url_dict = [{"Location": 'Asutin',"URL":'1139761'},
            {"Location": 'Raleigh',"URL":'1138960'},
            {"Location": 'Charlotte',"URL":'1138644'},
            {"Location": 'St.Louis',"URL":'1162348'},
            {"Location": 'Houston',"URL":'1140171'},
            {"Location": 'Salt Lake city',"URL":'1128289'},
            {"Location": 'Overland Park',"URL":'1151049'},
            {"Location": 'Orlando',"URL":'1154247'},
            {"Location": 'Nashville',"URL":'1144541'}]
  keyword = "Data+Scientist+"
  jobs_to_apply = pd.DataFrame()
  for i in range(0,len(url_dict)):
      jobs_to_apply.append(pull_jobs(url_format.format(keyword,keyword,url_dict[i]['URL']),10))

