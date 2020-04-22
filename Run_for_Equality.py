#! /usr/bin/env python3

'''
Author: Peter Stulpner, pstulpner@student.unimelb.edu.au
Purpose of this script is to automate the filling of the form required to log
runs for the intercollegiate Run for Equity Challeneg
'''

from selenium import webdriver
from time import sleep
from datetime import date as dt
from PIL import Image
from io import BytesIO
import os

try:
    os.chdir(r"C:\Users\peter\OneDrive\Desktop\Python Projects\Run_for_Equality")
except OSError:
    pass


def main():
    # Load a chrome window:
    print("Run_for_Equality version 1.0 - Peter Stulpner\n Running\n")
    print("Current diretory: \n")
    print(os.getcwd())

    date_today = dt.today()
    date_display = date_today.strftime("%d%m%y")
    date_display = date_display[:4] + '20' + date_display[4:]
    print(date_display)

    driver = webdriver.Chrome()

    distance = get_latest_run(driver, date_display)
    log_in("pstulpnerRunForEquality@gmail.com", "PeterS3700", driver)
    Run_for_EqualityForm(driver, date_display, distance)

    driver.close()


def log_in(username, password, driver):
    '''Function takes input of username, password and a webdriver to log in to
    a google account '''
    # Load google
    driver.get("https://google.com")

    # Sign into google account:
    sign_in = driver.find_element_by_link_text("Sign in")
    sign_in.click()

    print("Signing in to Google")
    sleep(2)

    enter_email = driver.find_element_by_name("identifier")
    enter_email.send_keys(username)
    print("Email entered")

    next = driver.find_element_by_xpath("//*[@id='identifierNext']/span/span")
    next.click()


    sleep(2)

    enter_pw = driver.find_element_by_name("password")
    enter_pw.send_keys(password)

    next = driver.find_element_by_xpath("//*[@id='passwordNext']/span/span")
    next.click()
    print("Password Entered")
    sleep(2)
    return print("Log in Complete")


def get_latest_run(driver, date_display):
    '''Function takes input of the current date and the driver and gets
    the latest activity distance covered and takes a screenshot of the
    activity  '''

    # Go to athlete
    driver.get("https://www.strava.com/athletes/18110314")
    sleep(5)

    # Get distance
    print("Retrieving distance")
    run_dist = driver.find_element_by_xpath("/html/body/div[3]/main/div[2]/div/div[2]/ol/li[1]/div[1]/div[2]/div[2]/ul/li[1]/div/div").text
    print(f"Latest run was: {run_dist}")

    # Save screenshot to Images sub-folder
    print("Getting run screenshot")
    os.chdir(r"C:\Users\peter\OneDrive\Desktop\Python Projects\Run_for_Equality\Images")
    activity_frame = driver.find_element_by_xpath("/html/body/div[3]/main/div[2]/div/div[2]/ol/li[1]").screenshot("run" + date_display + ".png")
    os.chdir(r"C:\Users\peter\OneDrive\Desktop\Python Projects\Run_for_Equality")

    print("Success")

    return run_dist

def Run_for_EqualityForm(driver, date_display, distance):
    print("Opening Form")
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSczjEak8ZGxYidFQIxEi7b3dG-v_9oPkRW1lJiV_jZJ4iKiyA/viewform")

    print("Entering name")
    name = driver.find_element_by_xpath("//*[@id='mG61Hd']/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/div[1]/input")
    name.send_keys("Peter Stulpner")

    print("Entering College")
    college = driver.find_element_by_xpath("//*[@id='mG61Hd']/div/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/input")
    college.send_keys("St Hilda's")

    print("Entering Date:")
    date = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div/div[2]/div[3]/div/div[2]/div/div[2]/div[1]/div/div[1]/input')
    date.send_keys(date_display)

    print("Entering run distance")
    run_distance = driver.find_element_by_xpath("//*[@id='mG61Hd']/div/div/div[2]/div[4]/div/div[2]/div/div[1]/div/div[1]/input")
    run_distance.send_keys(distance)

    print("Uploading image")
    upload_image(driver, date_display)
    sleep(20)

    print("Submitting")
    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div/div/div[3]/div[1]/div/div')
    submit_button.click()
    print("complete")





def upload_image(driver, date_display):
    # Find the upload image button
    file_upload = driver.find_element_by_xpath("//*[@id='mG61Hd']/div/div/div[2]/div[5]/div/div[3]")
    # Image filename
    file_name = 'run' + date_display + '.png'
    file_upload.click()
    sleep(5)
    # Switch frames
    iframe = driver.find_element_by_class_name('picker-frame')
    sleep(2)
    driver.switch_to.frame(iframe)
    sleep(1)
    input_field = driver.find_element_by_xpath('//input[@type="file"]')
    sleep(1)
    file_url = r"\Images" + "\\"  + file_name
    input_field.send_keys(os.getcwd() + file_url)
    upload = driver.find_element_by_id("picker:ap:0")
    upload.click()
    driver.switch_to.default_content()




if __name__ == "__main__":
    main()
