#!/usr/bin/env python3
"""Render a simple original 9:16 Animal Sounds Safari educational video."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np, wave, math, os, subprocess, random

W, H, FPS = 720, 1280, 15
DURATION = 30
OUTDIR = "output"
FRAMEDIR = "/tmp/animal-safari-frames"
os.makedirs(OUTDIR, exist_ok=True)
os.makedirs(FRAMEDIR, exist_ok=True)
random.seed(7)

def font(size, bold=False):
    paths = (["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold else
             ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"])
    for p in paths:
        if os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def centered(draw, xy, text, fnt, fill, stroke_width=0, stroke_fill="#ffffff"):
    draw.text(xy, text, font=fnt, fill=fill, anchor="mm",
              stroke_width=stroke_width, stroke_fill=stroke_fill)

def animal(draw, kind, cx, cy, s=1.0, bounce=0):
    cy += bounce
    # soft shadow
    draw.ellipse((cx-100*s, cy+115*s, cx+100*s, cy+145*s), fill="#b2dca5")
    if kind == "cow":
        body="#fffaf0"; patch="#343a50"
        draw.ellipse((cx-88*s,cy-20*s,cx+88*s,cy+125*s),fill=body,outline="#4c566a",width=4)
        draw.ellipse((cx-72*s,cy+15*s,cx-25*s,cy+65*s),fill=patch)
        draw.ellipse((cx+32*s,cy-5*s,cx+72*s,cy+42*s),fill=patch)
        draw.polygon([(cx-54*s,cy-65*s),(cx-83*s,cy-100*s),(cx-25*s,cy-80*s)],fill="#f5d7bd")
        draw.polygon([(cx+54*s,cy-65*s),(cx+83*s,cy-100*s),(cx+25*s,cy-80*s)],fill="#f5d7bd")
        draw.ellipse((cx-64*s,cy-100*s,cx+64*s,cy+28*s),fill=body,outline="#4c566a",width=4)
        draw.ellipse((cx-39*s,cy-58*s,cx-20*s,cy-33*s),fill="#222b45")
        draw.ellipse((cx+20*s,cy-58*s,cx+39*s,cy-33*s),fill="#222b45")
        draw.ellipse((cx-37*s,cy-12*s,cx+37*s,cy+17*s),fill="#f5a8b7")
        draw.ellipse((cx-20*s,cy-3*s,cx-10*s,cy+7*s),fill="#754a56")
        draw.ellipse((cx+10*s,cy-3*s,cx+20*s,cy+7*s),fill="#754a56")
    elif kind == "duck":
        draw.ellipse((cx-75*s,cy-5*s,cx+78*s,cy+125*s),fill="#ffd84a",outline="#db9e25",width=4)
        draw.ellipse((cx-48*s,cy-92*s,cx+55*s,cy+20*s),fill="#ffe36a",outline="#db9e25",width=4)
        draw.polygon([(cx+37*s,cy-38*s),(cx+98*s,cy-20*s),(cx+39*s,cy-5*s)],fill="#ff8a37")
        draw.ellipse((cx-24*s,cy-57*s,cx-8*s,cy-36*s),fill="#27344c")
        draw.arc((cx-14*s,cy-18*s,cx+20*s,cy+4*s),0,180,fill="#9b5a2a",width=3)
        draw.ellipse((cx-53*s,cy+30*s,cx+22*s,cy+82*s),fill="#fff0a2")
    elif kind == "dog":
        draw.ellipse((cx-77*s,cy-5*s,cx+77*s,cy+125*s),fill="#d99a5e",outline="#965c3b",width=4)
        draw.ellipse((cx-65*s,cy-90*s,cx+65*s,cy+35*s),fill="#e9b77f",outline="#965c3b",width=4)
        draw.ellipse((cx-88*s,cy-80*s,cx-45*s,cy+3*s),fill="#9c6346")
        draw.ellipse((cx+45*s,cy-80*s,cx+88*s,cy+3*s),fill="#9c6346")
        draw.ellipse((cx-35*s,cy-52*s,cx-18*s,cy-30*s),fill="#243047")
        draw.ellipse((cx+18*s,cy-52*s,cx+35*s,cy-30*s),fill="#243047")
        draw.ellipse((cx-25*s,cy-12*s,cx+25*s,cy+21*s),fill="#fff3df")
        draw.ellipse((cx-9*s,cy-8*s,cx+9*s,cy+6*s),fill="#273044")
        draw.arc((cx-16*s,cy-2*s,cx+16*s,cy+25*s),0,180,fill="#9d4653",width=3)
    else: # lion
        draw.ellipse((cx-95*s,cy-115*s,cx+95*s,cy+75*s),fill="#e98d34",outline="#bd5c26",width=4)
        draw.ellipse((cx-67*s,cy-80*s,cx+67*s,cy+55*s),fill="#ffc96b",outline="#bd5c26",width=4)
        draw.ellipse((cx-40*s,cy-45*s,cx-20*s,cy-20*s),fill="#273044")
        draw.ellipse((cx+20*s,cy-45*s,cx+40*s,cy-20*s),fill="#273044")
        draw.ellipse((cx-13*s,cy-8*s,cx+13*s,cy+12*s),fill="#55372c")
        draw.arc((cx-24*s,cy-4*s,cx+24*s,cy+31*s),0,180,fill="#55372c",width=4)
        for dx,dy in [(-78,-75),(70,-70),(-73,5),(70,12)]:
            draw.ellipse((cx+(dx-17)*s,cy+(dy-18)*s,cx+(dx+17)*s,cy+(dy+18)*s),fill="#ffc96b")

def make_scene(t):
    scene = min(4, int(t // 6))
    local = t - scene*6
    bg = ["#b8efff","#c9f6cc","#fff0b8","#d9d0ff","#b8efff"][scene]
    im = Image.new("RGB",(W,H),bg); d=ImageDraw.Draw(im)
    # sun, clouds, rolling hills
    d.ellipse((555,55,650,150),fill="#ffe36b")
    for x,y in [(100,115),(360,85),(515,205)]:
        d.ellipse((x-50,y-18,x+10,y+24),fill="#ffffff")
        d.ellipse((x-20,y-40,x+38,y+25),fill="#ffffff")
        d.ellipse((x+10,y-16,x+60,y+25),fill="#ffffff")
    d.ellipse((-180,760,500,1320),fill="#8fdfa2")
    d.ellipse((250,780,950,1350),fill="#65cf91")
    # confetti sparkles
    for i in range(22):
        x=(i*97+int(t*17))%W; y=(i*131)%700
        d.ellipse((x,y,x+7,y+7),fill=["#ff79a9","#ffcb42","#ffffff","#8d83ff"][i%4])
    titles=["ANIMAL SOUNDS SAFARI!","WHO SAYS MOO?","QUACK, QUACK!","WHO'S A GOOD PUP?","LET'S ROAR!"]
    subtitles=["Listen, guess, and learn!","The cow says...","The duck says...","The dog says...","The lion says..."]
    centered(d,(W//2,245),titles[scene],font(38,True),"#28345b",2)
    centered(d,(W//2,315),subtitles[scene],font(29,True),"#35466d")
    kind = ["cow","cow","duck","dog","lion"][scene]
    animal(d,kind,W//2,650,1.45, int(8*math.sin(local*3)))
    if scene == 0:
        centered(d,(W//2,950),"Ready, little explorers?",font(31,True),"#28345b")
        centered(d,(W//2,1010),"Let's listen carefully!",font(27),"#28345b")
    else:
        labels=["","MOO! MOO!","QUACK! QUACK!","WOOF! WOOF!","ROAR! ROAR!"]
        centered(d,(W//2,950),labels[scene],font(56,True),"#ffffff",4,"#e66b78")
        centered(d,(W//2,1030),"Can you say it too?",font(30,True),"#28345b")
    # footer branding
    d.rounded_rectangle((100,1135,620,1210),radius=30,fill="#ffffff",outline="#ffffff",width=3)
    centered(d,(W//2,1172),"THE LITTLE BRIGHT LAB",font(25,True),"#40518a")
    return im

def synth_audio(path, duration, kind="music"):
    sr=22050; n=int(sr*duration); t=np.arange(n)/sr
    if kind=="music":
        # cheerful, gentle major-key plucks
        out=np.zeros(n,dtype=np.float64)
        notes=[523.25,659.25,783.99,659.25,587.33,698.46,880.0,698.46]
        beat=0.32
        for i,f in enumerate(notes*20):
            start=int(i*beat*sr)
            if start>=n: break
            length=min(int(.22*sr),n-start)
            tt=np.arange(length)/sr
            env=np.exp(-tt*8)
            out[start:start+length] += .11*np.sin(2*np.pi*f*tt)*env
        # soft bass pulse
        out += .035*np.sin(2*np.pi*130.81*t)*(0.5+0.5*np.sin(2*np.pi*1.5*t))
    elif kind=="cow":
        out=.3*np.sin(2*np.pi*(115+8*np.sin(2*np.pi*3*t))*t)*np.exp(-t*1.3)
    elif kind=="duck":
        out=.25*np.sin(2*np.pi*480*t)*np.sin(2*np.pi*7*t)*np.exp(-t*1.8)
    elif kind=="dog":
        out=.25*np.sin(2*np.pi*180*t)*np.sin(2*np.pi*18*t)*np.exp(-t*2)
    else:
        out=.28*np.sin(2*np.pi*95*t)*np.sin(2*np.pi*5*t)*np.exp(-t*1.5)
    out=np.clip(out,-.85,.85)
    stereo=np.column_stack([out,out])
    with wave.open(path,"wb") as wf:
        wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(sr)
        wf.writeframes((stereo*32767).astype(np.int16).tobytes())

# Render frames
for i in range(DURATION*FPS):
    im=make_scene(i/FPS)
    im.save(f"{FRAMEDIR}/frame_{i:04d}.jpg",quality=88)

# Speech: create separate short narration clips, then align them to the timeline
sr=22050
audio=np.zeros(int(DURATION*sr),dtype=np.float64)
def add_clip(path, start, volume=0.82):
    if not os.path.exists(path): return
    with wave.open(path,"rb") as wf:
        data=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float64)/32768
        channels=wf.getnchannels(); rate=wf.getframerate()
        if channels>1: data=data.reshape(-1,channels).mean(axis=1)
        if rate != sr:
            old=np.arange(len(data))/rate; new=np.arange(int(len(data)*sr/rate))/sr
            data=np.interp(new,old,data)
    a=int(start*sr); b=min(len(audio),a+len(data))
    if b>a: audio[a:b] += data[:b-a]*volume

lines=[
 (0.3,"Welcome to Animal Sounds Safari! Let's listen and learn."),
 (6.2,"Who says moo? The cow says moo moo! Can you say moo?"),
 (12.2,"Quack quack! The duck says quack. Your turn!"),
 (18.2,"Woof woof! The puppy says woof. Great listening!"),
 (24.2,"Roar! The lion says roar. Amazing, little explorers!")
]
for idx,(start,line) in enumerate(lines):
    p=f"/tmp/voice_{idx}.wav"
    subprocess.run(["espeak-ng","-v","en-us+f3","-s","145","-p","68","-a","165","-w",p,line],check=True)
    add_clip(p,start,0.88)

# Add stylized synthesized animal cues in each matching scene (not field recordings)
for kind,start in [("cow",8.0),("duck",14.0),("dog",20.0),("lion",26.0)]:
    p=f"/tmp/{kind}.wav"; synth_audio(p,1.0,kind); add_clip(p,start,.35)
# background music
music="/tmp/music.wav"; synth_audio(music,DURATION,"music")
with wave.open(music,"rb") as wf:
    m=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float64)/32768
    m=m.reshape(-1,2).mean(axis=1)
audio += m*.58
# gentle fade at ends and normalize
fade=int(sr*.4)
audio[:fade] *= np.linspace(0,1,fade)
audio[-fade:] *= np.linspace(1,0,fade)
peak=max(0.01,np.max(np.abs(audio)))
audio=np.clip(audio*(0.92/peak),-0.98,.98)
stereo=np.column_stack([audio,audio])
with wave.open("/tmp/safari_audio.wav","wb") as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(sr)
    wf.writeframes((stereo*32767).astype(np.int16).tobytes())

# Encode the numbered frames and mix audio
subprocess.run([
 "ffmpeg","-y","-hide_banner","-loglevel","error",
 "-framerate",str(FPS),"-i",f"{FRAMEDIR}/frame_%04d.jpg",
 "-i","/tmp/safari_audio.wav","-t",str(DURATION),
 "-vf","scale=720:1280,format=yuv420p",
 "-c:v","libx264","-preset","veryfast","-crf","23",
 "-c:a","aac","-b:a","160k","-movflags","+faststart",
 f"{OUTDIR}/animal-sounds-safari.mp4"
],check=True)
print("Created output/animal-sounds-safari.mp4")
