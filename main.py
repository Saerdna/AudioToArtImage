import os
import sys
import web
import wave
import numpy as np
import math
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
    def _toCoordinate(self, midX, midY, width, height):
        preDis = None
        max_z = min(width - midX, height - midY)
        max_val = max(self._wave_data[0]) 
        arr = []
        for t in xrange(len(self._timeIdx)):
            z = (self._wave_data[0][t] / max_val) * max_z
            x = math.sin(t) * z + midX
            y = math.cos(t) * z + midY
            arr.append((x, y))
        print arr
        
urls = (
    '/uploader', 'uploader',
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
class uploader():
    def POST(self):
        w = web.input()
        return True
if __name__ == '__main__':
    app.run()
    #audio = WaveDecode("./data/38.wav")
    #audio._toCoordinate(402, 264, 660, 510)
