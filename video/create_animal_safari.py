#!/usr/bin/env python3
"""Render a 60-second Little Bright Lab animated-series sampler (no Pip/dragon)."""
from PIL import Image, ImageDraw, ImageFont
from pydub import AudioSegment
import math, os, random, subprocess, wave
import numpy as np

W,H,FPS,DURATION=720,1280,12,60
OUT="output/little-bright-lab-cartoon-world.mp4"
FRAMES="/tmp/lbl-world-frames"
os.makedirs(FRAMES,exist_ok=True); os.makedirs("output",exist_ok=True)
random.seed(23)
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(n): return ImageFont.truetype(FONT,n)
def text(d,xy,s,n,fill="#ffffff",stroke=3):
    d.text(xy,s,font=font(n),fill=fill,anchor="mm",stroke_width=stroke,stroke_fill="#26345e")
def rounded(d,box,fill,outline=None,r=28,w=3):
    d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=w)
def animal(d,kind,x,y,t,scale=1):
    bob=math.sin(t*4+x*.01)*8
    x=int(x); y=int(y+bob); s=scale
    # Soft ground shadow
    d.ellipse((x-90*s,y+95*s,x+90*s,y+120*s),fill="#d3e9c9")
    if kind=="Mimi":
        fur="#ffb4c9"; ear="#ff8eae"
        d.ellipse((x-65*s,y-95*s,x-20*s,y+10*s),fill=fur,outline="#8f5277",width=3)
        d.ellipse((x+20*s,y-95*s,x+65*s,y+10*s),fill=fur,outline="#8f5277",width=3)
        d.ellipse((x-54*s,y-85*s,x-29*s,y-5*s),fill=ear); d.ellipse((x+29*s,y-85*s,x+54*s,y-5*s),fill=ear)
        d.ellipse((x-68*s,y-35*s,x+68*s,y+100*s),fill=fur,outline="#8f5277",width=3)
        d.ellipse((x-43*s,y+0*s,x-18*s,y+29*s),fill="white"); d.ellipse((x+18*s,y,x+43*s,y+29*s),fill="white")
        d.ellipse((x-34*s,y+8*s,x-22*s,y+25*s),fill="#26345e"); d.ellipse((x+22*s,y+8*s,x+34*s,y+25*s),fill="#26345e")
        d.ellipse((x-9*s,y+34*s,x+9*s,y+48*s),fill="#d56c91")
        d.arc((x-20*s,y+35*s,x+20*s,y+65*s),0,180,fill="#8f5277",width=3)
    elif kind=="Moomo":
        d.ellipse((x-72*s,y-30*s,x+72*s,y+100*s),fill="#fff8e8",outline="#776f62",width=3)
        d.ellipse((x-62*s,y-90*s,x+62*s,y+35*s),fill="#fff8e8",outline="#776f62",width=3)
        d.ellipse((x-58*s,y-95*s,x-25*s,y-60*s),fill="#ffb5c2"); d.ellipse((x+25*s,y-95*s,x+58*s,y-60*s),fill="#ffb5c2")
        d.ellipse((x-46*s,y-65*s,x-20*s,y-32*s),fill="white"); d.ellipse((x+20*s,y-65*s,x+46*s,y-32*s),fill="white")
        d.ellipse((x-37*s,y-58*s,x-25*s,y-36*s),fill="#26345e"); d.ellipse((x+25*s,y-58*s,x+37*s,y-36*s),fill="#26345e")
        d.ellipse((x-18*s,y-20*s,x+18*s,y+5*s),fill="#ef9eae")
        d.ellipse((x-50*s,y+15*s,x-20*s,y+48*s),fill="#987b68"); d.ellipse((x+20*s,y+35*s,x+52*s,y+65*s),fill="#987b68")
    elif kind=="Dott":
        d.ellipse((x-70*s,y-65*s,x+70*s,y+90*s),fill="#a88be8",outline="#594b91",width=3)
        d.ellipse((x-68*s,y-95*s,x-8*s,y-25*s),fill="#c9b8ff",outline="#594b91",width=3)
        d.ellipse((x+8*s,y-95*s,x+68*s,y-25*s),fill="#c9b8ff",outline="#594b91",width=3)
        d.ellipse((x-47*s,y-35*s,x-5*s,y+10*s),fill="white"); d.ellipse((x+5*s,y-35*s,x+47*s,y+10*s),fill="white")
        d.ellipse((x-32*s,y-22*s,x-16*s,y+1*s),fill="#26345e"); d.ellipse((x+16*s,y-22*s,x+32*s,y+1*s),fill="#26345e")
        d.polygon([(x-12*s,y+8*s),(x+12*s,y+8*s),(x,y+28*s)],fill="#ffbd4a")
        d.arc((x-18*s,y+25*s,x+18*s,y+48*s),0,180,fill="#594b91",width=3)
        d.ellipse((x-65*s,y+0*s,x-25*s,y+52*s),fill="#a88be8"); d.ellipse((x+25*s,y+0*s,x+65*s,y+52*s),fill="#a88be8")
    else: # Rumble, friendly lion cub
        d.ellipse((x-80*s,y-85*s,x+80*s,y+80*s),fill="#f5a43b",outline="#a95b2a",width=3)
        d.ellipse((x-60*s,y-55*s,x+60*s,y+100*s),fill="#ffd37a",outline="#a95b2a",width=3)
        d.ellipse((x-45*s,y-28*s,x-12*s,y+8*s),fill="white"); d.ellipse((x+12*s,y-28*s,x+45*s,y+8*s),fill="white")
        d.ellipse((x-34*s,y-18*s,x-18*s,y+5*s),fill="#26345e"); d.ellipse((x+18*s,y-18*s,x+34*s,y+5*s),fill="#26345e")
        d.polygon([(x-12*s,y+16*s),(x+12*s,y+16*s),(x,y+30*s)],fill="#8e4d45")
        d.arc((x-24*s,y+25*s,x+24*s,y+55*s),0,180,fill="#8e4d45",width=3)
    # Blinking stars / movement accents
    for dx,dy in [(-90,-100),(92,-70)]:
        if math.sin(t*5+dx)>0:
            d.text((x+dx*s,y+dy*s),"✦",font=font(max(18,int(28*s))),fill="#fff16c",anchor="mm")
def scene(t):
    if t<12: return 0
    if t<24: return 1
    if t<36: return 2
    if t<48: return 3
    return 4
def frame(t):
    idx=scene(t)
    palettes=[("#9be7ff","#c8f4ff"),("#b8f2c8","#e9ffd9"),("#ffd9a1","#fff0cc"),("#b9c7ff","#e5eaff"),("#ffc6dc","#ffe9f0")]
    top,bottom=palettes[idx]
    im=Image.new("RGB",(W,H),top); d=ImageDraw.Draw(im)
    for yy in range(H):
        if yy%4==0:
            r=int((1-yy/H)*int(top[1:3],16)+(yy/H)*int(bottom[1:3],16))
            g=int((1-yy/H)*int(top[3:5],16)+(yy/H)*int(bottom[3:5],16))
            b=int((1-yy/H)*int(top[5:7],16)+(yy/H)*int(bottom[5:7],16))
            d.line((0,yy,W,yy),fill=(r,g,b))
    # drifting clouds and a playful rolling landscape
    for j in range(4):
        cx=int((j*230+t*18)%900)-90; cy=140+j%2*90
        d.ellipse((cx,cy,cx+110,cy+55),fill="#ffffff")
        d.ellipse((cx+25,cy-25,cx+80,cy+45),fill="#ffffff")
    d.ellipse((-150,850,430,1370),fill="#83dba2")
    d.ellipse((280,820,950,1390),fill="#69cc91")
    if idx==0:
        title="WELCOME TO"; subtitle="THE LITTLE BRIGHT LAB"
        who="Mimi"
    elif idx==1:
        title="ANIMAL SOUNDS SAFARI"; subtitle="Listen, guess, then say it!"
        who="Moomo"
    elif idx==2:
        title="LITTLE NUMBER ADVENTURES"; subtitle="Can you count 1, 2, 3?"
        who="Mimi"
    elif idx==3:
        title="ALPHABET & WORD EXPLORERS"; subtitle="A is for Animal!"
        who="Dott"
    else:
        title="BRIGHT SMILES + GROWING UP GREAT"; subtitle="Healthy habits. Kind hearts."
        who="Rumble"
    # Intro/outro show the whole ensemble; middle scenes spotlight the episode friend.
    if idx in (0,4):
        animal(d,"Mimi",150,700,t,.75); animal(d,"Moomo",310,710,t,.75)
        animal(d,"Dott",470,700,t,.75); animal(d,"Rumble",610,710,t,.68)
    else:
        animal(d,who,360,710,t,1.35)
    # Scene-specific floating learning props
    if idx==1:
        animal(d,"Moomo",360,735,t,1.2)
        text(d,(360,930),"MOO!  QUACK!  WOOF!",38,"#ffffff")
    elif idx==2:
        for i in range(3):
            xx=250+i*110; yy=490+math.sin(t*4+i)*12
            d.ellipse((xx-35,yy-35,xx+35,yy+35),fill="#ffdf55",outline="#e9a52c",width=3)
            text(d,(xx,yy),str(i+1),36,"#26345e",1)
    elif idx==3:
        rounded(d,(240,470,480,610),"#ffffff","#8773c8",24,5); text(d,(360,540),"A a",82,"#7457bd",1)
    elif idx==4:
        text(d,(360,500),"BRUSH • SHARE • CARE",30,"#ffffff")
    rounded(d,(28,55,692,205),"#5b66ad", "#ffffff", 32,4)
    text(d,(360,100),title,27)
    text(d,(360,158),subtitle,23,"#fff16c",2)
    text(d,(360,1150),"LEARN • PLAY • SHINE!",26,"#ffffff")
    return im

# Build a frame-by-frame animated MP4.
for i in range(FPS*DURATION):
    frame(i/FPS).save(f"{FRAMES}/{i:05d}.png")
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",f"{FRAMES}/%05d.png","-c:v","libx264","-pix_fmt","yuv420p","-r",str(FPS),"/tmp/lbl-world-video.mp4"],check=True)
# Generate a light original instrumental bed.
sr=22050; total=int(sr*DURATION); audio=np.zeros(total,dtype=np.float32)
notes=[523.25,659.25,783.99,659.25,587.33,698.46,880,698.46]
for j,start in enumerate(np.arange(0,DURATION,.32)):
    a=int(start*sr); n=min(int(.27*sr),total-a); tt=np.arange(n)/sr
    f=notes[j%len(notes)]
    audio[a:a+n]+=0.07*np.sin(2*np.pi*f*tt)*np.sin(np.pi*np.arange(n)/n)
audio=np.clip(audio,-.95,.95)
with wave.open("/tmp/lbl-world-music.wav","wb") as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
    wf.writeframes((audio*32767).astype(np.int16).tobytes())
# Clear narration, one speaker at a time, with no overlapping voices.
lines=[
 (1.0,"Welcome to The Little Bright Lab, where learning is an adventure!"),
 (13.0,"Meet our animal friends. Listen carefully. What sound does a cow make? Moo!"),
 (25.0,"Let's count together. One, two, three! Great counting!"),
 (37.0,"A is for animal. A, A, animal! Let's explore new words together."),
 (49.0,"Remember to brush your teeth, be kind, and help your friends. You are bright!"),
]
voice=AudioSegment.silent(duration=DURATION*1000)
for i,(start,line) in enumerate(lines):
    mp3=f"/tmp/lbl-voice-{i}.mp3"
    subprocess.run(["edge-tts","--voice","en-US-AriaNeural","--rate","+4%","--text",line,"--write-media",mp3],check=True)
    clip=AudioSegment.from_file(mp3).apply_gain(-2)
    voice=voice.overlay(clip,position=int(start*1000))
music=AudioSegment.from_wav("/tmp/lbl-world-music.wav").apply_gain(-18)
mix=music.overlay(voice)
mix.export("/tmp/lbl-world-mix.mp3",format="mp3",bitrate="128k")
subprocess.run(["ffmpeg","-y","-loglevel","error","-i","/tmp/lbl-world-video.mp4","-i","/tmp/lbl-world-mix.mp3","-c:v","copy","-c:a","aac","-shortest",OUT],check=True)
print(f"Created {OUT}")
