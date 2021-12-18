import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

plot_grid_size = (4,6)

def plot_img(index, img, title):
    plt.subplot(plot_grid_size[0],plot_grid_size[1],index)
    plt.imshow(img[...,::-1])#rgb 순으로 출력
    plt.axis('off'), plt.title(title) 
    
def display_untilKey(Pimgs, Titles):
    for img, title in zip(Pimgs, Titles):
        cv.imshow(title, img)
    cv.waitKey(0)

def generate_gaussian_pyramid(img, levels):
    GP = [img]
    for i in range(1, levels): # 0 to levels - 1 same as range(0, levels, 1)
        img = cv.pyrDown(img)
        GP.append(img)
    return GP

def generate_laplacian_pyramid(GP):
    levels = len(GP)
    LP = [] #[GP[levels + 1]]
    for i in range(levels-1, 0, -1):
        upsample_img = cv.pyrUp(GP[i], None, GP[i-1].shape[:2])
        laplacian_img = cv.subtract(GP[i-1], upsample_img)
        LP.append(laplacian_img)
    LP.reverse()
    return LP

def generate_pyramid_composition_image(Pimgs):
    levels = len(Pimgs)
    rows, cols = Pimgs[0].shape[:2] 
    composite_image = np.zeros((rows, cols + int(cols / 2 + 0.5), 3), dtype=Pimgs[0].dtype)
    composite_image[:rows, :cols, :] = Pimgs[0]
    i_row = 0
    for p in Pimgs[1:]:
        n_rows, n_cols = p.shape[:2]
        composite_image[i_row:i_row + n_rows, cols:cols + n_cols,:] = p
        i_row += n_rows
    return composite_image

def stitch_LhalfAndRhalf(P_left, P_right):
    P_stitch = []
    for la,lb in zip(P_left, P_right):
        left=la.copy()
        right=lb.copy()
        l_x=left.shape[0];l_y=left.shape[1]
        r_x=right.shape[0];r_y=right.shape[1]
        left[(l_x-r_x)//2:((l_x-r_x)//2)+r_x , (l_y-r_y)//2:((l_y-r_y)//2)+r_y]=right
        P_stitch.append(left)
    return P_stitch

img_eye = cv.imread("./eye.jpg")
img_hand = cv.imread("./hand.jpg")

img_eye=cv.resize(img_eye, (101, 101))
img_hand=cv.resize(img_hand, (501, 501))

plot_img(1, img_eye, "eye")
plot_img(2, img_hand, "hand") 


GP_eye = generate_gaussian_pyramid(img_eye, 6)
GP_hand = generate_gaussian_pyramid(img_hand, 6)
LP_eye = generate_laplacian_pyramid(GP_eye)
LP_hand = generate_laplacian_pyramid(GP_hand)


display_untilKey([generate_pyramid_composition_image(GP_eye), 
                   generate_pyramid_composition_image(GP_hand),                    
                   generate_pyramid_composition_image(LP_eye),
                   generate_pyramid_composition_image(LP_hand)], 
                  ["GP_eye", "GP_hand", "LP_eye", "LP_hand"])


LP_stitch = stitch_LhalfAndRhalf(LP_hand,LP_eye)
GP_stitch = stitch_LhalfAndRhalf(GP_hand,GP_eye)

display_untilKey([generate_pyramid_composition_image(GP_stitch),
                   generate_pyramid_composition_image(LP_stitch)], 
                  ["composite GP imgs", "composite LP imgs"])

recon_img = GP_stitch[-1] 
lp_maxlev = len(LP_stitch) - 1
plot_img(6, recon_img.copy(), "level: " + str(5))

for i in range(lp_maxlev, -1, -1):
    recon_img = cv.pyrUp(recon_img, None,LP_stitch[i].shape[:2])
    plot_img(i + 1 + 12, recon_img.copy(), "level: " + str(i))
    recon_img = cv.add(recon_img, LP_stitch[i])
    plot_img(i + 1, recon_img.copy(), "level: " + str(i))
    plot_img(i + 1 + 6, LP_stitch[i].copy(), "level: " + str(i))
    
plot_img(1, recon_img, "result")
plt.show()