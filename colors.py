#!/usr/bin/env python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
from os.path import isfile
import itertools
import numpy as np

class ColorLoader:
    links = ["http://www.camelia.sk/dmc_1.htm",
             "http://www.camelia.sk/dmc_2.htm",
             "http://www.camelia.sk/dmc_3.htm",
             "http://www.camelia.sk/dmc_4.htm",
             "http://www.camelia.sk/dmc_5.htm",
             "http://www.camelia.sk/dmc_6.htm"
    ]

    local_file = "/home/anton/apz/xstitch-py/data/dmc.htm"
    
    colors = []
    
    def grouped(self, iterable, n):
        return zip(*[iter(iterable)]*n) #TODO: Figure out if this is optimal.


    class Color:
        def __init__(self, dca_num, color, name="",):
            self.name = name
            self.dca_num = dca_num
            self.color = color
            self.rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
            
        def __str__(self):
            return "{}:\n\tdca: {} \n\tcolor: {} \n\trgb: {}".format(self.name, self.dca_num, self.color, self.rgb)
    
    def load_color_page(self, link):
        page_colors = []
        f = urlopen(link)
        color_file = f.read() #f.read().decode("utf-8")
        #print(f.read())
        bs = BeautifulSoup(color_file, "html.parser")
        
        tags = bs.find_all('tr')
        
        ff = lambda tag : len(tag.attrs) == 0 
        tags = list(filter(ff, tags))
        
        ff = lambda tag : len(list(tag.children)) == 12
        tags = list(filter(ff,tags))
    
        remove_nl = lambda tag : list(filter(lambda child : child != '\n', tag))
        
        tags = list(map(remove_nl, tags))
    
        curr_num=""
        curr_name=""
        curr_color=""
    
        for tag in tags:
            for num, name, color in self.grouped(tag,3):
                page_colors.append(self.Color(num.font.string,
                                         color.attrs['bgcolor'],
                                         name.font.string.replace("\r\n","").replace(" ", "")))

        return page_colors

    def load_colors(self):
        if self.colors:
            return self.colors 
        self.colors = list(itertools.chain.from_iterable(map(self.load_color_page, self.links)))
        return self.colors
    
    def to_np_array(self):
        self.load_colors()
        return np.array(list(map(lambda col: col.rgb, self.colors)))
    
            
