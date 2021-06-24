import time
from instaclient import InstaClient
from instaclient.errors.common import *
from webdriver_manager.chrome import ChromeDriverManager


import cv2
import numpy as np
import matplotlib.pyplot as plt
def convertToRGB(image):
    
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

def facialPattern(Image_path):
    import numpy as np
    import matplotlib.pyplot as plt
    haar_cascade_face = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    comparison_img  = cv2.imread(Image_path)
    gray_compare = cv2.cvtColor(comparison_img, cv2.COLOR_BGR2GRAY)
    compare_rects = haar_cascade_face.detectMultiScale(gray_compare, scaleFactor = 1.12, minNeighbors = 3)

    for (x,y,w,h) in compare_rects:
     cv2.rectangle(comparison_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    plt.imshow(convertToRGB(comparison_img))
    plt.show()




    driver.close()

def match(img_path):
    img = cv2.imread(img_path)
    img2 = cv2.imread("Capture.JPG")
    corr = cv2.matchTemplate(img2, img, 
                        cv2.TM_SQDIFF_NORMED)[0][0]
    print(corr)
    return corr

def matchface(Image):
    img = cv2.imread(Image,0)
    template = cv2.imread('Capture.JPG',0)
    w, h = template.shape[::-1]
    
    methods = ['cv2.TM_CCOEFF_NORMED',]
    for meth in methods:
        img2 = img.copy()
        method = eval(meth)
        # Apply template Matching
        res = cv2.matchTemplate(img2,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img2,top_left, bottom_right, (0,255,0), 2)
        plt.subplot(121),plt.imshow(template,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img2,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        
        plt.suptitle(meth)
        plt.show()


def Image(arr):
    import urllib
    from urllib.request import urlretrieve
    from selenium import webdriver

    driver = webdriver.Chrome(ChromeDriverManager().install())    
    for i in arr.keys():
        # get the image source
        driver.get(arr[i])
        img = driver.find_element_by_xpath('/html/body/img')
        src = img.get_attribute('src')

        # download the image
        urlretrieve(src, "E:/Documents/Python/Instagram/images/captcha.png")
        if match("images\captcha.png") >= 0.4:
            matchface("images\captcha.png")
            print(f"Found:{i} --> {local[i]}")

local = {}

client = InstaClient(driver_path='C:/Users/abyss/.wdm/drivers/chromedriver/win32/88.0.4324.96/chromedriver.exe')

client.login(username='abyss033', password='#$Unknown$#')

username = "viciouztrickster"

followers = client.get_followers(user=username, count=65000000, callback_frequency=45)
count = 0
for follower in followers[0]:
    if follower["username"] not in local.keys():
        local[follower["username"]] = follower["profile_pic_url"]
    if follower["username"][-3:] == "801":
        print("Found")
        print(follower["profile_pic_url"])
        break

Image(local)
