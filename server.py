import os
import sys
import web
import wave
import numpy as np
import math
import json
import base64

class WaveDecode():
    def __init__(self, filename):
        wav = wave.open(filename, "rb")
        self._params = wav.getparams()
        nchannels, sampwidth, framerate, nframes = self._params[:4]
        self._str_data = wav.readframes(nframes)
        wave_data = np.fromstring(self._str_data, dtype=np.short)
        wave_data.shape = -1, nchannels
        self._wave_data = wave_data.T
        self._timeIdx = np.arange(0, nframes) * (1.0 / framerate)
        wav.close()
    def _toCoordinate(self, width, height):
        preDis = None
        midX = width * 1.0 / 2
        midY = height * 1.0 / 2
        max_z = min(width - midX, height - midY)
        max_val = max(self._wave_data[0]) 
        arr = []
        prePoi = None
        for t in xrange(len(self._timeIdx)):
            if t % 50 != 0:continue
            z = (self._wave_data[0][t] / max_val) * max_z
            x = math.sin(t) * z + midX
            y = math.cos(t) * z + midY
            if abs(x - midX) < 5 and abs(y - midY) < 5:continue
            if prePoi != (x, y):
                arr.append((x, y))
                prePoi = (x, y)

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
        image = i.get('image').split('data:image/png;base64,')[1]
        image_name = i.get('name')
        fp = open('%s.png' % (image_name), 'w+')
        fp.write(base64.decodestring(image))
        fp.close()
class Uploader:
    def POST(self):
        audio = WaveDecode("./data/38.wav")
        i = web.input()
        width = int(i.get('width'))
        height = int(i.get('height'))
        arr = audio._toCoordinate(width, height)
        return arr
if __name__ == '__main__':
    app.run()
