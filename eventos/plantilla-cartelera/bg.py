from PIL import Image, ImageFilter
import numpy as np
from scipy import ndimage
W,H=1920,1080; rng=np.random.default_rng(7)
src=Image.open('/root/kairus-media/google/show-escenario.jpg').convert('RGB')
src=src.resize((1920,2400)).crop((0,60,1920,1140)).filter(ImageFilter.GaussianBlur(34))
L=np.array(src.convert('L')).astype(float)/255
lo=np.array([10,6,14]); hi=np.array([78,44,94])
base=lo+(hi-lo)*np.clip(L*1.4,0,1)[...,None]
yy,xx=np.mgrid[0:H,0:W]
def blob(cx,cy,rx,ry,c,k):
    d=((xx-cx)/rx)**2+((yy-cy)/ry)**2; return np.exp(-d)[...,None]*np.array(c)*k
base+=blob(560,360,560,380,(206,120,240),0.36)
base+=blob(1650,80,520,300,(206,120,240),0.12)
base+=blob(150,40,420,260,(255,200,170),0.10)
# haces de luz
beams=np.zeros((H,W))
for x0,ang,w in [(430,0.22,90),(820,-0.18,110),(1180,-0.32,70)]:
    xl=x0+(yy)*np.tan(ang); beams+=np.exp(-((xx-xl)/(w+yy*0.18))**2)*np.clip(1-yy/1000,0,1)
base+=ndimage.gaussian_filter(beams,8)[...,None]*np.array([235,215,235])*0.16
# bokeh
bk=np.zeros((H,W,3))
for _ in range(55):
    x,y=rng.uniform(0,W),rng.uniform(0,H*0.8); r=rng.uniform(6,34)
    c=np.array([206,120,240]) if rng.random()<0.6 else np.array([250,225,210])
    m=(((xx-x)**2+(yy-y)**2)<r*r).astype(float); bk+=m[...,None]*c*rng.uniform(0.05,0.18)
bk=ndimage.gaussian_filter(bk,(3,3,0)); base+=bk
# viñeta
v=1-0.55*np.clip(((xx-W*0.4)/(W*0.75))**2+((yy-H*0.45)/(H*0.8))**2,0,1); base*=v[...,None]
Image.fromarray(np.clip(base,0,255).astype('uint8')).save('fx/bg.png')
# niebla (humo) RGBA
n=sum(ndimage.gaussian_filter(rng.random((H//4,W//4)),s)*w for s,w in [(30,1),(12,.6),(5,.3)])
n=(n-n.min())/(n.max()-n.min()); n=np.array(Image.fromarray((n*255).astype('uint8')).resize((W,H),Image.BICUBIC)).astype(float)/255
for name,k,band in [('haze1',0.55,(520,1080)),('haze2',0.8,(700,1080))]:
    g=np.clip((yy-band[0])/(band[1]-band[0]),0,1)
    a=np.clip((n**1.6)*g*k,0,1)*255
    col=np.zeros((H,W,4)); col[...,:3]=[92,58,112]; col[...,3]=a
    Image.fromarray(col.astype('uint8'),'RGBA').save(f'fx/{name}.png')
# fuga de luz superior
lk=np.zeros((H,W,4)); g=np.exp(-(((xx-0)/520)**2+((yy-0)/360)**2))
lk[...,:3]=[255,170,200]; lk[...,3]=g*120; Image.fromarray(lk.astype('uint8'),'RGBA').save('fx/leak.png')
print('ok')
