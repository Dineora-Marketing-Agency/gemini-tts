"""Analyze a stepped scroll capture (one screenshot per fixed scroll increment).
Usage: python3 -I steps_analyze.py <name> (reads rec/<name>_steps/*.png and rec/<name>_steps.json)
Outputs per-step camera motion, view changes ("new shots") per viewport of scroll, palette, fill; writes
rec/<name>_scroll.json and rec/<name>_scroll_sheet.jpg."""
import sys, os, json, glob
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze import luma, global_motion, kmeans, rgb2hsv, hue_name  # noqa: E402

name = sys.argv[1]
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rec')
meta = json.load(open(os.path.join(base, name + '_steps.json')))
files = sorted(glob.glob(os.path.join(base, name + '_steps', '*.png')))
ims = [Image.open(f).convert('RGB') for f in files]
W = 256
H = int(round(W * ims[0].height / ims[0].width / 2)) * 2
F = np.stack([np.asarray(im.resize((W, H), Image.BOX), np.float32) / 255 for im in ims])
Y = luma(F)
vh_step = meta['viewports'] / (len(F) - 1)  # viewports of scroll per step

q = (F * 7.999).astype(np.int32)
ch = np.stack([np.bincount((c[..., 0] * 64 + c[..., 1] * 8 + c[..., 2]).ravel(), minlength=512) / (H * W) for c in q])
steps = []
for i in range(1, len(F)):
    hd = 0.5 * np.abs(ch[i] - ch[i - 1]).sum()
    d = float(np.abs(Y[i] - Y[i - 1]).mean())
    g = global_motion(Y[i - 1], Y[i])
    row = dict(i=i, vh=round(i * vh_step, 2), hist_change=round(float(hd), 3), luma_change=round(d, 4))
    if g:
        # per viewport of scroll
        k = 100 / vh_step
        row.update(pan=round(g['tx'] * k, 1), tilt=round(g['ty'] * k, 1), zoom=round(g['zoom'] * k, 1),
                   roll=round(float(np.degrees(g['rot'])) / vh_step, 1), resid=round(g['resid'] * k, 1), n=g['n'])
    steps.append(row)

# a "shot change" = the framing no longer matches the previous step (motion fit fails or big histogram jump)
shot_changes = [s['vh'] for s in steps if s['hist_change'] > 0.35 or ('n' not in s and s['luma_change'] > 0.02)]

pal_px = F.reshape(-1, 3)[np.random.default_rng(0).choice(F.shape[0] * H * W, 60000, replace=False)]
C, sh = kmeans(pal_px, 6)
hh, ss, vv = rgb2hsv(F)
m = (ss > 0.25) & (vv > 0.15)
hues = []
if m.sum() > 50:
    names = [hue_name(x) for x in hh[m][::max(1, m.sum() // 20000)]]
    u, c = np.unique(names, return_counts=True)
    hues = [(u[i], round(c[i] / c.sum() * 100)) for i in np.argsort(-c)[:4]]

gy, gx = np.gradient(Y, axis=(1, 2))
gm = np.sqrt(gx ** 2 + gy ** 2)
fill = float(((gm > 0.012) | (np.abs(Y - np.median(Y, axis=(1, 2), keepdims=True)) > 0.10)).mean())
out = dict(name=name, viewports=meta['viewports'], steps=len(F), vh_per_step=round(vh_step, 3),
           shot_changes_at_vh=shot_changes, shots=len(shot_changes) + 1,
           vh_per_shot=round(meta['viewports'] / (len(shot_changes) + 1), 2),
           palette=[('#%02x%02x%02x' % tuple((c * 255).round().astype(int)), round(float(s) * 100, 1)) for c, s in zip(C, sh)],
           hues=hues, luma_mean=round(float(Y.mean()), 3), pct_near_black=round(float((Y < 0.06).mean()) * 100, 1),
           pct_highlight=round(float((Y > 0.85).mean()) * 100, 1), fill_pct_pixels=round(fill * 100, 1),
           luma_per_step=[round(float(y.mean()), 3) for y in Y], per_step=steps)
json.dump(out, open(os.path.join(base, name + '_scroll.json'), 'w'), ensure_ascii=False, indent=0)

# contact sheet of every other step
pick = list(range(0, len(ims), max(1, len(ims) // 24)))
if pick[-1] != len(ims) - 1:
    pick.append(len(ims) - 1)
tw = 320; th = int(tw * ims[0].height / ims[0].width)
cols = 5; rows = (len(pick) + cols - 1) // cols
sheet = Image.new('RGB', (cols * (tw + 6) + 6, rows * (th + 6) + 30), (40, 40, 40))
dr = ImageDraw.Draw(sheet)
dr.text((8, 8), f"{name}: {meta['viewports']} viewports of scroll, tiles labelled with scroll depth (viewport heights)", fill=(255, 255, 0))
for k, i in enumerate(pick):
    x = 6 + (k % cols) * (tw + 6); y = 30 + (k // cols) * (th + 6)
    sheet.paste(ims[i].resize((tw, th)), (x, y))
    dr.rectangle([x, y, x + 70, y + 14], fill=(0, 0, 0))
    dr.text((x + 3, y + 2), f"{i * vh_step:4.2f} vh", fill=(255, 255, 255))
sheet.save(os.path.join(base, name + '_scroll_sheet.jpg'), quality=85)

print(json.dumps({k: out[k] for k in ['name', 'viewports', 'steps', 'vh_per_step', 'shots', 'shot_changes_at_vh', 'vh_per_shot', 'palette', 'hues', 'luma_mean', 'pct_near_black', 'pct_highlight', 'fill_pct_pixels']}, ensure_ascii=False))
print('vh   hist  luma   pan  tilt  zoom  roll resid n')
for s in steps:
    print(f"{s['vh']:5.2f} {s['hist_change']:.2f} {s['luma_change']:.3f} {s.get('pan', '-'):>5} {s.get('tilt', '-'):>5} {s.get('zoom', '-'):>5} {s.get('roll', '-'):>5} {s.get('resid', '-'):>5} {s.get('n', '-')}")
