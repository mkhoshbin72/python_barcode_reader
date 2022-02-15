import cv2
import matplotlib.pyplot as plt
from pyzbar import pyzbar
import argparse
import os


def preprocess(img_path, gray=False):

    img = cv2.imread(img_path)
    if gray == False:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    elif gray == True:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return img


def show(img):

    plt.figure(figsize=(10,10))

    l = len(img.shape)

    if l == 2:
        plt.imshow(img, cmap='gray')

    else:
        plt.imshow(img)

    plt.axis('off')
    plt.show()


def draw_barcode(img, decoded_objects):

    decoded_objects = decoded_objects[0]
    image = cv2.rectangle(img, (decoded_objects.rect.left, decoded_objects.rect.top), 
                            (decoded_objects.rect.left + decoded_objects.rect.width, decoded_objects.rect.top + decoded_objects.rect.height),
                            color=(0, 255, 0),
                            thickness=5)

    cv2.putText(image,
                decoded_objects.data.decode('utf-8'),
                (decoded_objects.rect.left+5, decoded_objects.rect.top-10),
                cv2.FONT_HERSHEY_COMPLEX,
                0.7,
                (0,0,255),
                2)

    return image


def barcode_reader(img_path):

    gray_img = preprocess(img_path, gray=True)
    decoded_objects = pyzbar.decode(gray_img)

    return decoded_objects



if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required = True,
        help = "path to the image file")
    ap.add_argument("-v", "--view", required = False, default=False, action='store_true',
        help = "view image with barcode")
    ap.add_argument("-s", "--save", required = False, default=False, action='store_true',
        help = "save result imag")
    args = vars(ap.parse_args())

    image_path = args['image']
    view = args['view']
    save = args['save']

    decoded_objects = barcode_reader(image_path)
    barcode = decoded_objects[0].data.decode('utf-8')
    print('Barcode: ', barcode)
    
    if view == True or save == True:
        image = preprocess(image_path)
        image = draw_barcode(image, decoded_objects)
        
        if view == True:
            show(image)
        if save == True:
            cv2.imwrite(f'resutls/res_{os.path.basename(image_path)}', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
