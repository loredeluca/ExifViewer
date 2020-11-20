# Image-Exif Viewer
This software uses PyQt5 to implement a JPEG Image and EXIF viewer. It has the following features:
- **View multiple images**: allow the user to add/remove more than one image from a file selector with controls for switching to next/previous image in the list.
- **Visualization of images**: your JPEG images can be scaled to have a maximum dimension (height or width) of 512 pixels.
- **Visualization of image EXIF data**: the table next to the image list all EXIF tags encoded in the JPEG file and provides a scrolling widget to view them all.
- **Rescaling**: the main window of your GUI support rescaling. That is, when the user resizes the application, the user interface and the image scale appropriately.
- **Image rotation**: the GUI has a button interface to access image rotation, with 90° increments.
- **Geolocalization**: if an image has GPS Geolocation Tags in its EXIF tag set, a button allows users to click on the location and open a browser with Google Maps centered on the GPS location of the image.

![output](https://github.com/loredeluca/ExifViewer/blob/main/file/gui.gif)

### How to install
To build the files, you will need the [PyQt5](https://pypi.org/project/PyQt5/) and [Pillow](https://pillow.readthedocs.io/en/stable/index.html) libraries, then the program can be launched:
```sh
$ python3 exifViewer.py
```
### How to make it work
The user can interact with the GUI using the following commands:

| Command | Description |
| :---: | --- |
| <img src="https://github.com/loredeluca/ExifViewer/blob/main/icon/addimage.png" width=" 25" height="25"> | Add an image (or more than one), filling the list at the top |
| <img src="https://github.com/loredeluca/ExifViewer/blob/main/icon/remove.png" width=" 25" height="25"> | Remove the image from the list |
| <img src="https://github.com/loredeluca/ExifViewer/blob/main/icon/doubleclick.png" width=" 25" height="25"> | View the image and the exif data |
| <img src="https://github.com/loredeluca/ExifViewer/blob/main/icon/map.png" width=" 18" height="25"> | View the geolocalization |
| <img src="https://github.com/loredeluca/ExifViewer/blob/main/icon/leftrotate.png" width=" 25" height="25"> or <img src="https://github.com/loredeluca/ExifViewer/blob/main/icon/rightrotate.png" width=" 25" height="25">  | Rotate the image 90° to the left and to the right |
| <img src="https://github.com/loredeluca/ExifViewer/blob/main/icon/left.png" width=" 25" height="25"> or <img src="https://github.com/loredeluca/ExifViewer/blob/main/icon/right.png" width=" 25" height="25">  | Switch between images |
