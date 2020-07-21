# Copyright Clayton Brown 2019. See LICENSE file.

from typing import Tuple

from PIL import Image
import numpy

from dataclasses import dataclass

@dataclass
class ImageData:
    '''
    Image return data from loadPNG or convert.
    '''

    backgroundColorData: numpy.ndarray
    textColorData: numpy.ndarray
    transparencyData: numpy.ndarray
    characterData: numpy.ndarray

def loadPNG(filePath: str, outputSize: Tuple[int], useHalfBlocks: bool = True) -> ImageData:
    '''
    Output size is normalized into terminal space. Meaning an image that's 20x20 will
        actually appear to be 20x40. (because a terminal character is twice as tall as it is wide)

    Returns are:
        Background colors
        Text colors
        Transparency
    '''

    if not useHalfBlocks:
        imageData = numpy.swapaxes(numpy.array(Image.open(filePath).resize(outputSize, Image.BOX)), 0, 1)
        return ImageData(
            imageData[:,:,:3],
            numpy.zeros((imageData.shape[0], imageData.shape[1], 3)),
            imageData[:,:,3],
            numpy.ones(outputSize, dtype=numpy.int16) * ord(" ")
        )

    imageData = numpy.swapaxes(numpy.array(Image.open(filePath).resize((outputSize[0], outputSize[1] * 2), Image.BOX)), 0, 1)
    backgroundColors = imageData[:,1::2,:3]
    textColors = imageData[:,::2,:3]

    return ImageData(
            backgroundColors,
            textColors,
            imageData[:,1::2,3],
            numpy.ones(outputSize, dtype=numpy.int16) * 9600
        )

def convertImage():
    '''

    '''