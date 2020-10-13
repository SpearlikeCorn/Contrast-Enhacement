from skimage.morphology import closing
from skimage.morphology import opening
from skimage.morphology import selem
import numpy as np
from scipy.ndimage import gaussian_gradient_magnitude


def minmax(img):
    return (img - np.min(img))/(np.max(img)-np.min(img))


def CE(img, radius=None, stop_condition=40):
    '''
    Contrast Enhancement of Medical X-Ray ImageUsing Morphological Operators with OptimalStructuring Element,
    https://arxiv.org/pdf/1905.08545.pdf
    :param img: 2D np array, image
    :param radius: int [1-N], radius of the structuring element used for morphology operations
    :param stop_condition: int, value to which Edge content (EC) difference is compared, if EC difference is smaller
    then 'stop_condition' current value of radius consider to be optimal (recommended: 10-100 depending on the problem)
    :return: 2D np array, Contrast enhanced image normalized in between values [0-1]
    '''
    A = minmax(img)
    ECA = np.sum(gaussian_gradient_magnitude(A, 1))
    prevEC = 0
    # radius adapt to the image
    if radius is None:
        for r in range(1,30):
            # define SE as B
            B = selem.disk(r)
            # opening and closing operations defined in the paper
            Atop = A - opening(A, selem=B)
            Abot = closing(A, selem=B) - A
            Aenhanced = A + Atop - Abot
            Aenhanced = np.clip(Aenhanced, a_min=0, a_max=None)
            # Edge content calculations
            EC = np.sum(gaussian_gradient_magnitude(Aenhanced, 1))
            # min max scaling processed image
            Aenhanced_normed = (Aenhanced - np.min(Aenhanced))/(np.max(Aenhanced)-np.min(Aenhanced))
            # stopping condition
            if EC - prevEC < stop_condition:
                break
            prevEC = EC
    # pre-defined radius
    else:
        print("Radius =", radius)
        B = selem.disk(radius)
        Atop = A - opening(A, selem=B)
        Abot = closing(A, selem=B) - A
        Aenhanced = A + Atop - Abot
        Aenhanced = np.clip(Aenhanced, a_min=0, a_max=None)

        EC = np.sum(gaussian_gradient_magnitude(Aenhanced, 1))

        Aenhanced_normed = (Aenhanced - np.min(Aenhanced)) / (np.max(Aenhanced) - np.min(Aenhanced))
        print("EC =", EC)
    return Aenhanced_normed