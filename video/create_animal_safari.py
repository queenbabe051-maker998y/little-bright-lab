#!/usr/bin/env python3
"""Create a lively, original 9:16 Animal Sounds Safari short."""
from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment
import math, os, random, subprocess

W,H,FPS,DURATION=720,1280,20,36
FRAMES="/tmp/lbl-frames"; OUT="output/animal-sounds-safari.mp4"
os.makedirs(FRAMES,exist_ok=True); os.makedirs("output",exist_ok=True)
random.seed(14)

def font(n,b=False):
    p="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if b else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p,n)
def txt(d,xy,s,n,fill="#fff",b=True,anchor="mm",stroke=0,outline="#24305e"):
    d.text(xy,s,font=font(n,b),fill=fill,anchor=anchor,stroke_width=stroke,stroke_fill=outline)
def rounded(d,box,fill,outline=None,r=28,w=3):
    d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=w)
def star(d,x,y,r,c):
    pts=[]
    for i in range(10):
        a=-math.pi/2+i*math.pi/5; rr=r if i%2==0 else r*.42
        pts.append((x+math.cos(a)*rr,y+math.sin(a)*rr))
    d.polygon(pts,fill=c)
def mascot(d,cx,cy,t,scale=1):
    # Original recurring mascot: Pip, a turquoise baby dragon with a golden crest and star freckles.
    bob=math.sin(t*5)*9
    cy+=bob
    s=scale
    # tail and feet
    d.polygon([(cx+48*s,cy+58*s),(cx+110*s,cy+88*s),(cx+88*s,cy+32*s)],fill="#19b8b3")
    d.ellipse((cx-58*s,cy+75*s,cx-8*s,cy+112*s),fill="#159d9f")
    d.ellipse((cx+8*s,cy+75*s,cx+58*s,cy+112*s),fill="#159d9f")
    # wings
    d.polygon([(cx-42*s,cy+20*s),(cx-92*s,cy-20*s),(cx-80*s,cy+52*s)],fill="#77e5d1",outline="#087e91")
    d.polygon([(cx+42*s,cy+20*s),(cx+92*s,cy-20*s),(cx+80*s,cy+52*s)],fill="#77e5d1",outline="#087e91")
    # head/body
    d.ellipse((cx-65*s,cy-42*s,cx+65*s,cy+91*s),fill="#21c9c2",outline="#087e91",width=max(2,int(4*s)))
    d.ellipse((cx-75*s,cy-104*s,cx+75*s,cy+30*s),fill="#36d8ca",outline="#087e91",width=max(2,int(4*s)))
    # crest
    d.polygon([(cx-32*s,cy-94*s),(cx-50*s,cy-133*s),(cx-5*s,cy-107*s),
               (cx+15*s,cy-145*s),(cx+29*s,cy-99*s),(cx+53*s,cy-119*s),(cx+47*s,cy-80*s)],fill="#ffcb45")
    # cheeks, eyes, smile
    d.ellipse((cx-57*s,cy-34*s,cx-30*s,cy-10*s),fill="#ff9ab7")
    d.ellipse((cx+30*s,cy-34*s,cx+57*s,cy-10*s),fill="#ff9ab7")
    d.ellipse((cx-40*s,cy-69*s,cx-13*s,cy-35*s),fill="#fff")
    d.ellipse((cx+13*s,cy-69*s,cx+40*s,cy-35*s),fill="#fff")
    d.ellipse((cx-30*s,cy-60*s,cx-17*s,cy-39*s),fill="#27365f")
    d.ellipse((cx+17*s,cy-60*s,cx+30*s,cy-39*s),fill="#27365f")
    d.ellipse((cx-26*s,cy-57*s,cx-21*s,cy-51*s),fill="#fff")
    d.ellipse((cx+21*s,cy-57*s,cx+26*s,cy-51*s),fill="#fff")
    d.arc((cx-24*s,cy-36*s,cx+24*s,cy+1*s),5,170,fill="#14586c",width=max(2,int(4*s)))
    for dx,dy in [(-48,-83),(49,-81),(-44,7),(47,10)]:
        star(d,cx+dx*s,cy+dy*s,5*s,"#fff3a8")

def draw_animal(d,kind,cx,cy,t,s=1):
    cy+=math.sin(t*5)*8
    # ground shadow
    d.ellipse((cx-130*s,cy+140*s,cx+130*s,cy+170*s),fill="#a1dca6")
    if kind=="cow":
        d.ellipse((cx-95*s,cy-4*s,cx+95*s,cy+145*s),fill="#fffaf1",outline="#45516f",width=4)
        d.ellipse((cx-78*s,cy+22*s,cx-28*s,cy+82*s),fill="#34415e")
        d.ellipse((cx+36*s,cy+6*s,cx+76*s,cy+60*s),fill="#34415e")
        d.polygon([(cx-50*s,cy-66*s),(cx-90*s,cy-115*s),(cx-18*s,cy-91*s)],fill="#f7c6d2")
        d.polygon([(cx+50*s,cy-66*s),(cx+90*s,cy-115*s),(cx+18*s,cy-91*s)],fill="#f7c6d2")
        d.ellipse((cx-72*s,cy-112*s,cx+72*s,cy+34*s),fill="#fffaf1",outline="#45516f",width=4)
        d.ellipse((cx-43*s,cy-67*s,cx-20*s,cy-36*s),fill="#25304e")
        d.ellipse((cx+20*s,cy-67*s,cx+43*s,cy-36*s),fill="#25304e")
        d.ellipse((cx-43*s,cy-15*s,cx+43*s,cy+25*s),fill="#f5a9bd")
        d.ellipse((cx-23*s,cy-3*s,cx-12*s,cy+10*s),fill="#9b5c75"); d.ellipse((cx+12*s,cy-3*s,cx+23*s,cy+10*s),fill="#9b5c75")
        d.ellipse((cx-16*s,cy-124*s,cx+16*s,cy-93*s),fill="#f3bd45")
    elif kind=="duck":
        d.ellipse((cx-85*s,cy-5*s,cx+80*s,cy+145*s),fill="#ffcf42",outline="#dc9a24",width=4)
        d.ellipse((cx-60*s,cy-110*s,cx+58*s,cy+30*s),fill="#ffe36a",outline="#dc9a24",width=4)
        d.polygon([(cx+36*s,cy-45*s),(cx+112*s,cy-22*s),(cx+40*s,cy-5*s)],fill="#ff813c")
        d.ellipse((cx-31*s,cy-70*s,cx-10*s,cy-43*s),fill="#27324c")
        d.ellipse((cx-26*s,cy-66*s,cx-20*s,cy-60*s),fill="#fff")
        d.ellipse((cx-56*s,cy+30*s,cx+28*s,cy+85*s),fill="#fff0a3")
        d.ellipse((cx-53*s,cy+136*s,cx-3*s,cy+151*s),fill="#ff9138")
        d.ellipse((cx+9*s,cy+136*s,cx+58*s,cy+151*s),fill="#ff9138")
    elif kind=="dog":
        d.ellipse((cx-85*s,cy-3*s,cx+85*s,cy+145*s),fill="#d99a5e",outline="#925a3e",width=4)
        d.ellipse((cx-72*s,cy-105*s,cx+72*s,cy+37*s),fill="#edbd87",outline="#925a3e",width=4)
        d.ellipse((cx-104*s,cy-89*s,cx-48*s,cy+15*s),fill="#9e6247")
        d.ellipse((cx+48*s,cy-89*s,cx+104*s,cy+15*s),fill="#9e6247")
        d.ellipse((cx-42*s,cy-68*s,cx-20*s,cy-39*s),fill="#25304e")
        d.ellipse((cx+20*s,cy-68*s,cx+42*s,cy-39*s),fill="#25304e")
        d.ellipse((cx-33*s,cy-19*s,cx+33*s,cy+28*s),fill="#fff1de")
        d.ellipse((cx-12*s,cy-12*s,cx+12*s,cy+7*s),fill="#25304e")
        d.arc((cx-20*s,cy-2*s,cx+20*s,cy+32*s),0,180,fill="#a34458",width=4)
        d.ellipse((cx-15*s,cy+14*s,cx+15*s,cy+43*s),fill="#f36b91")
    else: # friendly lion
        d.ellipse((cx-112*s,cy-130*s,cx+112*s,cy+95*s),fill="#f28a37",outline="#bd5a2d",width=4)
        for a in range(12):
            ang=a*math.pi/6
            x=cx+105*s*math.cos(ang); y=cy-20*s+105*s*math.sin(ang)
            d.ellipse((x-22*s,y-22*s,x+22*s,y+22*s),fill="#ffb34f")
        d.ellipse((cx-72*s,cy-96*s,cx+72*s,cy+47*s),fill="#ffd078",outline="#bd5a2d",width=4)
        d.ellipse((cx-42*s,cy-61*s,cx-20*s,cy-33*s),fill="#25304e")
        d.ellipse((cx+20*s,cy-61*s,cx+42*s,cy-33*s),fill="#25304e")
        d.ellipse((cx-14*s,cy-20*s,cx+14*s,cy+2*s),fill="#57392f")
        d.arc((cx-29*s,cy-12*s,cx+29*s,cy+34*s),0,180,fill="#57392f",width=4)

ANIMALS=[
 {"kind":"cow","title":"WHO SAYS MOO?","sound":"MOO! MOO!","prompt":"Listen closely...","voice":"Listen carefully! Who makes this sound?","reveal":"A COW! The cow says MOO!","sound_start":6.0},
 {"kind":"duck","title":"WHO GOES QUACK?","sound":"QUACK! QUACK!","prompt":"Can you guess?","voice":"Who goes quack, quack? Take a guess!","reveal":"A DUCK! The duck says QUACK!","sound_start":12.0},
 {"kind":"dog","title":"WHO SAYS WOOF?","sound":"WOOF! WOOF!","prompt":"You know this one!","voice":"Who says woof, woof? Can you guess?","reveal":"A PUPPY! The puppy says WOOF!","sound_start":18.0},
 {"kind":"lion","title":"WHO GOES ROAR?","sound":"ROAR! ROAR!","prompt":"A jungle mystery!","voice":"Listen to this big jungle sound!","reveal":"A LION! The lion says ROAR!","sound_start":24.0},
]
def scene_for(t):
    if t<4: return -1
    if t<28: return min(3,int((t-4)//6))
    return 4
def frame(t):
    sc=scene_for(t)
    bgs=["#6bd9f2","#8be6c1","#ffd76b","#b7a6ff","#ff9fc3"]
    bg=bgs[max(0,sc)]
    im=Image.new("RGB",(W,H),bg); d=ImageDraw.Draw(im)
    # layered rolling hills
    d.ellipse((-160,820,500,1450),fill="#77d99c")
    d.ellipse((220,850,900,1450),fill="#48c98e")
    # dynamic bubbles and sparkles
    colors=["#fff3a8","#ff83b7","#ffffff","#917bff"]
    for i in range(26):
        x=(i*137+int(t*42))%W; y=(i*89+int(math.sin(t+i)*14))%780
        if i%3==0: star(d,x,y,8+(i%3)*2,colors[i%4])
        else: d.ellipse((x,y,x+7,y+7),fill=colors[i%4])
    d.ellipse((565,60,660,155),fill="#fff0a1")
    # header capsule
    rounded(d,(35,35,685,115),"#ffffff")
    txt(d,(360,75),"THE LITTLE BRIGHT LAB",25,"#34416f",True)
    if sc==-1:
        txt(d,(360,205),"ANIMAL SOUND",51,"#fff",True,stroke=3,outline="#40518b")
        txt(d,(360,270),"SAFARI!",64,"#fff",True,stroke=4,outline="#f15f98")
        txt(d,(360,350),"LISTEN • GUESS • ROAR!",25,"#34416f",True)
        mascot(d,360,665,t,1.5)
        rounded(d,(85,940,635,1050),"#fff")
        txt(d,(360,985),"Can you guess the animal?",29,"#35416f",True)
        txt(d,(360,1100),"Ready, explorers?",27,"#fff",True,stroke=2,outline="#40518b")
    elif sc in range(4):
        a=ANIMALS[sc]; local=(t-4)%6
        txt(d,(360,190),a["title"],36,"#fff",True,stroke=3,outline="#35416f")
        rounded(d,(100,240,620,310),"#fff")
        txt(d,(360,275),a["prompt"],27,"#35416f",True)
        # mystery phase hides animal until sound has played; then pop reveal
        if local<2.6:
            # big mystery question mark and Pip pointing
            mascot(d,255,635,t,1.0)
            rounded(d,(395,450,585,650),"#fff","#ff79ad",5,34)
            txt(d,(490,545),"?",108,"#ff70a6",True)
            txt(d,(360,835),"WHAT ANIMAL IS IT?",29,"#fff",True,stroke=2,outline="#40518b")
            txt(d,(360,895),"Listen... then guess!",24,"#35416f",True)
        else:
            # animal revealed with a celebratory burst
            for j in range(12):
                ang=j*math.pi/6
                star(d,360+190*math.cos(ang),570+190*math.sin(ang),13,"#fff3a8")
            draw_animal(d,a["kind"],360,610,t,1.13)
            rounded(d,(80,830,640,940),"#fff","#ff83b7",4,32)
            txt(d,(360,875),a["sound"],53,"#f15f87",True)
            txt(d,(360,1000),a["reveal"],24,"#34416f",True)
            mascot(d,360,1090,t,.48)
    else:
        txt(d,(360,205),"SUPER SOUND",46,"#fff",True,stroke=3,outline="#40518b")
        txt(d,(360,265),"RECAP!",60,"#fff",True,stroke=4,outline="#f15f98")
        # four mini animal tiles for quick recall
        for i,a in enumerate(ANIMALS):
            x=28+i*171
            rounded(d,(x,390,x+155,700),"#fff",None,24)
            draw_animal(d,a["kind"],x+77,515,t+i,.48)
            txt(d,(x+77,630),["COW","DUCK","PUPPY","LION"][i],19,"#34416f",True)
            txt(d,(x+77,667),["MOO!","QUACK!","WOOF!","ROAR!"][i],19,"#f15f87",True)
        mascot(d,360,880,t,.9)
        rounded(d,(70,1030,650,1130),"#fff")
        txt(d,(360,1080),"You are a SOUND STAR!",29,"#34416f",True)
    return im

# Render a lively, clean frame sequence.
for i in range(DURATION*FPS):
    frame(i/FPS).save(f"{FRAMES}/f{i:04d}.jpg",quality=91)

# Audio: real animal calls are downloaded by the workflow; voice and music are mixed underneath.
sr=22050
music=AudioSegment.silent(duration=DURATION*1000,frame_rate=sr).set_channels(2)
# cheerful original instrumental loop, no third-party music
notes=[523.25,659.25,783.99,659.25,587.33,698.46,880.0,698.46]
import numpy as np, wave
samples=np.zeros(int(sr*DURATION),dtype=np.float32)
for i in range(int(DURATION/.32)):
    start=int(i*.32*sr); f=notes[i%len(notes)]; length=min(int(.24*sr),len(samples)-start)
    tt=np.arange(length)/sr
    samples[start:start+length]+=(.12*np.sin(2*np.pi*f*tt)*np.exp(-tt*7)).astype(np.float32)
    samples[start:start+length]+=(.025*np.sin(2*np.pi*(f/2)*tt)*np.exp(-tt*5)).astype(np.float32)
samples=np.clip(samples,-.7,.7)
st=np.column_stack([samples,samples])
with wave.open("/tmp/lbl-music.wav","wb") as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes((st*32767).astype(np.int16).tobytes())
music=AudioSegment.from_wav("/tmp/lbl-music.wav")-20
voice=AudioSegment.silent(duration=DURATION*1000,frame_rate=sr).set_channels(2)
def add_voice(start,text):
    p=f"/tmp/lbl-voice-{start}.wav"
    subprocess.run(["espeak-ng","-v","en-us+f3","-s","158","-p","72","-a","170","-w",p,text],check=True)
    clip=AudioSegment.from_wav(p).set_frame_rate(sr).set_channels(2)+2
    voice.overlay(clip,position=int(start*1000))
# add voice via reassignment because pydub overlay returns a new segment
def voice_at(start,text):
    global voice
    p=f"/tmp/lbl-voice-{start}.mp3"
    subprocess.run(["edge-tts","--voice","en-US-AnaNeural","--rate","+8%","--pitch","+4Hz","--text",text,"--write-media",p],check=True)
    clip=AudioSegment.from_file(p).set_frame_rate(sr).set_channels(2)+2
    voice=voice.overlay(clip,position=int(start*1000))
voice_at(.25,"Welcome to Animal Sound Safari! Listen, guess, and learn with Pip!")
for i,a in enumerate(ANIMALS):
    start=4+i*6
    voice_at(start+.15,a["voice"])
    # name reveal starts after a pause for guessing
    voice_at(start+3.1,a["reveal"])
# finale prompt
voice_at(28.3,"Cow says moo! Duck says quack! Puppy says woof! Lion says roar! You're a sound star!")
mix=music.overlay(voice)
# insert real animal sounds at the mystery moment; audio names are downloaded by workflow
for kind,start in [("cow",6.15),("duck",12.15),("dog",18.15),("lion",24.15)]:
    p=f"assets/sounds/{kind}.mp3"
    if os.path.exists(p):
        clip=AudioSegment.from_file(p).set_frame_rate(sr).set_channels(2)
        # keep short, clear and prominent, with a small fade
        clip=clip[:2200].fade_in(80).fade_out(180)-3
        mix=mix.overlay(clip,position=int(start*1000))
mix=mix.fade_in(350).fade_out(700)
mix.export("/tmp/lbl-final-audio.wav",format="wav")
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-framerate",str(FPS),"-i",f"{FRAMES}/f%04d.jpg","-i","/tmp/lbl-final-audio.wav","-t",str(DURATION),"-vf","scale=720:1280,format=yuv420p","-c:v","libx264","-preset","veryfast","-crf","21","-c:a","aac","-b:a","160k","-movflags","+faststart",OUT],check=True)
print("Created",OUT)
