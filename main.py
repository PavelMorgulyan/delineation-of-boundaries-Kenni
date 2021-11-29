# -*- coding: utf-8 -*-

#Загрузка библиотек и функций
import glob
from skimage import io
from skimage.color import rgb2gray
from skimage.viewer import ImageViewer
from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter
from skimage import data, color, img_as_ubyte
from skimage import feature

#Функция для вывода изображения
def showImg(img) :
    imgViewer = ImageViewer(img)
    imgViewer.show()
    
#Функция подсчета коэффициента для решения
def computeRatio(img):
    #Применение алгоритма выделения границ
    edges = feature.canny(img, sigma=6)
    #Нахождение приближенного эллипса
    resultEllipseForms = hough_ellipse(edges, accuracy = 18, threshold=4,
                       min_size=10)
    resultEllipseForms.sort(order='accumulator')
    bestForm = list(resultEllipseForms[-1])
    #Получение параметров приближенного эллипса
    yc, xc, a, b = [int(round(x)) for x in bestForm[1:5]]
    orientation = bestForm[5]
    #print (a, b)
    #Определение минимального коэффициента соотношения осей эллипса
    if b != 0 and a !=0:
        k1 = (2*float(a)) / (2*float(b))
        k2 = (2*float(b)) / (2*float(a))
    else:
        resK = 0
        return resK
    resK = 0
    if (k1 > k2):
        resK = k2
    else:
        resK = k1
    #print (resK)
    cy, cx = ellipse_perimeter(yc, xc, a, b, orientation)
    edges = color.gray2rgb(img_as_ubyte(edges))
    edges[cy, cx] = (250, 0, 0)
    io.imshow(edges)
    return resK

#Путь к выборкам изображений
# basePath = 'dataset/dataset_fruits/Training'
basePath = 'dataset/dataset_fruits/Testing'

#Классы изображений
classes = [
    'Apple_Red_Delicious',
    'Quince',
]

#Объект классов изображения
imgData = {}

#Загрузка изображений в программу
#Применения изменения оттенков на серый
for imgClass in classes:
    imgData[imgClass] = []
    for file in glob.glob('{}/{}/*'.format(basePath, imgClass)):
        imgData[imgClass].append(rgb2gray(io.imread(file)))

#Массив критериев выборки изображений
ratioCoefArray = []

#Перебор изображений из выборки и занесение коээфициентов в массив критерие
for img in imgData['Quince']:
    ratioCoefArray.append(computeRatio(img))
  
#Пороговый коэффициент для решения
recCoefRatio = 0.86

#Счетчики верного и неверного решения
countCoefRec = 0
countCoefRecMax = 0

print (max(ratioCoefArray))
#Подсчет порогового коэффициента для обучающей выборки
#Подсчет верного и неверного вхождения для тестовой выборки
coefSum = 0
for coef in ratioCoefArray:
    coefSum = coefSum + coef
    if coef > recCoefRatio:
        countCoefRec = countCoefRec + 1
    if coef < recCoefRatio:
        countCoefRecMax = countCoefRecMax + 1
    
#Расчет порогового коээфициента
avgCoef = coefSum/len(ratioCoefArray)

print(avgCoef)
#Расчет процентного соотношения верно идентифицированных изображений
print(countCoefRecMax/len(ratioCoefArray))