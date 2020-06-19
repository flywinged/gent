# Copyright Clayton Brown 2019. See LICENSE file.

from typing import Tuple

from PIL import Image
import numpy

def loadPNG(filePath: str, outputSize: Tuple[int]) -> Tuple[numpy.ndarray, numpy.ndarray]:
    '''
    Output size is normalized into terminal space. Meaning an image that's 20x20 will
        actually appear to be 20x40. (because a terminal character is twice as tall as it is wide)
    '''

    imageData = numpy.swapaxes(numpy.array(Image.open(filePath).resize(outputSize, Image.BOX)), 0, 1)
    return imageData[:,:,:3], imageData[:,:,3]
