import os
import sys
import web
import random
import wave
import numpy as np
import math
import json
import base64
import thread

mylock = thread.allocate_lock()  
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
    def dist(self, s, t):
        return math.sqrt((s[0] - t[0])**2 + (s[1] - t[1])**2)
    def toCoordinate(self, width, height, image_ratio):
        preDis = None
        midX = width * 1.0 / 2
        midY = height * 1.0 / 2
        max_z = min(width - midX, height - midY)
        arr = []
        prePoi = None
        time_len = min(len(self._timeIdx), len(self._wave_data[0]))
        wave_arr = random.sample(self._wave_data[0], image_ratio)
        max_val = max(wave_arr) 
        arr.append((midX, midY))
        preZ = 0
        for one in wave_arr:
            det = math.fabs((one * 1.0 / max_val) * max_z * 0.9)
            arr.append((midX + det - preZ, midY + det))
            preZ = det
        arr.append((midX, midY))
        '''
        for t in random.sample(xrange(time_len), image_ratio):
            z = (self._wave_data[0][t] / max_val) * max_z * 0.9
            x = math.sin(t) * z + midX
            y = math.cos(t) * z + midY
            arr.append((x, y))
        '''
        return json.dumps(arr)
urls = (
    '/uploader', 'Uploader',
    '/flush', 'Flush',
    '/save', 'Saver',
    '/path', 'Path',
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
global output_path
output_path = None
global input_path
input_path = None
class Path:
    def GET(self):
        global output_path
        global input_path
        i = web.input()
        op = i.get('op')
        path_type = i.get('path_type')
        if op == 'get':
            if path_type == "output":
                if output_path == None:
                    output_path = os.getcwd() + '/data/save/'
                return output_path
            elif path_type == "input":
                if input_path == None:
                    input_path = os.getcwd() + '/data/input/'
                return input_path
        elif op == 'set':
            path = i.get('path')
            if path_type == "output":
                output_path = path
            elif path_type == "input":
                input_path = path
            try:
                os.makedirs(path)
            except OSError as exc: # Python >2.5 (except OSError, exc: for Python <2.5)
                if os.path.isdir(path):
                    pass
                else:
                    return False
            return True
global g_filename
class Saver:
    def POST(self):
        global output_path
        i = web.input()
        image = i.get('image')
        image = image.split('data:image/png;base64,')[1]
        #image_name = i.get('filename').split('.')[0]
        global g_filename
        image_name = g_filename.split('.')[0]
        fp = open('%(output_path)s/%(image_name)s.png' % ({"output_path":output_path, "image_name": image_name}), 'wb')
        fp.write(base64.decodestring(image))
        fp.close()
        mylock.release()
global prelist
prelist = {}
class Flush:
    def GET(self):
        global input_path
        global prelist
        global g_filename
        req = web.input()
        width = int(req.get('width'))
        height = int(req.get('height'))
        image_ratio = int(req.get('image_ratio'))
        nowlist = {}
        arr = None
        filename = None
        if mylock.locked() == True:
            return json.dumps(None)
        mylock.acquire()
        for one in os.listdir(input_path):
            tmp = one.split('.')
            if tmp[-1].lower() != 'wav':continue
            nowlist[one] = True
            if prelist.has_key(one) == False:
                filename = one
                break
        g_filename = filename
        if filename == None:
            mylock.release()
            return json.dumps(None)
        for one in prelist.keys():
            if nowlist.has_key(one) == False:
                prelist.pop(one)
        prelist[filename] = True
        audio = WaveDecode(input_path + "/" + filename)
        arr = audio.toCoordinate(width, height, image_ratio)
        return arr
class Uploader:
    def POST(self):
        mylock.acquire()
        req = web.input()
        width = int(req.get('width'))
        height = int(req.get('height'))
        filename = req.get('name')
        image_ratio = int(req.get('image_ratio'))
        filebuff = req.get('file')
        audio = WaveDecode(filebuff)
        arr = audio.toCoordinate(width, height, image_ratio)
        return arr
if __name__ == '__main__':
    app.run()
