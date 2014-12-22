import os
import sys
import web
import random
import wave
import numpy as np
import math
import json
import base64
import random

class WaveDecode():
    def __init__(self, filebuff):
        fp = open("tmp.wav", "wb")
        fp.write(filebuff)
        fp.close()
        wav = wave.open("tmp.wav", "rb")
        self._params = wav.getparams()
        nchannels, sampwidth, framerate, nframes = self._params[:4]
        self._str_data = wav.readframes(nframes)
        wave_data = np.fromstring(self._str_data, dtype=np.short)
        wave_data.shape = -1, nchannels
        self._wave_data = wave_data.T
        self._timeIdx = np.arange(0, nframes) * (1.0 / framerate)
        wav.close()
    def _toCoordinate(self, width, height, image_ratio):
        midX = width * 1.0 / 2
        midY = height * 1.0 / 2
        max_z = min(width - midX, height - midY)
        max_val = max(self._wave_data[0]) 
        arr = []
        prePoi = None
        time_len = min(len(self._timeIdx), len(self._wave_data[0]))
        for t in random.sample(xrange(time_len), image_ratio):
            z = (self._wave_data[0][t] / max_val) * max_z * 0.8
            x = math.sin(t) * z + midX
            y = math.cos(t) * z + midY
            arr.append((x, y))
        return json.dumps(arr)
urls = (
    '/uploader', 'Uploader',
    '/save', 'Saver',
    '/', 'Index'
)
app = web.application(urls, globals())
t_globals = {
    'datestr': web.datestr,    
}
render = web.template.render('pages', globals=t_globals)  
class Index:
    def GET(self):
        return render.index()
class Saver:
    def POST(self):
        i = web.input()
        image = i.get('image')#.split('data:image/bmp;base64,')[1]
        image = image.split('data:image/png;base64,')[1]
        image_name = i.get('filename').split('.')[0]
        fp = open('./data/save/%s.png' % (image_name), 'wb')
        fp.write(base64.decodestring(image))
        fp.close()
class Uploader:
    def POST(self):
        i = web.input()
        width = int(i.get('width'))
        height = int(i.get('height'))
        image_ratio = int(i.get("image_ratio"))
        filebuff = i.get('file')
        audio = WaveDecode(filebuff)
        arr = audio._toCoordinate(width, height, image_ratio)
        return arr
if __name__ == '__main__':
    app.run()
