from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np
from scipy import ndimage
import os
os.makedirs('prep',exist_ok=True)
def biggest(a):
    m=a>40; lab,n=ndimage.label(m)
    if n>1:
        sizes=ndimage.sum(m,lab,range(1,n+1)); keep=np.argmax(sizes)+1
        a=np.where(lab==keep,a,0)
    return a
# duotone: noche #0e0b10 -> crema #f2eadc, contrast up
lo=np.array([14,11,16]); hi=np.array([242,234,220])
for k in ['angelo','erwin']:
    im=Image.open(f'cut/{k}.png').convert('RGBA')
    if k=='ivan': im=im.crop((0,0,im.width,585))
    r,g,b,a=im.split()
    a=Image.fromarray(biggest(np.array(a)).astype('uint8'))
    l=ImageOps.grayscale(im.convert('RGB'))
    l=ImageOps.autocontrast(l,cutoff=1)
    l=ImageEnhance.Contrast(l).enhance(1.15)
    t=np.array(l)/255.0
    t=np.clip(t,0,1)**1.05
    rgb=(lo[None,None,:]*(1-t[...,None])+hi[None,None,:]*t[...,None]).astype('uint8')
    o=Image.fromarray(rgb).convert('RGBA'); o.putalpha(a)
    o=o.crop(o.getbbox()); o.save(f'prep/{k}.png'); print(k,o.size)
