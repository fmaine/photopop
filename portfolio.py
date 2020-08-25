"""Wikiguide : Class wrapper to wikipedia search API

Wikipedia search API encapsulation

  Typical usage example:

  wg = wikiguide.Wikiguide()
  pages = wg.textsearch('Paris')
"""
__author__ = "Francois Maine"
__copyright__ = "Copyright 2020, freedom Partners"
__email__ = "fm@freedom-partners.com"

import os
import json

class Portfolio():

    def __init__(self):
        self._images_dir = os.environ.get('PHOTOPOP_IMAGES_DIR','static/images')

    def get_photos(self,id):
        result = []
        dir = self._images_dir+'/'+id
        print('dir : ',dir)
        for filename in os.listdir(dir):
            longfilename = dir+'/'+filename
            if self.is_jpeg(longfilename):
                result.append(longfilename[7:])
        return result

    def get_collections(self):
        series = []
        root = self._images_dir
        for dir in os.listdir(root):
            path = root+'/'+dir
            if os.path.isdir(path):
                if os.path.isfile(path+'/serie.json'):
                    with open(path+'/serie.json') as json_file:
                        serie = json.load(json_file)
                        serie['photos']=[]
                        for file in os.listdir(path):
                            if self.is_jpeg(path+'/'+file):
                                photo = {
                                'id':file,
                                'url':(path+'/'+file)[7:],
                                'collection':path[14:],
                                }
                                serie['photos'].append(photo)
                        series.append(serie)
        return series

    def get_label(self,name):
        if name ==  'Divagations':
            return 'Divagations Pigalliennes et Lointaines'
        elif name == 'UnSoir':
            return 'Rencontres d\'un soir'
        else:
            return ''

    def is_jpeg(self,filename):
        return len(filename)>3 and filename[-4:]=='.jpg'
