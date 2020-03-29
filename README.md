# DunesDetector
DunesDetector is a QGIS plugin that creates temporal stacks of Sentinel 2 satellites images and performs classification on them in order to detect desert dunes over a user-defined region.
It is currently developed for Linux.

## Getting Started

### Prerequisites

For running the *DunesDetector* is needed to have installed the OSGeoLive Virtual Machine.

For Sentinel-2 image data retrieval there are two main ways:
* from the Copernicus Open Access Hub
* API Hubsentinelsat

The first method allows the user to use the online interactive interface and browse the area of interest directly by the Copernicus Open Access Hub site while the second one allows to use a Python sentinelsat library to access the API of Copernicus Sentinels Scientific Data Hub. It needs to install the following dependency:
```
pip install sentinelsat
```
Example of shell instruction:
```
(user) C:\Users\Desktop\Folder_in>sentinelsat -u username -p password -g file.geojson --sentinel 2 -s YYYYMMDD -e YYYYMMDD -d
```
Also a JQ dependency is needed: 
```
sudo apt-get install jq
```
### Installing

Launch OSGeoLive Virtual Machine

Select a folder and download the code, then compress 'dunes_detector' folder as .ZIP

```
git clone https://github.com/Sara495/DunesDetector
```
From QGIS Desktop install plugin, choosing the option install from ZIP, and select the ZIP file created


### Running

Launch the DunesDetector from the plugin window in QGIS

Then fill the fields as following: 

1. **Input folder:**
connect to the folder where the user has the unzipped folders of Sentinel 2 images. The folders must be the original ones without name modification

2. **Study area:**
connect to the folder where there’s the Shapefile of the area of interest and select the Shapefile
3. **Resolution:**
spatial resolution at which the user wants to reproject the bands
4. **Number of clusters for K-Mean classifier:**
the number of clusters that the user wants to use to classify images, used as parameter in
the i.cluster algorithm. It is defined by the user by iteratively looking at resulting DATE_cluster_class.txt , created after the first unsupervised classification process and located in the output folder, until the maximum percentage of stable points and maximum convergence value is reached. Another way could be to have experience and a priori knowledge on the study area.
5. **START button:**
clicking on START button the dunes_detector.py script will be launched and the images preprocessing will start.
6. **Waiting Warning Message:**
When the process ends the folder with the output results will be open and the user can directly import the desidered images in QGIS

## Warning
In case of denied access error copy in the terminal the following code to allow the user to have the privileges to read files

```
chmod u=rx /home/user/.local/share/QGIS/QGIS3/profiles/default/python/plugins/dunes_detector/pythonScripts/launch.sh
```

## Authors
| Name and Surname  | Email                                  |
|-------------------|----------------------------------------|
| Sara Maffioli   | saramaffioli@outlook.it |
| Federica Vaghi | federica.vaghi@mail.polimi.it | 

