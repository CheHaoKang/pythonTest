# -*- coding: UTF-8 -*-

from selenium import webdriver
import sys

if __name__ == "__main__":
    driver = webdriver.PhantomJS(service_args=["--remote-debugger-port=9000"])
    driver.implicitly_wait(10)
    driver.get("http://www.gatherproxy.com/proxylist/anonymity/?t=Elite")

    # driver.find_element_by_css_selector("#lst-ib").send_keys("google")
    driver.find_element_by_css_selector("input[class='button']").click()
    print(driver.page_source)
    print('=================================')

    try:
        i = 1;
        while True:
            driver.find_element_by_xpath("//form[@id='psbform']/div[@class='pagenavi']/a[" + str(i) + "]").click()
            print(driver.page_source)
            print('=================================')
            i += 1
    except:
        print("Unexpected error:", sys.exc_info())


    # driver.find_element_by_css_selector("#id .pagenavi a")
    # print(driver.find_element_by_xpath("//form[@id='psbform']/div[@class='pagenavi']/a[1]"))


    # driver.find_element_by_id("Username").send_keys("deckenkang6622@gmail.com")
    # driver.find_element_by_id("su").click()
    # driver.quit()

