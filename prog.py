import pyfits as pf
import numpy as np
import matplotlib.pyplot as plt
import os , sys
import natsort
from natsort import natsort

class Image_characterstics:	
	
	def __init__(self,filename):
		self.filename = filename

	def start_time_image(self):              #extracts starting time of image
		hdu = pf.open(self.filename)
		return hdu[0].header['AINTBEG']

	def end_time_image(self):			#extracts end time of image
		hdu = pf.open(self.filename)
		return hdu[0].header['ATIMEEND']

	def extract_intensity(self):         #extracts intensity of brightest pixel
		hdu = pf.open(self.filename)
		image = hdu[0].data
		intensity = np.nanmax(image)
		return intensity
	
	def extract_flux_Conv_factor(self):  # since value of flux = (intensity*GAIN)/EXPTIME
		hdu = pf.open(self.filename)
		factor = hdu[0].header['GAIN']/hdu[0].header['EXPTIME']
		return factor
		

class Graph:

	def __init__(self,xlabel,ylabel,title,xvalues,yvalues,color):
		self.xlabel = xlabel
		self.ylabel = ylabel 
		self.title  = title
		self.xvalues = xvalues
		self.yvalues = yvalues
		self.color = color
	
	def plot_graph(self):
		plt.plot(self.xvalues,self.yvalues,self.color)
		plt.ylabel(self.ylabel)
		plt.xlabel(self.xlabel)
		plt.title(self.title)
		plt.show()
	

def extract_filenames(path):
        dirs = os.listdir(path)
        direc = natsort(dirs)
        return direc
		

def main():

	time = []
	flux_values = []
	time_in_seconds = 0 # count variable of time
	dirs = extract_filenames("bcd") # path of directory
	for filename in dirs:
		filename = 'bcd/' + filename
		image = Image_characterstics(filename)
		start_time = image.start_time_image()
		end_time  = image.end_time_image()
		intensity = image.extract_intensity()
		factor = image.extract_flux_Conv_factor()
		flux = factor*intensity
		flux_values.append(flux)
		time.append(time_in_seconds)
		time_in_seconds = time_in_seconds + (end_time - start_time)
		
	graph1 = Graph('Time (seconds)','Flux (Jy)','Lightcurve',time,flux_values,'r')
	graph1.plot_graph()
	

main()
