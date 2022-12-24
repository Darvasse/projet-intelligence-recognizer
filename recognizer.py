import cv2
import sys
import os
import random

cascPath = sys.argv[1]
filePath = sys.argv[2]
population = 3
populationInformation = []
parametre = []

def randomizePopulation(population):
    for i in range(0, population):
        populationInformation.append([random.uniform(1.01, 1.1), random.randint(3, 6), random.randint(30, 50)])

def getFaces(filePath, populationParametre:list):
    moyenne = 0
    for i in range(0, 2):
        totalFaces = 0
        #print(filePath+str(i)+'\\')
        print(populationParametre)
        print(populationParametre[0])
        Fails = 0
        for pic in os.listdir(filePath+str(i)+'\\'):
            
            faceCascade = cv2.CascadeClassifier(cascPath)

            image = cv2.imread(filePath+str(i)+'\\'+pic)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=populationParametre[0],
                minNeighbors=populationParametre[1],
                minSize=(populationParametre[2], populationParametre[2]),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            totalFaces += len(faces)
            #print("Found {0} faces!".format(len(faces)))
            
            if len(faces)!=i:
                Fails += 1

            """for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)"""

            #cv2.imshow("Faces found", image)
        print("Total faces found: ", totalFaces)
        print("Total fails: ", Fails)
        print("Success rate: ", (totalFaces-Fails)/totalFaces)
        moyenne += (totalFaces-Fails)/totalFaces
    print("Moyenne: ", moyenne/2)
    return moyenne/2
#getFaces(filePath, [1.0599287243182003, 3, 30])
def testPopulation(population):
    for i in range(0, population):
        parametre.append(getFaces(filePath, populationInformation[i]))
        print("Parametre: ", populationInformation[i])

def fitness(parametre):
    best = 0
    for i in range(0, len(parametre)):
        if parametre[i] > parametre[best]:
            best = i
    return best

def diversification(populationParametre):
    for i in range(1, population):
        populationParametre[i][0] += random.uniform(-0.01, 0.01)
        populationParametre[i][1] += random.randint(-1, 1)
        populationParametre[i][2] += random.randint(-5, 5)
    return populationParametre
if input("Is training? (y/n) ") == "y":
    randomizePopulation(population)
    print("=======================================================Population: ", populationInformation)
    bestCount = 0
    while True:
        lastBest = fitness(parametre)
        testPopulation(population)
        print("Best parametre: "+str(fitness(parametre))+" ", populationInformation[fitness(parametre)])
        diversification(populationInformation)
        print("=======================================================Nouvelle population: ", populationInformation)
        newBest = fitness(parametre)
        if lastBest == newBest:
            bestCount += 1
            if bestCount == 3:
                print("Final parametre: "+str(fitness(parametre))+" ", populationInformation[fitness(parametre)])
                break
        else:
            bestCount = 0
else:
    if input("Voulez-vous tester votre IA ? (y/n) ") == "y":
        scale = float(input("Entrez le scaleFactor: "))
        minNeighbors = int(input("Entrez le minNeighbors: "))
        minSize = int(input("Entrez le minSize: "))
        populationInformation.append([scale, minNeighbors, minSize])
        print("Parametre: ", populationInformation[0])
        print("Fitness: ", getFaces('.\\archive\\test_machine\\', populationInformation[0]))
    else:
        print("Entrez le chemin relatif de votre image à tester: ")
        imagePath = input()
        scale = float(input("Entrez le scaleFactor: "))
        minNeighbors = int(input("Entrez le minNeighbors: "))
        minSize = int(input("Entrez le minSize: "))
        populationInformation.append([scale, minNeighbors, minSize])
        print("Parametre: ", populationInformation[0])
        faceCascade = cv2.CascadeClassifier(cascPath)  
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=populationInformation[0][0],
            minNeighbors=populationInformation[0][1],
            minSize=(populationInformation[0][2], populationInformation[0][2]),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        print("Found {0} faces!".format(len(faces)))
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow("Faces found", image)
        cv2.waitKey(0)

        


"""
def selection(populationParametre, parametre):
    newPopulationParametre = []
    for i in range(0, population):
        newPopulationParametre.append(populationParametre[fitness(parametre)])
    return newPopulationParametre

def diversification(populationParametre):
    for i in range(0, population):
        populationParametre[i][0] += random.uniform(-0.01, 0.01)
        populationParametre[i][1] += random.randint(-1, 1)
        populationParametre[i][2] += random.randint(-5, 5)
    return populationParametre

def evolution(populationParametre, parametre):
    populationParametre = selection(populationParametre, parametre)
    populationParametre = diversification(populationParametre)
    return populationParametre

def main(populationParametre):
    for i in range(0, 100):
        print("Generation: ", i)
        parametre = []
        for i in range(0, population):
            parametre.append(getFaces(filePath, populationParametre[i]))
        populationParametre = evolution(populationParametre, parametre)
        print("Best parametre: ", populationParametre[fitness(parametre)])
        print("Best fitness: ", parametre[fitness(parametre)])

main(populationInformation)"""
