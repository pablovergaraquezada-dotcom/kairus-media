from PIL import Image
from rembg import remove, new_session
import sys
S='/root/kairus-media/stock/artistas/'
crops={
 'angelo':('angelo-2.jpg',(0,120,1010,1080)),
 'erwin':('erwin-claudio.jpg',(780,60,1920,1080)),
 'gaby':('gaby.jpg',(1100,0,1920,1080)),
 'ivan':('ivan-cabello.jpg',(130,330,900,1254)),
 'wilo':('la-wilo.jpg',(0,0,1000,1080)),
 'mexicano':('mexicano.jpg',(0,0,640,941)),
 'tiro':('tirotallas.jpg',(1330,0,1900,900)),
}
s=new_session('isnet-general-use')
for k,(f,b) in crops.items():
  im=Image.open(S+f).convert('RGB').crop(b)
  o=remove(im,session=s,post_process_mask=True)
  o=o.crop(o.getbbox()); o.save(f'cut/{k}.png'); print(k,o.size)
