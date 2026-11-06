from PIL import Image, ImageDraw, ImageOps, ImageFilter, ImageChops
import numpy as np, json
from scipy import ndimage
W,H=1920,1080
CREMA=(242,234,220); LILA=(206,120,240); NOCHE=(14,11,16)
def clean(a):
    m=a>40; lab,n=ndimage.label(m)
    if n>1:
        s=ndimage.sum(m,lab,range(1,n+1)); a=np.where(lab==np.argmax(s)+1,a,0)
    return a
def dots(L, cell, ang, fn, ss=3):
    """L: float array 0..1 (h,w). devuelve máscara 0..255 de puntos"""
    h,w=L.shape
    im=Image.fromarray((L*255).astype('uint8')).rotate(ang,expand=True,resample=Image.BILINEAR,fillcolor=0)
    R=np.array(im).astype(float)/255; rh,rw=R.shape
    out=Image.new('L',(rw*ss,rh*ss),0); d=ImageDraw.Draw(out)
    for y in range(0,rh,cell):
        for x in range(0,rw,cell):
            v=R[y:y+cell,x:x+cell].mean()
            r=fn(v)*cell*0.72*ss
            if r>0.35*ss:
                cx,cy=(x+cell/2)*ss,(y+cell/2)*ss; d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=255)
    out=out.resize((rw,rh),Image.LANCZOS).rotate(-ang,expand=True,resample=Image.BILINEAR)
    ow,oh=out.size; l=(ow-w)//2; t=(oh-h)//2
    return np.array(out.crop((l,t,l+w,t+h))).astype(float)
def person(k,h,crop=None,fade=0.0,depth=1.0,cell=5):
    im=Image.open(f'cut/{k}.png').convert('RGBA')
    if crop: im=im.crop(crop)
    im=im.crop(im.getbbox()); w=int(im.width*h/im.height); im=im.resize((w,h),Image.LANCZOS)
    a=clean(np.array(im)[...,3]).astype(float)/255
    a=np.clip((a-0.3)/0.5,0,1)
    if fade:
        s=int(h*(1-fade)); g=np.ones(h); g[s:]=np.linspace(1,0,h-s)**1.2; a=a*g[:,None]
    g=ImageOps.grayscale(im.convert('RGB'))
    g=ImageOps.autocontrast(g,cutoff=1.5)
    g=g.filter(ImageFilter.UnsharpMask(radius=6,percent=90,threshold=2))
    L=np.array(g).astype(float)/255
    L=np.clip((L-0.52)*1.18+0.5,0,1)
    t=L**1.1
    smooth=np.array(NOCHE,float)*(1-t[...,None])+np.array(CREMA,float)*t[...,None]
    lil=dots(L,cell,20,lambda v: 0.95*np.exp(-((v-0.34)/0.2)**2))
    cre=dots(L,cell,45,lambda v: max(0,v-0.55)*1.9)
    col=smooth.copy()
    lm=(lil/255)[...,None]*0.75; col=col*(1-lm)+np.array(LILA)*lm
    cm=(cre/255)[...,None]*0.35; col=col*(1-cm)+np.array(CREMA)*cm
    col=col*depth+np.array([40,24,52])*(1-depth)
    rgba=np.zeros((h,w,4))
    rgba[...,:3]=col; rgba[...,3]=a*255
    body=Image.fromarray(rgba.astype('uint8'),'RGBA')
    # pase lila corrido (silueta desplazada)
    sil=np.zeros((h,w,4)); sil[...,:3]=LILA; sil[...,3]=ndimage.binary_erosion(a>0.5,iterations=2)*255*(0.8 if depth>0.9 else 0.45)
    return body, Image.fromarray(sil.astype('uint8'),'RGBA')
def spotlight():
    yy,xx=np.mgrid[0:H,0:W]
    g=np.exp(-(((xx-640)/620)**2+((yy-560)/420)**2))*0.75+np.exp(-(((xx-1100)/380)**2+((yy-700)/300)**2))*0.35
    m=dots(np.clip(g,0,1),9,30,lambda v: v**1.1)
    o=np.zeros((H,W,4)); o[...,:3]=LILA; o[...,3]=m*0.55
    return Image.fromarray(o.astype('uint8'),'RGBA')
def paper():
    rng=np.random.default_rng(3)
    n=ndimage.gaussian_filter(rng.random((H,W)),1.2); n2=ndimage.gaussian_filter(rng.random((H//6,W//6)),4)
    n2=np.array(Image.fromarray(((n2-n2.min())/(n2.max()-n2.min())*255).astype('uint8')).resize((W,H),Image.BICUBIC)).astype(float)/255
    v=(n-n.mean())*60+(n2-0.5)*14
    base=np.array(NOCHE,float)+v[...,None]*np.array([1,0.9,1.1])
    return Image.fromarray(np.clip(base,0,255).astype('uint8')).convert('RGBA')
if __name__=='__main__':
    D=json.load(open('datos3.json'))
    bg=paper(); bg.alpha_composite(spotlight()); bg.save('fx/riso_bg.png')
    canvas=Image.new('RGBA',(W,H),(0,0,0,0))
    for p in D['people']:
        b,s=person(p['f'],p['h'],crop=tuple(p['crop']) if p.get('crop') else None,fade=p.get('fade',0),depth=p.get('depth',1.0),cell=p.get('cell',5))
        x=p['x']; y=H-p.get('b',0)-p['h']
        canvas.alpha_composite(s,(x+p.get('ox',10),y+p.get('oy',8)) if x+10>=0 else (0,0)) if False else None
        # pegar con offset seguro
        def paste(img,x,y):
            l=max(0,-x); t=max(0,-y); img=img.crop((l,t,img.width,img.height)); canvas.alpha_composite(img,(max(0,x),max(0,y)))
        paste(s,x+7,y+5); paste(b,x,y)
    A=np.array(canvas).astype(float); xx=np.arange(W)[None,:]
    A[...,3]*=np.clip((1450-xx)/90,0,1); canvas=Image.fromarray(A.astype('uint8'),'RGBA')
    canvas.save('fx/riso_people.png'); print('ok')
