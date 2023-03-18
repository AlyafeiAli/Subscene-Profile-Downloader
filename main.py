from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
import undetected_chromedriver as uc
import os

current_dir = os.getcwd()
download_dir = os.path.join(current_dir, "subscene")
options = uc.ChromeOptions()
options.add_argument("--disable-popup-blocking")
exec_ = os.path.join("C:", "chromedriver")

def download_profile(profileID):
    driver = uc.Chrome(executable_path=exec_, use_subprocess=True, options=options)
    driver.set_window_size(960, 720)
    params = {
        "behavior": "allow",
        "downloadPath": download_dir
    }
    driver.execute_cdp_cmd("Page.setDownloadBehavior", params)
    links = []

    counter = 0
    while True:
        counter += 1
        url = f"https://subscene.com/u/{profileID}/subtitles?Id={profileID}&page={counter}&orderBy=latest"
        driver.get(url)
        for row in driver.find_elements(By.XPATH,
                                        "/ html / body / div[1] / div[3] / div / table / tbody / tr / td[1] / a"):  # xp
            o = row.get_attribute("href")
            links.append(o)
            with open("links.txt", "a+") as myfile:
                myfile.write(f"{o}\n")
            print(o)
        print(f"page {counter}")
        check = driver.find_element(By.CLASS_NAME, 'PagedList-skipToNext').text
        if not check:
            print("Reached end!")
            break
        sleep(0.5)


    # driver.close()
    for link in links:
        driver.execute_script(f"window.open('{link}', 'new window');")
        driver.switch_to.window(driver.window_handles[1])
        name = driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/div[2]/div[2]/ul/li[1]/div[1]").text
        button = driver.find_element(By.ID, "downloadButton")
        button.click()
        print(f"downlaoded {name}")
        sleep(0.5)
    sleep(1)
    driver.close()
    return links
    # sleep(3)

profile_link = input("Enter subscene profile id: ")
links = download_profile(profile_link)

print(f"num of links downlaoded: {len(links)}")