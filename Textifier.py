import numpy as np
import argparse
import imutils
import glob
import cv2

items = None

image = cv2.imread("test.png")
roi = image[220:850, 590:1300]
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

for imagePath in glob.glob("database/classes/*.png"):

	template = cv2.imread(imagePath)
	template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
	template = cv2.Canny(template, 50, 200)
	(tH, tW) = template.shape[:2]
	found = None
	classe = None

	for scale in np.linspace(1.0, 2.0, 20)[::-1]:

		resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
		r = gray.shape[1] / float(resized.shape[1])

		edged = cv2.Canny(resized, 50, 200)
		result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
		(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

		if found is None or maxVal > found[0]:
			found = (maxVal, maxLoc, r)
			if maxLoc[1] < 150 and maxLoc[0] < 100:		
				classe = imagePath			
				a,b = classe.split('\\')
				classeName, trash = b.split('_')
				
spells = set()			
for imagePath in glob.glob("database/spells/"+classeName+"/*.png"):

	template = cv2.imread(imagePath)
	template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
	template = cv2.Canny(template, 50, 200)
	(tH, tW) = template.shape[:2]
	found = None
	

	for scale in np.linspace(1.0, 2.0, 20)[::-1]:

		resized = imutils.resize(gray, width = int(gray.shape[1] * scale))
		r = gray.shape[1] / float(resized.shape[1])

		edged = cv2.Canny(resized, 50, 200)
		result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
		(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

		if found is None or maxVal > found[0]:
			found = (maxVal, maxLoc, r)
			if maxLoc[1] > 440 and maxLoc[1] < 490:
				if "passive" not in imagePath:
					x,y,spellsPath = imagePath.split('/')
					a,b = spellsPath.split('_')
					spell, trash = b.split('.')
					spells.add(spell)
				else:
					x,y,spellsPath = imagePath.split('/')
					a,b,c = spellsPath.split('_')
					spell, trash = c.split('.')
					spells.add(spell)
	
	print(imagePath)
	print(maxVal)
#faire pour les items

with open("Character.txt", 'w', encoding='latin1') as output:
	output.write("Class: " + classeName + "\n")
	output.write("Skills: \n")
	for x in spells:
		output.write(x + "\n")