import os
import sys
import web
import wave
import numpy as np
import pylab as pl

class WaveDecode():
    def __init__(self, filename):
        wav = wave.open(filename, "rb")
        self._params = wav.getparams()
        nchannels, sampwidth, framerate, nframes = self._params[:4]
        print nchannels, sampwidth, framerate, nframes
        self._str_data = wav.readframes(nframes)
        wave_data = np.fromstring(self._str_data, dtype=np.short)
        wave_data.shape = -1, nchannels
        self._wave_data = wave_data.T
        self._timeIdx = np.arange(0, nframes) * (1.0 / framerate)
        wav.close()
    def draw(self):
        pl.subplot(211) 
        timeX = []
        waveY = []
        for i in xrange(len(self._wave_data[0])):
            if i % 100 == 0:
                timeX.append(self._timeIdx[i])
                waveY.append(self._wave_data[0][i])
        pl.plot(timeX, waveY)
        pl.show()

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
