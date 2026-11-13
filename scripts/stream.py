import numpy as np, json
from PIL import Image
U=[];V=[]
for m in range(1,13):
    a=np.array(Image.open(f'web/data/cur_{m:02d}.png')).astype(np.float32)
    U.append((a[...,0]-128)*0.015); V.append((a[...,1]-128)*0.015); W=a[...,2]>127
u=np.mean(U,0); v=np.mean(V,0); sp=np.hypot(u,v)
H,Wd=u.shape
def samp(A,lon,lat):
    x=(lon+180)/0.25-0.5; y=(90-lat)/0.25-0.5
    x0=int(np.floor(x)); y0=int(np.floor(y)); ax=x-x0; ay=y-y0
    if y0<0 or y0>H-2: return 0.0
    xa=x0%Wd; xb=(x0+1)%Wd
    return A[y0,xa]*(1-ax)*(1-ay)+A[y0,xb]*ax*(1-ay)+A[y0+1,xa]*(1-ax)*ay+A[y0+1,xb]*ax*ay
def water(lon,lat):
    x=int((lon+180)/0.25)%Wd; y=int((90-lat)/0.25)
    return 0<=y<H and W[y,x]
OC=1.1  # occupancy cell deg
occ=np.zeros((int(180/OC),int(360/OC)),bool)
def ocell(lon,lat): return int((90-lat)/OC)%occ.shape[0], int(((lon+180)%360)/OC)%occ.shape[1]
STEP=0.22
def trace(lon,lat,sign):
    pts=[]; mine=set()
    for i in range(400):
        uu=samp(u,lon,lat); vv=samp(v,lon,lat); s=np.hypot(uu,vv)
        if s<0.04 or not water(lon,lat) or abs(lat)>78: break
        c=ocell(lon,lat)
        if occ[c] and c not in mine: break
        mine.add(c); pts.append((lon,lat,s))
        c0=np.cos(np.radians(lat))
        dx=sign*uu/s*STEP/c0; dy=sign*vv/s*STEP
        lon=(lon+dx+180)%360-180; lat+=dy
    return pts,mine
lines=[]
seeds=[(lo,la) for la in np.arange(-76,78,1.1) for lo in np.arange(-180,180,1.1)]
order=np.argsort([-samp(sp,lo,la) for lo,la in seeds])
for k in order:
    lo,la=seeds[k]
    if not water(lo,la) or occ[ocell(lo,la)] or samp(sp,lo,la)<0.06: continue
    f,mf=trace(lo,la,1); b,mb=trace(lo,la,-1)
    pts=b[::-1]+f[1:]
    if len(pts)<12: continue
    for c in mf|mb: occ[c]=True
    lines.append(pts)
feats=[]
for pts in lines:
    # split at dateline jumps and into chunks of ~8 vertices with mean speed
    seg=[pts[0]]
    def flush(seg):
        if len(seg)>1:
            feats.append({'type':'Feature','properties':{'s':round(float(np.mean([p[2] for p in seg])),2)},
              'geometry':{'type':'LineString','coordinates':[[round(p[0],2),round(p[1],2)] for p in seg]}})
    for p in pts[1:]:
        if abs(p[0]-seg[-1][0])>180: flush(seg); seg=[p]; continue
        seg.append(p)
        if len(seg)>=12: flush(seg); seg=[p]
    flush(seg)
json.dump({'type':'FeatureCollection','features':feats},open('web/data/streams.json','w'),separators=(',',':'))
print(len(lines),'lines',len(feats),'segments')
