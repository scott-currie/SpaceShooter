import os
import pygame

class ImageLoader(object):
	@staticmethod
	def load(img_folder, file_name, scale=1.0):
		'''Accepts a relative path and file name, then returns a converted image
			 suitable for use by Sprite instance.
			Arguments:
				img_folder 	: string 	: folder name of file location
				file_name 	: string 	: file name to load from disk
				dimensions 	: int tuple : width and height to scale image before converting
		'''		
		#Folder/file name are relative to program entry point
		image = pygame.image.load(os.path.join(img_folder, file_name))
		#Scale image 
		imgSize = image.get_size()
		hSize = int(imgSize[0] * scale)
		vSize = int(imgSize[1] * scale)
		image = pygame.transform.scale(image, (hSize, vSize))
		#Convert image
		image.convert()
		#Return image
		return image