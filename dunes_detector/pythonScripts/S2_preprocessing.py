#!/usr/bin/env python
#  -*- coding:utf-8 -*-

# START A GRASS SESSION WITH A LOCATION HAVING PROPER CRS (i.e. the same of the roi)
# FROM THE GRASS COMMAND PROMPT, TYPE > ipython and then copy and paste the script to run it

#import grass.script as grass
try:
    from grass.script import core as grass
except ImportError:
    import grass
except:
    raise Exception("Cannot find 'grass' Python module. Python is supported by GRASS from version >= 6.4")
import glob
import os
import sys
from datetime import datetime
import time
import fnmatch
import json
from grass.script import mapcalc
start = time.time()

#INPUT DATA
'''the commented lines are useful only to run directly the script from the GRASS terminal as:
> python ../S2_preproc.py "../rawdata/" "../roi.shp" 10
'''
from sys import argv

foldin_in = sys.argv[1]

if foldin_in[-1]!="/":
    foldin =  foldin_in+"/"
else:
    foldin = foldin_in

roi_in = sys.argv[2]
res_in = sys.argv[3]

#IMPORT JSON FILE FOR PARAMETERS CONFIGURATION
with open('/home/user/Desktop/UAE/config.json') as json_file:  
    parameters = json.load(json_file)

# UAE PATH
#foldin = r'C://Users//sara maffioli//Desktop//UAE//rawdataUAE//' #folder containing the sentinel imagery .SAFE 
#roi_in = r'C://Users//sara maffioli//Desktop//UAE//study_area//uae_utm39N.shp' # roi Shapefile

# # EGYPT PATH
# foldin = parameters['parameters'][0]['foldin'] #folder containing the sentinel imagery .SAFE 
# #foldin = r'/home/user/Desktop/UAE/rawdataEGYPT/' #folder containing the sentinel imagery .SAFE 
# roi_in = parameters['parameters'][0]['roi'] # roi Shapefile
# #roi_in = r'/home/user/Desktop/UAE/study_area/egypt_utm36N.shp' # roi Shapefile

# res_in = parameters['parameters'][0]['resolution'] # GRASS Region target resolution

# print (foldin)
# print (roi_in)
# print (res_in)

# BAND LIST
band_list=["B02","B03","B04","B05","B06","B07","B08","B8A","B11","B12"]

# CREATE OUTPUT FOLDER WITHIN THE INPUT FOLDER
folder_out = foldin + "outDOS"
if not os.path.exists(folder_out):        
    os.makedirs(folder_out)

#SET LOCATION 
#grass.create_location(dbase='foldin', location='Lnew', overwrite=True) #filename='roi_in'
#SET REGION ACCORDING TO SHAPE AND RES
grass.run_command("v.in.ogr",input=roi_in,output="roi",overwrite=True)
grass.run_command("g.region",vect="roi",res=res_in,flags="a")

# GET DATES
data = os.listdir(foldin)
dates=[]
for item in data:
    if item.endswith('.SAFE'): 
        date = (item.split("_")[-1]).split(".SAFE")[0]
        dates.append(datetime.strptime(date.partition('T')[0], '%Y%m%d').date())        
ldates = list(set(dates))
print (ldates)

# PROCESSING SCENES BY DATE
name_list=[]
band_name_list=[]
clusters=[]
images=[]
date_aq=[]
path_gr=[]
path_im=[]
for d in ldates:
  for x in data:
    if x.endswith('.SAFE') and x.find(d.strftime("%Y%m%d"))!=-1:
      name_list.append(x.split("_")[5]+"_"+x.split("_")[2])
      print(name_list)
      date_aq=(x.split(".")[0]).split("_")[-1]
      path_gr = "%s"%foldin+x+"/GRANULE/"
      for files in os.listdir(path_gr):
        if files.endswith(date_aq):
          path_im= "%s"%path_gr+files+"/IMG_DATA/"
          for bands_image in os.listdir(path_im):
            for bl in band_list:
              if bl == (bands_image.split(".")[0]).split("_")[-1] and bands_image.endswith('.jp2'):
                print(bands_image)        
                grass.run_command("r.in.gdal", input="%s"%path_im+'/'+bands_image, output=bands_image,flags='okr',overwrite=True)
                band = x.split("_")[5]+"_"+x.split("_")[2]+'_'+bl
                grass.run_command("g.rename", rast="%s,%s"%(bands_image,band+'_cf')) 

  #clouds
   #        cloud_im= "%s"%path_gr+files+"/QI_DATA"
   #        for im_c in os.listdir(cloud_im):
   #          if im_c.split("_")[1] == "CLOUDS" and im_c.endswith('.gfs'):
   #            grass.run_command("r.in.gdal", input="%s"%cloud_im+'/'+im_c, output=im_c,flags='okr',overwrite=True)        
   #         # IMPORT BANDS (flag -c to import vector cloud mask). 
   #    grass.run_command("i.sentinel.import", input="%s"%foldin+x,pattern='B(02|03|04|05|06|07|08|8A|11|12)', flags='c', overwrite=True)
      # # On Ubuntu add pattern='B(02|03|04|05|06|07|08|8A|11|12)' to read only bands of interest
        
    #   #CLOUD MASKING
   #          #cloud_mask_name_original = x.split('_')[4]+'_'+x.split('_')[1]+'_MSK_CLOUDS'
   #    cloud_mask_name_original = x.split('_')[5]+'_'+x.split('_')[2]+'_MSK_CLOUDS'
   #    cloud_mask_name = x.split("_")[5]+"_"+x.split("_")[2]+'_MSK_CLOUDS'
      # #check if the mask is imported and do the processing, othervise skip cloud masking by simply renaming bands
   #    cloud_check = grass.read_command("g.list",flags="f",type="vect")
      
   #    if cloud_mask_name_original in cloud_check:
   #      grass.run_command("g.rename", vector="%s,%s"%(cloud_mask_name_original,cloud_mask_name))
   #      grass.run_command("v.to.rast",input="%s"%cloud_mask_name,output="%s"%cloud_mask_name+'_rast',use='val',overwrite=True)
   #      grass.run_command("g.remove",type='vector',pattern="%s"%d.strftime("%Y%m%d"),flags='fr')
   #      for u in band_list:
   #        band = x.split("_")[5]+"_"+x.split("_")[2]+'_'+u
   #        mapcalc("$new = if (isnull($cloudmask)== 1, $original, null())",new="%s"%band+'_cf',cloudmask="%s"%cloud_mask_name+'_rast',original="%s"%band,overwrite=True)
   #    else:
      # for u in band_list:
      #   band = x.split("_")[5]+"_"+x.split("_")[2]+'_'+u
      #   grass.run_command("g.rename", rast="%s,%s"%(band,band+'_cf')) 
							
    # MERGE SAME BANDS OF MULTIPLE TILES AND CORRECT WITH DOS 
  for n in band_list:
    band_name_list = [s + "_"+n+'_cf' for s in name_list]
		
    if len(name_list) > 1:
            # PATCH BANDS
      grass.run_command("r.patch",input="%s"%",".join(band_name_list),output=d.strftime("%Y%m%d")+"_"+n+'_cf',overwrite=True)
    else:
            # SINGLE IMAGERY SCENE, RENAME ONLY WITHOUT PATCHING
      grass.run_command("g.rename", rast="%s,%s"%(band_name_list[0],d.strftime("%Y%m%d")+"_"+n+'_cf'))        
        # GET MINIMUM VALUE OF PATCHED BANDS
    vmin = float(grass.parse_command('r.univar', map='%s'%d.strftime("%Y%m%d")+"_"+n+'_cf', flags='g')['min'])
        # COMPUTE DOS
    mapcalc("$new = $original - $minimum",new=d.strftime("%Y%m%d")+"_dos_"+n,original=d.strftime("%Y%m%d")+"_"+n+'_cf',minimum=vmin,overwrite=True)

    # CREATE GROUP
  name = d.strftime("%Y%m%d")+"_dos"
  myInput=[name + "_"+n for n in band_list]
  grass.run_command("i.group",group='s2',subgroup='s2',input=",".join(myInput))

    # CLUSTER
  cluster_name = d.strftime("%Y%m%d")+"_cluster"
  num_cluster=parameters['parameters'][0]['clusters']
  grass.run_command("i.cluster", group='s2' ,subgroup='s2', signaturefile='cluster', classes=num_cluster, reportfile="%s"%foldin+"outDOS/"+cluster_name +"_class.txt", overwrite=True)   
  grass.run_command("i.maxlik", group='s2' ,subgroup='s2', signaturefile='cluster', output=cluster_name,overwrite=True)

  #clusters.append(cluster_name)
    # EXPORT CLUSTER MAP
  grass.run_command("r.out.gdal",input=cluster_name,output=foldin+"outDOS/"+cluster_name+'.tiff',overwrite=True)
    # RECLASSIFY
  grass.run_command("r.reclass",input=cluster_name ,output=cluster_name+"_rec", rules=foldin+'dune.txt' , title="Reclassification", overwrite=True)
  mapcalc("$reclass_map=$reclass_map",reclass_map=cluster_name+"_rec",overwrite=True)
  grass.run_command("r.out.gdal",input=cluster_name+"_rec",output=foldin+"outDOS/"+cluster_name+'_rec'+'.tiff',overwrite=True)
  clusters.append(cluster_name+'_rec')
     
    # REMOVE ALL DATA FROM THE GRASS MAPSET TO START PROCESSING ANOTHER SCENE
    #grass.run_command("g.remove",type='raster,vector',pattern="%s"%d.strftime("%Y%m%d"),flags='fr')
    #grass.run_command("g.remove",type='group',name='s2',flags='f')

  name_list=[]
  # band_name_list=[]

# DIFFERENCE MAP  
mapcalc("$difference=$first-$second", difference='difference',first=clusters[0],second=clusters[1],overwrite=True)
# EXPORT CLUSTER MAP
grass.run_command("r.out.gdal",input='difference',output=foldin+"outDOS/"+'difference'+'.tiff',flags='c',overwrite=True)
#end = time.time()
#print (end-start)
	
    # EXPORT TIFF WITH COMPRESSION 
    #grass.run_command("r.out.gdal",input='s2',output=foldin+"outDOS/"+name+'.tiff', createopt="COMPRESS=DEFLATE,NUM_THREADS=ALL_CPUS,PREDICTOR=3,BIGTIFF=YES",flags='tc',overwrite=True)


for d in ldates:
  grass.run_command("g.remove",type='raster,vector',pattern="%s"%d.strftime("%Y%m%d"),flags='fr')
  grass.run_command("g.remove",type='group',name='s2',flags='f')
  grass.run_command("g.remove",type='raster',name='difference',flags='f')
  grass.run_command("g.remove",type='raster',pattern="%s"%d.strftime("%Y%m%d")+'_cluster_rec',flags='fr')
  clusters=[]
  name_list=[]
  band_name_list=[]
  cluster_name=[]
  clouds_image=[]
  date_aq=[]
  path_gr=[]
  path_im=[]

end = time.time()
print (end-start) 


