import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

plot_grid_size = (4, 3)

def plot_img_histcdf(index1, index2,index3, img,img_rgb ,title):
    plt.subplot(plot_grid_size[0],plot_grid_size[1], index1)
    plt.imshow(img, cmap='gray')
    plt.axis('off'), plt.title(title+" gray") 

    plt.subplot(plot_grid_size[0],plot_grid_size[1],index3)
    plt.imshow(img_rgb)
    plt.axis('off'), plt.title(title+" rgb")
    

    plt.subplot(plot_grid_size[0],plot_grid_size[1], index2)
    hist,bins = np.histogram(img.flatten(), 256, [0,256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max()/ cdf.max()
    plt.plot(cdf_normalized, color = 'b')
    plt.hist(img.flatten(),256,[0,256], color = 'r')
    plt.xlim([0,256]), plt.title(title) 
    plt.legend(('cdf','histogram'), loc = 'upper left')
   
img= cv.imread("./airpot3.jpg")    
img_gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
img_rgb=cv.cvtColor(img,cv.COLOR_BGR2RGB)
img_hsv=cv.cvtColor(img_rgb,cv.COLOR_RGB2HSV)

#오리지날
plot_img_histcdf(1,2,3,img_gray,img_rgb,"original")

#HE
h,s,v= cv.split(img_hsv)
img_he= cv.equalizeHist(v)
hsv2 = cv.merge([h, s, img_he])
img_rgb_he=cv.cvtColor(hsv2,cv.COLOR_HSV2RGB)#컬러
img_gray_he= cv.equalizeHist(img_gray)#그레이
plot_img_histcdf(4,5,6,img_gray_he,img_rgb_he,"HE")

#AHE
h,s,v= cv.split(img_hsv)
ahe = cv.createCLAHE(clipLimit=100000, tileGridSize=(8,8))
v=ahe.apply(v)
hsv2 = cv.merge([h, s, v])
img_rgb_he=cv.cvtColor(hsv2,cv.COLOR_HSV2RGB)#컬러
img_gray_he= ahe.apply(img_gray)#그레이
plot_img_histcdf(7,8,9,img_gray_he,img_rgb_he,"AHE")


#CLAHE
h,s,v= cv.split(img_hsv)
clahe = cv.createCLAHE(clipLimit=2, tileGridSize=(8,8))
v=clahe.apply(v)
hsv2 = cv.merge([h, s, v])
img_rgb_he=cv.cvtColor(hsv2,cv.COLOR_HSV2RGB)#컬러
img_gray_he= clahe.apply(img_gray)#그레이
plot_img_histcdf(10,11,12,img_gray_he,img_rgb_he,"CLAHE")


plt.show()