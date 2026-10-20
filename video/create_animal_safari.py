#!/usr/bin/env python3
"""Create a lively, original 9:16 Animal Sounds Safari short."""
from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment
import math, os, random, subprocess

W,H,FPS,DURATION=720,1280,12,90
FRAMES="/tmp/lbl-frames"; OUT="output/little-bright-lab-learning-show.mp4"
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

# A longer original preschool learning-show episode.
ANIMALS=[
 {"kind":"cow","title":"C IS FOR COW!","sound":"MOO! MOO!","voice":"Listen carefully! What animal says moo?","reveal":"COW! C is for cow. The cow says moo!","sound_start":9.0},
 {"kind":"duck","title":"D IS FOR DUCK!","sound":"QUACK! QUACK!","voice":"Can you hear the quack quack?","reveal":"DUCK! D is for duck. The duck says quack!","sound_start":17.0},
 {"kind":"dog","title":"D IS FOR DOG!","sound":"WOOF! WOOF!","voice":"Who says woof? Make your best puppy sound!","reveal":"DOG! D is for dog. The dog says woof!","sound_start":25.0},
 {"kind":"lion","title":"L IS FOR LION!","sound":"ROAR! ROAR!","voice":"A big jungle sound! Who could it be?","reveal":"LION! L is for lion. The lion says roar!","sound_start":33.0},
]
def scene_for(t):
    if t<5: return -1
    if t<37: return min(3,int((t-5)//8))
    if t<54: return 4
    if t<69: return 5
    if t<88: return 6
    return 7

def frame(t):
    sc=scene_for(t)
    bgs=["#71dff5","#8be6c1","#ffd76b","#b7a6ff","#ff9fc3","#7bdcf4","#ffd76b","#a9edc4"]
    im=Image.new("RGB",(W,H),bgs[max(0,sc)]); d=ImageDraw.Draw(im)
    d.ellipse((-160,820,500,1450),fill="#77d99c")
    d.ellipse((220,850,900,1450),fill="#48c98e")
    colors=["#fff3a8","#ff83b7","#ffffff","#917bff"]
    for i in range(26):
        x=(i*137+int(t*42))%W; y=(i*89+int(math.sin(t+i)*14))%780
        if i%3==0: star(d,x,y,8+(i%3)*2,colors[i%4])
        else: d.ellipse((x,y,x+7,y+7),fill=colors[i%4])
    d.ellipse((565,60,660,155),fill="#fff0a1")
    rounded(d,(35,35,685,115),"#ffffff")
    txt(d,(360,75),"THE LITTLE BRIGHT LAB",25,"#34416f",True)
    if sc==-1:
        txt(d,(360,205),"LEARN & PLAY!",57,"#fff",True,stroke=4,outline="#40518b")
        txt(d,(360,275),"ANIMAL SOUNDS • ABCs • COUNTING",22,"#34416f",True)
        mascot(d,360,640,t,1.55)
        rounded(d,(70,900,650,1010),"#fff")
        txt(d,(360,955),"Let's learn together!",34,"#f15f87",True)
        txt(d,(360,1080),"Sing, count, and smile!",28,"#fff",True,stroke=2,outline="#40518b")
    elif sc in range(4):
        a=ANIMALS[sc]; local=(t-5)%8
        txt(d,(360,190),a["title"],39,"#fff",True,stroke=3,outline="#35416f")
        rounded(d,(90,235,630,305),"#fff")
        txt(d,(360,270),"LISTEN AND GUESS!",28,"#35416f",True)
        if local<3.8:
            mascot(d,250,620,t,1.0)
            rounded(d,(395,440,585,640),"#fff","#ff79ad",5,34)
            txt(d,(490,535),"?",108,"#ff70a6",True)
            txt(d,(360,820),"WHAT ANIMAL IS IT?",29,"#fff",True,stroke=2,outline="#40518b")
            txt(d,(360,885),"Think... think... think!",25,"#35416f",True)
        else:
            for j in range(12):
                ang=j*math.pi/6; star(d,360+190*math.cos(ang),550+190*math.sin(ang),13,"#fff3a8")
            draw_animal(d,a["kind"],360,590,t,1.13)
            rounded(d,(80,810,640,925),"#fff","#ff83b7",4,32)
            txt(d,(360,850),a["sound"],52,"#f15f87",True)
            txt(d,(360,895),a["reveal"],22,"#34416f",True)
            mascot(d,360,1080,t,.48)
    elif sc==4:
        txt(d,(360,190),"ABC ADVENTURE!",47,"#fff",True,stroke=3,outline="#40518b")
        txt(d,(360,255),"Sing the letters with Pip!",27,"#34416f",True)
        letters=list("ABCDEF")
        for i,L in enumerate(letters):
            x=65+i*118; y=430+math.sin(t*4+i)*25
            rounded(d,(x,y,x+105,y+140),["#ff83b7","#ffe36a","#77dfc5","#b7a6ff","#ffad6b","#71dff5"][i],None,22)
            txt(d,(x+52,y+70),L,67,"#fff",True,stroke=2,outline="#35416f")
        mascot(d,360,760,t,.85)
        rounded(d,(65,930,655,1035),"#fff")
        txt(d,(360,980),"A, B, C, D, E, F!",35,"#f15f87",True)
        txt(d,(360,1090),"A is for apple! B is for ball!",23,"#34416f",True)
    elif sc==5:
        txt(d,(360,190),"LET'S COUNT!",54,"#fff",True,stroke=3,outline="#40518b")
        txt(d,(360,260),"Count the bouncing stars!",27,"#34416f",True)
        n=min(5,max(1,int((t-54)//2.7)+1))
        for i in range(n):
            x=115+i*123; y=500+math.sin(t*5+i)*24
            star(d,x,y,48,["#ff83b7","#fff3a8","#ffffff","#b7a6ff","#ffad6b"][i])
            txt(d,(x,y+85),str(i+1),36,"#34416f",True)
        mascot(d,360,820,t,.85)
        rounded(d,(90,965,630,1065),"#fff")
        txt(d,(360,1015),"1, 2, 3, 4, 5!",42,"#f15f87",True)
    elif sc==6:
        txt(d,(360,185),"BRUSH, BRUSH, BRUSH!",39,"#fff",True,stroke=3,outline="#40518b")
        txt(d,(360,245),"Keep your smile sparkly!",26,"#34416f",True)
        # friendly tooth and oversized toothbrush illustration
        d.ellipse((220,370,500,700),fill="#fff",outline="#7f8bc0",width=5)
        for x in [270,340,410]:
            d.ellipse((x-30,580,x+30,720),fill="#fff",outline="#7f8bc0",width=3)
        d.ellipse((280,470,310,510),fill="#34416f"); d.ellipse((405,470,435,510),fill="#34416f")
        d.arc((300,505,420,590),0,180,fill="#f15f87",width=7)
        # toothbrush handle and bristles
        d.rounded_rectangle((470,520,530,850),radius=25,fill="#ff83b7",outline="#b74d85",width=4)
        d.rounded_rectangle((455,430,545,555),radius=18,fill="#71dff5",outline="#3b8eae",width=4)
        for x in range(465,540,18): d.line((x,440,x,480),fill="#fff",width=5)
        steps=["1. Use a pea-sized fluoride toothpaste","2. Brush gently in small circles","3. Brush every side for two minutes","4. Spit it out; don't swallow"]
        for i,line in enumerate(steps):
            rounded(d,(55,760+i*78,665,820+i*78),"#fff")
            txt(d,(360,790+i*78),line,21,"#34416f",True)
        mascot(d,360,1130,t,.42)
    else:
        txt(d,(360,200),"YOU DID IT!",56,"#fff",True,stroke=4,outline="#40518b")
        txt(d,(360,270),"LEARNING SUPERSTAR!",35,"#fff",True,stroke=3,outline="#f15f98")
        mascot(d,360,650,t,1.05)
        rounded(d,(55,930,665,1040),"#fff")
        txt(d,(360,985),"Animals • ABCs • Counting • Healthy teeth",22,"#34416f",True)
        txt(d,(360,1100),"See you next time, little explorers!",24,"#fff",True,stroke=2,outline="#40518b")
    return im

# Render frames; low enough FPS for a practical GitHub-hosted render.
for i in range(DURATION*FPS):
    frame(i/FPS).save(f"{FRAMES}/f{i:04d}.jpg",quality=90)

sr=22050
import numpy as np, wave
samples=np.zeros(int(sr*DURATION),dtype=np.float32)
notes=[523.25,659.25,783.99,659.25,587.33,698.46,880.0,698.46]
for i in range(int(DURATION/.28)):
    start=int(i*.28*sr); f=notes[i%len(notes)]; length=min(int(.22*sr),len(samples)-start)
    tt=np.arange(length)/sr
    samples[start:start+length]+=(.11*np.sin(2*np.pi*f*tt)*np.exp(-tt*7)).astype(np.float32)
    samples[start:start+length]+=(.02*np.sin(2*np.pi*(f/2)*tt)*np.exp(-tt*5)).astype(np.float32)
samples=np.clip(samples,-.7,.7); st=np.column_stack([samples,samples])
with wave.open("/tmp/lbl-music.wav","wb") as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes((st*32767).astype(np.int16).tobytes())
music=AudioSegment.from_wav("/tmp/lbl-music.wav")-21
voice=AudioSegment.silent(duration=DURATION*1000,frame_rate=sr).set_channels(2)
def voice_at(start,text):
    global voice
    p=f"/tmp/lbl-voice-{int(start*10)}.mp3"
    subprocess.run(["edge-tts","--voice","en-US-AnaNeural","--rate","+8%","--pitch","+4Hz","--text",text,"--write-media",p],check=True)
    clip=AudioSegment.from_file(p).set_frame_rate(sr).set_channels(2)+2
    voice=voice.overlay(clip,position=int(start*1000))
voice_at(.3,"Welcome to The Little Bright Lab! I'm Pip! Today we'll discover animal sounds, explore our ABCs, count to five, and learn to brush our teeth. Let's go!")
for i,a in enumerate(ANIMALS):
    start=5+i*8
    voice_at(start+.2,a["voice"])
    voice_at(start+4.0,a["reveal"])
voice_at(37.3,"A, B, C, D, E, F! A is for apple, B is for ball, C is for cow! Let's sing the letters together!")
voice_at(45.0,"A, B, C, D, E, F! Great singing!")
voice_at(54.2,"Let's count together! One, two, three, four, five! Count the stars with me!")
voice_at(61.5,"One, two, three, four, five! Hooray!")
voice_at(69.2,"Time to brush our teeth! Use a pea-sized amount of fluoride toothpaste. Brush gently in little circles on the outside, inside, and chewing surfaces. Brush for two minutes, twice every day, with help from a grown-up. Spit out the toothpaste. Don't swallow it!")
voice_at(83.0,"Fantastic brushing! You're a learning superstar! See you next time, little explorers!")
mix=music.overlay(voice)
for kind,start in [("cow",9.0),("duck",17.0),("dog",25.0),("lion",33.0)]:
    p=f"assets/sounds/{kind}.mp3"
    if os.path.exists(p):
        clip=AudioSegment.from_file(p).set_frame_rate(sr).set_channels(2)[:2400].fade_in(80).fade_out(180)-4
        mix=mix.overlay(clip,position=int(start*1000))
mix=mix.fade_in(350).fade_out(800)
mix.export("/tmp/lbl-final-audio.wav",format="wav")
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-framerate",str(FPS),"-i",f"{FRAMES}/f%04d.jpg","-i","/tmp/lbl-final-audio.wav","-t",str(DURATION),"-vf","scale=720:1280,format=yuv420p","-c:v","libx264","-preset","veryfast","-crf","22","-c:a","aac","-b:a","160k","-movflags","+faststart",OUT],check=True)
print("Created",OUT)
