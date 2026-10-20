import bpy, math, os
from mathutils import Vector

# Genuine Blender 3D proof-of-concept for The Little Bright Lab.
# This is intentionally a first blockout; later iterations should replace
# primitive-built models with approved sculpted/rigger characters.
ROOT = os.environ.get("LITTLE_BRIGHT_LAB_OUTPUT", os.path.abspath("output"))
FRAMES = os.path.join(ROOT, "blender_frames")
os.makedirs(FRAMES, exist_ok=True)
os.makedirs(ROOT, exist_ok=True)

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete(use_global=False)
for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
    pass

def mat(name, color, roughness=0.68):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    bs=m.node_tree.nodes.get("Principled BSDF"); bs.inputs["Base Color"].default_value=(*color,1)
    bs.inputs["Roughness"].default_value=roughness
    return m

PINK=mat("Mimi • petal pink",(0.95,0.34,0.56)); CREAM=mat("Moomo • warm cream",(0.94,0.86,0.68))
BROWN=mat("Moomo • cocoa patches",(0.28,0.12,0.07)); LAV=mat("Dott • lavender",(0.56,0.42,0.84))
GOLD=mat("Rumble • honey gold",(1.0,0.48,0.08)); MANE=mat("Rumble • soft mane",(0.72,0.23,0.035))
WHITE=mat("Eye whites",(1,0.98,0.9)); BLACK=mat("Pupils",(0.035,0.025,0.045))
GREEN=mat("Grass",(0.20,0.53,0.26)); LEAF=mat("Leaves",(0.12,0.39,0.20)); SKY=mat("Sky",(0.38,0.72,0.94))
YELLOW=mat("Flower centers",(1.0,0.72,0.12)); ORANGE=mat("Beak",(1.0,0.42,0.06))

def uv(name, loc, scale, material, seg=24, rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale; o.data.materials.append(material)
    bpy.ops.object.shade_smooth(); return o

def cone(name, loc, radius, depth, material, rot=(0,0,0)):
    bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=radius, radius2=0, depth=depth, location=loc, rotation=rot)
    o=bpy.context.object; o.name=name; o.data.materials.append(material); bpy.ops.object.shade_smooth(); return o

def character(name, x, kind, bodymat):
    parts=[]
    body=uv(name+" body",(x,0,1.1),(0.57,0.43,0.65),bodymat); parts.append(body)
    head=uv(name+" head",(x,0,2.0),(0.64,0.48,0.56),bodymat); parts.append(head)
    if kind=="bunny":
        for dx,ang in [(-0.25,-0.16),(0.25,0.16)]:
            ear=uv(name+" ear",(x+dx,-0.01,2.72),(0.17,0.15,0.48),bodymat); ear.rotation_euler[1]=ang; parts.append(ear)
            inner=uv(name+" inner ear",(x+dx,-0.145,2.73),(0.075,0.025,0.32),mat(name+" ear blush",(0.98,0.56,0.68))); inner.rotation_euler[1]=ang; parts.append(inner)
        tail=uv(name+" tail",(x+0.55,0.18,0.75),(0.19,0.18,0.19),WHITE); parts.append(tail)
    elif kind=="cow":
        for dx,dz in [(-0.31,0.16),(0.3,-0.06)]:
            patch=uv(name+" patch",(x+dx,-0.41,1.15+dz),(0.19,0.035,0.26),BROWN); parts.append(patch)
        muzzle=uv(name+" muzzle",(x,-0.46,1.83),(0.28,0.13,0.20),mat(name+" muzzle pink",(0.94,0.55,0.58))); parts.append(muzzle)
        for dx in [-0.32,0.32]:
            horn=cone(name+" horn",(x+dx,0,2.53),0.12,0.28,YELLOW); parts.append(horn)
    elif kind=="owl":
        for dx in [-0.35,0.35]:
            tuft=cone(name+" feather tuft",(x+dx,0,2.48),0.19,0.35,LAV); parts.append(tuft)
            wing=uv(name+" wing",(x+dx*1.35,-0.02,1.35),(0.25,0.22,0.40),LAV); parts.append(wing)
        beak=cone(name+" beak",(x,-0.51,1.92),0.13,0.25,ORANGE,(math.pi/2,0,0)); parts.append(beak)
    elif kind=="lion":
        mane=uv(name+" mane",(x,0.04,2.0),(0.78,0.61,0.72),MANE); parts.append(mane)
        face=uv(name+" face",(x,-0.48,2.02),(0.48,0.18,0.43),GOLD); parts.append(face)
        for a in range(10):
            ang=2*math.pi*a/10
            tuft=uv(name+" mane tuft",(x+0.67*math.sin(ang),0.02,2+0.62*math.cos(ang)),(0.20,0.23,0.22),MANE); parts.append(tuft)
        # Keep face visible in front of mane
        parts.append(face)
    # Common eyes, positioned toward camera (camera looks from y=-)
    for dx in [-0.22,0.22]:
        eye=uv(name+" eye",(x+dx,-0.44,2.12),(0.14,0.09,0.17),WHITE); parts.append(eye)
        pupil=uv(name+" pupil",(x+dx+0.015,-0.525,2.11),(0.065,0.035,0.09),BLACK); parts.append(pupil)
        glint=uv(name+" eye sparkle",(x+dx-0.018,-0.56,2.15),(0.024,0.015,0.03),WHITE); parts.append(glint)
    smile=uv(name+" smile",(x,-0.535,1.88),(0.12,0.025,0.035),BROWN); parts.append(smile)
    for dx in [-0.28,0.28]:
        leg=uv(name+" foot",(x+dx,-0.02,0.52),(0.18,0.25,0.15),bodymat); parts.append(leg)
    return parts, head

# Floor and world
bpy.ops.mesh.primitive_plane_add(size=200, location=(0,0,0))
floor=bpy.context.object; floor.name="Meadow"; floor.data.materials.append(GREEN)
world=bpy.context.scene.world or bpy.data.worlds.new("Little Bright Lab sky")
bpy.context.scene.world=world; world.color=(0.32,0.48,0.7)
world.use_nodes=True; world.node_tree.nodes["Background"].inputs[0].default_value=(0.24,0.48,0.68,1)
world.node_tree.nodes["Background"].inputs[1].default_value=0.6

# Decorative distant trees
for x,z,s in [(-5,1.8,1.3),(-4,2.2,1.5),(4.4,2,1.4),(5.3,1.6,1.1)]:
    uv("Storybook tree canopy",(x,1.7,z),(s,s*0.6,s),LEAF)
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.17, depth=1.8, location=(x,1.8,z-1.15))
    bpy.context.object.data.materials.append(BROWN)

# Four original cast members for a character lineup; Moomo will animate from behind leaves.
mimi, mimi_head=character("Mimi", -2.2, "bunny", PINK)
moomo, moomo_head=character("Moomo", 2.1, "cow", CREAM)
dott, dott_head=character("Dott", -0.4, "owl", LAV)
rumble, rumble_head=character("Rumble", 0.7, "lion", GOLD)

# Bushes at right foreground conceal Moomo initially.
bushes=[]
for x,z,s in [(1.45,0.65,0.72),(2.0,0.75,0.86),(2.55,0.62,0.72)]:
    bushes.append(uv("Reveal bush",(x,-0.55,z),(s,0.42,s*0.8),LEAF))

# Hide Dott and Rumble from animation framing; still present in character sheet render.
for obj in dott+dott_head.children if False else []: pass
for o in dott+rumble:
    o.hide_render=True

# Character lineup camera for sheet.
def camera(name, loc, target, ortho):
    bpy.ops.object.camera_add(location=loc)
    c=bpy.context.object; c.name=name; c.data.type="ORTHO"; c.data.ortho_scale=ortho
    c.rotation_euler=(Vector(target)-c.location).to_track_quat("-Z","Y").to_euler()
    return c
scene=bpy.context.scene
scene.render.engine="CYCLES" if False else "BLENDER_EEVEE_NEXT"
scene.render.resolution_x=1280; scene.render.resolution_y=720; scene.render.resolution_percentage=100
scene.render.image_settings.file_format="PNG"
bpy.ops.object.light_add(type="AREA", location=(-4,-6,8)); key=bpy.context.object; key.data.energy=1250; key.data.shape="DISK"; key.data.size=7
bpy.ops.object.light_add(type="AREA", location=(4,1,6)); fill=bpy.context.object; fill.data.energy=900; fill.data.size=5
sheetcam=camera("Character sheet camera",(0,-12,4.0),(0,0,1.55),10.2)
scene.camera=sheetcam
# For sheet show all four; reveal bushes are hidden in sheet and characters placed in row.
for o in dott+rumble: o.hide_render=False
for o in bushes: o.hide_render=True
for o in mimi+moomo+dott+rumble: o.hide_render=False
# Reposition lineup to show each cast member separated.
for group, xnew in [(mimi,-3.1),(moomo,-1.05),(dott,1.05),(rumble,3.1)]:
    # group parts are object references; move their x positions relative to prior root.
    xs=[o.location.x for o in group]
    if xs:
        delta=xnew - xs[0]
        for o in group: o.location.x += delta
# Camera frame
scene.render.filepath=os.path.join(ROOT,"little-bright-lab-character-sheet.png")
bpy.ops.render.render(write_still=True)

# Return Mimi and Moomo to story positions; hide owl and lion, restore reveal bushes.
for group, xnew in [(mimi,-2.2),(moomo,2.1)]:
    xs=[o.location.x for o in group]
    if xs:
        delta=xnew-xs[0]
        for o in group: o.location.x += delta
for o in dott+rumble: o.hide_render=True
for o in bushes: o.hide_render=False
# Moomo starts partly hidden behind the bushes then steps left into view.
for o in moomo:
    base=o.location.copy()
    o.location.x += 1.0
    o.keyframe_insert(data_path="location", frame=1)
    o.location.x = base.x + 1.0
    o.keyframe_insert(data_path="location", frame=72)
    o.location.x = base.x
    o.keyframe_insert(data_path="location", frame=144)
# Mimi leans/listens with a gentle body bounce and head tilt.
for o in mimi:
    base=o.location.copy()
    o.keyframe_insert(data_path="location", frame=1)
    o.location.z = base.z + 0.10
    o.keyframe_insert(data_path="location", frame=45)
    o.location.z = base.z
    o.keyframe_insert(data_path="location", frame=80)
    o.location.z = base.z + 0.06
    o.keyframe_insert(data_path="location", frame=115)
    o.location.z = base.z
    o.keyframe_insert(data_path="location", frame=144)
# Animate camera gentle push-in.
storycam=camera("Safari story camera",(0,-12,4.2),(0,0,1.45),9.3)
scene.camera=storycam
for frame, scale in [(1,9.3),(144,8.5)]:
    storycam.data.ortho_scale=scale; storycam.data.keyframe_insert(data_path="ortho_scale",frame=frame)
scene.frame_start=1; scene.frame_end=144; scene.render.fps=18
scene.render.resolution_x=1280; scene.render.resolution_y=720
scene.render.image_settings.file_format="PNG"
scene.render.filepath=os.path.join(FRAMES,"frame_")
scene.render.resolution_percentage=100
# Slightly softened interpolation
for obj in bpy.data.objects:
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kp in fc.keyframe_points: kp.interpolation="BEZIER"
for frame in range(scene.frame_start, scene.frame_end+1):
    scene.frame_set(frame)
    scene.render.filepath=os.path.join(FRAMES, f"frame_{frame:04d}.png")
    bpy.ops.render.render(write_still=True)
print("Rendered character sheet and 8-second 3D motion-test frames.")
