'''

Cryptography assignment: part C - watermarking an image using noise diffusion
'''
#from PIL import Image
import numpy
import operator
from scipy import ndimage
from matplotlib import pyplot as plt

def processImage(image, size):
    l = ndimage.imread(image)
    for i in range(size):
        for j in range(size):
            l[i][j] = [l[i][j][0],l[i][j][1], l[i][j][2]]
    return l

def showImage(pixels):
    plt.imshow(pixels, interpolation='none')
    plt.show()

def maximum(list1):
    highest = 0
    for i in range(len(list1)):
        for j in range(len(list1[i])):
            for k in range(3):
                num = list1[i][j][k]
                if(num > highest):
                    highest = num
    return highest
        
def WM(cipher, plaintext, covertext, size, R):
    cipher = numpy.fft.fft(cipher) # Compute spectrum of cipher
    plaintext = numpy.fft.fft(plaintext) # Compute spectrum of plaintext
    powerspectrum = numpy.power(numpy.absolute(cipher), 2) #Compute Power Spectrum


    #Pre-condition power spectrum of cipher

    for i in range(size):
        for j in range(size):
            for k in range(3):
                temp = powerspectrum[i][j][k]
                if(temp == 0):
                    powerspectrum[i][j] = 1

    #Diffuse plaintext image with pre-conditioned cipher
    diffusion = numpy.divide(numpy.multiply(cipher, plaintext), powerspectrum)
    diffusion = numpy.real(numpy.fft.ifft(diffusion)) #Compute real part of IFFT

    diffusion = numpy.divide(diffusion, maximum(diffusion)) #Normalise diffused field


    #Compute the watermark
    watermark = numpy.add(numpy.multiply(R, diffusion), covertext)
    watermark = numpy.divide(watermark, maximum(watermark)) #Normalise for output
    return watermark

def RECWM(cipher, watermark, covertext, size):
    diffusion = numpy.subtract(watermark, covertext)
    cipher = numpy.fft.fft(cipher)
    diffusion = numpy.fft.fft(numpy.absolute(diffusion))

    #Correlate diffused field with cipher
    plaintext = numpy.multiply(numpy.conj(cipher), diffusion)
    plaintext = numpy.real(numpy.fft.ifft(plaintext))       #Compute real part of IFFT

    plaintext = numpy.divide(plaintext, maximum(plaintext)) #Normalise output
    return plaintext


size = 500
cipher = processImage('1.bmp', size)
plaintext = processImage('2.bmp', size)
covertext = processImage('3.bmp', size)
# get watermark image
watermark = WM(cipher, plaintext, covertext, size, 50)
#displays watermark with noise/confusion
showImage(watermark)
#recovers plaintext
plaintext = RECWM(cipher, watermark, covertext, size)
#shows plain text
showImage(plaintext)





    

