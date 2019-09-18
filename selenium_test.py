from selenium import webdriver
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800,600))
display.start()
driver = webdriver.Firefox()
driver.get('https://www.baidu.com')
print(driver.title)
driver.quit()
display.stop()