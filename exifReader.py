from PyQt5 import QtCore

import PIL.Image
import PIL.ExifTags


class Exif(QtCore.QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super(Exif, self).__init__(*args, **kwargs)
        self.exifData = None

    def update(self, data):
        self.exifData = data

    def rowCount(self, parent=QtCore.QModelIndex()):
        if self.exifData is not None:
            return len(list(self.exifData.values()))
        else:
            return 0

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 2

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            i = index.row()
            j = index.column()
            if j == 0:
                return list(self.exifData)[i]
            else:
                return str(self.exifData[(list(self.exifData)[i])])
        else:
            return QtCore.QVariant()

    def headerData(self, column_number, orientation=QtCore.Qt.Horizontal, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if column_number == 0:
                return 'Exif Info'
            else:
                return 'Data'

    def get_position(self):
        try:
            return str(convert_to_degree(self.exifData['GPSInfo'][2])) + ',' + \
                   str(convert_to_degree(self.exifData['GPSInfo'][4]))
        except KeyError:
            return None


def convert_to_degree(value):
    d = value[0][0] / value[0][1]
    m = value[1][0] / value[1][1]
    s = value[2][0] / value[2][1]

    return d + (m / 60.0) + (s / 3600.0)


def getExif(imagePath):
    try:
        img = PIL.Image.open(imagePath)
        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
        }
        return exif
    except AttributeError:
        error_msg = 'NotFound'
        return error_msg
