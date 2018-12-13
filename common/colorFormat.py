#!/usr/bin/env python

def color_format(content,fontcolor='default',background='default',mode='default',length=0):
    fc = {'default':0,'black':30,'red':31,'green':32,'yellow':33,'blue':34,'purple':35,'white':37}
    bg = {'default':0,'black':40,'red':41,'green':42,'yellow':43,'blue':44,'purple':45,'white':47}
    dm = {'default':0,'highlight':1,'underline':4,'twinkle':5,'invisible':8}
    result = '\033[%d;%d;%dm' %(fc[fontcolor],bg[background],dm[mode])
    content_format = '%' + '%ss' % length
    content = content_format % content
    result = result + content
    result = result + '\033[m'
    return result


if __name__ == '__main__':
    content = 'hello'
    content = color_format(content,fontcolor='red',mode='highlight',background='yellow',length=20)
    # content = color_format(content)
    print content