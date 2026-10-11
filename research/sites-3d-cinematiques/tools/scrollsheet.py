"""Turn a scroll recording into (1) a trimmed constant-fps mp4 and (2) a contact sheet
indexed by scroll progress. Usage: python3 -I scrollsheet.py <rec.webm> <meta.json> <outprefix> [n=20] [cols=5]"""
import sys, json, subprocess, os, tempfile
from PIL import Image, ImageDraw

webm, meta, outp = sys.argv[1:4]
n = int(sys.argv[4]) if len(sys.argv) > 4 else 20
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 5
m = json.load(open(meta))
t0, t1 = m['scrollStartS'], m['scrollEndS'] + 4.0  # include the smoothing tail
mp4 = outp + '.mp4'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', webm, '-ss', f'{t0:.2f}', '-to', f'{t1:.2f}', '-r', '25',
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', mp4], check=True)
dur = t1 - t0
tiles = []
with tempfile.TemporaryDirectory(dir=os.path.dirname(os.path.abspath(outp))) as td:
    for i in range(n):
        frac = i / (n - 1)
        t = min(dur - 0.2, frac * (m['scrollEndS'] - m['scrollStartS']) + (2.5 if i == n - 1 else 0))
        f = os.path.join(td, f'{i}.png')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.2f}', '-i', mp4, '-frames:v', '1', '-vf', 'scale=384:-2', f], check=True)
        tiles.append((frac, Image.open(f).convert('RGB')))
tw, th = tiles[0][1].size
rows = (n + cols - 1) // cols
sheet = Image.new('RGB', (cols * (tw + 6) + 6, rows * (th + 6) + 34), (40, 40, 40))
d = ImageDraw.Draw(sheet)
d.text((8, 8), f"{os.path.basename(outp)} - {m['viewports']} viewports of scroll - tiles at scroll progress", fill=(255, 255, 0))
for i, (frac, im) in enumerate(tiles):
    x = 6 + (i % cols) * (tw + 6); y = 34 + (i // cols) * (th + 6)
    sheet.paste(im, (x, y))
    d.rectangle([x, y, x + 96, y + 14], fill=(0, 0, 0))
    d.text((x + 3, y + 2), f"{frac * 100:5.1f}%  {frac * m['viewports']:.1f}vh", fill=(255, 255, 255))
sheet.save(outp + '_sheet.jpg', quality=85)
print(mp4, outp + '_sheet.jpg', f'{dur:.1f}s')
