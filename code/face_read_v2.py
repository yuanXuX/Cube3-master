import cv2
import math
# import numpy as np

color = {'W': 0, 'R': 1, 'G': 2, 'B': 3, 'O': 4, 'Y': 5, 'U': 6}


def get_mean_RGB(img):
    # note: the default color format in CV2.imread is BGR
    blue = img[:, :, 0].mean()
    green = img[:, :, 1].mean()
    red = img[:, :, 2].mean()
    return red, green, blue


def get_mean_HSV(img):
    HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h = HSV[:, :, 0].mean()
    s = HSV[:, :, 1].mean()
    v = HSV[:, :, 2].mean()
    return h, s, v


def get_color_HSVRGB(h, s, v, r, g, b):
    if (r==0 or b / r > 2) and b > g:
        return color['B']
    elif (r==0 or g / r > 2) and g > b:
        return color['G']
    if (b==0 or r / b > 2) and (g==0 or r / g > 2):
        if h > 8:
            return color['O']
        else:
            return color['R']
    elif h < 20 and s < 150:
        return color['W']
    elif h < 50:
        return color['Y']
    else:
        return color['W']


def sq_color_read(img, edge_pect):
    '''
        input:
            image of a single sticker(of a single color)
        return:
            one integer representing the sticker's color
            W:0 R:1 G:2 B:3 O:4 Y:5
    '''
    ori_size = len(img)
    start = math.floor(ori_size*(edge_pect/2))
    end = math.floor(ori_size*(1-edge_pect/2))
    img_center = img[start:end, start:end]
    r, g, b = get_mean_RGB(img_center)
    h, s, v = get_mean_HSV(img_center)
    return get_color_HSVRGB(h, s, v, r, g, b)


def face_read(img):
    '''
        input:  
            image read by cv2.imread(pth)
            (the given img must be a square)
        return:
            a list of 9 integers�?
                W:0 R:1 G:2 B:3 O:4 Y:5
            representing colors of the 9 stickers on the cube face
    '''
    colors = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    size_len = len(img)
    s_size = int(size_len / 3)
    for i in range(9):
        l = i // 3 + 1
        c = i % 3 + 1
        sticker = img[(l-1)*s_size:l*s_size, (c-1)*s_size:c*s_size]
        colors[i] = sq_color_read(sticker, 0.7)
    name2color = {v: k for k, v in color.items()}
    return colors


if (__name__ == '__main__'):
    img = cv2.imread("capture_python.png")
    face_read(img)

# W:0 R:1 G:2 B:3 O:4 Y:5
