import cv2
import sys
import numpy as np

images = []
images_gray = []


def split_images(image_paths):
    global images
    images = []
    for i in range(0, len(image_paths)):
        images.append(cv2.imread(image_paths[i]))
        b, g, r = cv2.split(images[i])
        filename = image_paths[i].split('.')[0]
        filename = filename.split('\\')[0].replace('sample','temp') + '\\' + filename.split('\\')[1] + '_b' + '.png'
        cv2.imwrite(filename + '_b' + '.png', b)
        cv2.imwrite(filename + '_g' + '.png', g)
        cv2.imwrite(filename + '_r' + '.png', r)


def detect_contours(image_paths):
    global images
    global images_gray
    images = []
    images_gray = []
    for i in range(0, len(image_paths)):
        # open in grayscale
        images_gray.append(cv2.imread(image_paths[i], cv2.IMREAD_GRAYSCALE))
        images.append(cv2.imread(image_paths[i]))
        # find threshold; to be optimised
        thresh = cv2.threshold(images_gray[i], 45, 255, cv2.THRESH_BINARY)[1]
        # find contours based on thresholded image
        contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
        # draw contours on image
        cv2.drawContours(images[i], contours, -1, (0, 255, 0), 3)
        # show image
        cv2.imshow(image_paths[i], images[i])


if __name__ == '__main__':
    image_paths = sys.argv[2:]
    if sys.argv[1] == 'split':
        split_images(image_paths)
    if sys.argv[1] == 'contours':
        detect_contours(image_paths)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
