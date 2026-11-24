from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import numpy as np, os
from scipy import ndimage
os.makedirs('fx',exist_ok=True)
STOPS=[(0.0,(9,5,12)),(0.38,(62,38,76)),(0.72,(196,168,176)),(1.0,(250,240,226))]
def gmap(t):
    out=np.zeros(t.shape+(3,))
    for (p0,c0),(p1,c1) in zip(STOPS,STOPS[1:]):
        m=(t>=p0)&(t<=p1); u=((t-p0)/(p1-p0))[m][:,None]
        out[m]=np.array(c0)*(1-u)+np.array(c1)*u
    return out
def clean(a):
    m=a>40; lab,n=ndimage.label(m)
    if n>1:
        s=ndimage.sum(m,lab,range(1,n+1)); a=np.where(lab==np.argmax(s)+1,a,0)
    return a
def proc(k, crop=None, fadebottom=0.0):
    im=Image.open(f'cut/{k}.png').convert('RGBA')
    if crop: im=im.crop(crop)
    rgb=np.array(im.convert('RGB')).astype(float); a=clean(np.array(im)[...,3]).astype(float)
    if fadebottom:
        h=a.shape[0]; s=int(h*(1-fadebottom)); g=np.ones(h); g[s:]=np.linspace(1,0,h-s)**1.3; a*=g[:,None]
    L=np.array(ImageOps.autocontrast(Image.fromarray(rgb.astype('uint8')).convert('L'),cutoff=0.8)).astype(float)/255
    L=np.clip((L-0.5)*1.12+0.5,0,1)
    g=gmap(L); col=g*0.7+rgb*0.3
    # rim light lila desde arriba
    A=a/255; inner=ndimage.gaussian_filter(A,2.5); rim=np.clip(A-inner,0,1)*A
    yy=np.linspace(1.0,0.35,A.shape[0])[:,None]; rim=ndimage.gaussian_filter(np.clip(rim*2.2*yy,0,1),1.0)
    lila=np.array([206,120,240])
    col=col*(1-rim[...,None]*0.7)+lila*rim[...,None]*0.7
    # sombra suave en la base
    out=np.dstack([np.clip(col,0,255),a]).astype('uint8')
    o=Image.fromarray(out,'RGBA'); o=o.crop(o.getbbox()); o.save(f'fx/{k}.png')
    # variante de fondo: desenfoque + niebla
    b=np.array(o).astype(float); fog=np.array([58,35,72])
    b[...,:3]=b[...,:3]*0.8+fog*0.2
    ob=Image.fromarray(b.astype('uint8'),'RGBA').filter(ImageFilter.GaussianBlur(2.2)); ob.save(f'fx/{k}_b.png')
    print(k,o.size)
for k in ['wilo','gaby','tiro','mexicano','erwin','botota','creici']: proc(k)
proc('ivan',crop=(0,0,10**4,585),fadebottom=0.18)
proc('angelo',fadebottom=0.3)
