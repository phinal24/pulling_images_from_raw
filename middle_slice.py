### Import all the things
import os, sys
import glob
import shutil
import MySQLdb
import numpy as np

### Target location of files on storage server
directory="/mnt/glusterfs"

### Define functions
def find_between(string,first,last):
	try:
		start=string.index(first)+len(first)
		end=string.index(last,start)
		return string[start:end]
	except ValueError:
		return ""

### Connect to database
conn = MySQLdb.connect(host='###.###.###.###', user='USER', passwd='PASS', db='DATA_BASE')
try:
	with conn:
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM xtek_scans")
		for row in cursor:
			id = int(row[0])
			sample = row[1]
			date = row[2].strftime("%Y-%m-%d")
			micro_ct = row[3]
			group_folder = row[4]
			remote_folder = row[5]
			voxel = row[6]
			bitrate = row[7]
			xdim = int(row[8])
			ydim = int(row[9])
			zdim = int(row[10])
			try:
				year=date.rsplit('-',2)[0]
        			recon_number=remote_folder.rsplit('_',1)[-1]
				new_directory="%s/%s" % (directory,year)
				new_sample_folder="%s/%s" % (new_directory,sample)
        			new_recon_raw="%s/RECON_%s/%s_%s_%s_%sx%sx%s.raw" % (new_sample_folder,recon_number,sample,voxel,bitrate,xdim,ydim,zdim)
				if os.path.exists(new_recon_raw):
					### ENTER IN THE CODE FOR EXTRACTING THE IMAGE ###
					volume=np.loadfile(new_recon_faw)		#check syntax
					array=np.reshape(volume,(zdim,ydim,xdim))	#check syntax
					z_center=int(zdim) // 2				#check syntax
					slice50=array[(zdim - 1):zdim]			#check syntax
					slice50=np.reshape(slice50,(ydim,xdim))		#check syntax
					saveimage(slice50,uint8,png_slice50)		#check syntax twice
					print("Successfully extracted slice@50 from %s/RECON_%s" % (sample,recon_number))
			except:
				print("Problem with %s" % (sample))
except:
	print("Problem with pulling from the database")
