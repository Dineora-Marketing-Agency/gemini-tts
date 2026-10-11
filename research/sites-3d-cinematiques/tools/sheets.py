"""Contact sheet: 8 evenly spaced frames, 4x2 grid, timestamp labels.
Usage: python3 -I sheets.py <outdir> <video> [...]"""
import sys, os, subprocess, json, tempfile
from PIL import Image, ImageDraw

out = sys.argv[1]
for p in sys.argv[2:]:
    j = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'json', p],
                                  capture_output=True, text=True).stdout)
    dur = float(j['format']['duration'])
    ts = [min(dur - 0.3, dur * k / 7) for k in range(8)]
    tiles = []
    with tempfile.TemporaryDirectory(dir=os.path.join(out, '..', 'tmp')) as td:
        for i, t in enumerate(ts):
            f = os.path.join(td, f'{i}.png')
            for back in (0, 0.5, 1.0):
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{max(0, t - back):.3f}', '-i', p, '-frames:v', '1',
                                '-vf', 'scale=420:-2', f])
                if os.path.exists(f):
                    break
            tiles.append((t, Image.open(f).convert('RGB')))
    tw, th = tiles[0][1].size
    sheet = Image.new('RGB', (tw * 4 + 5 * 6, th * 2 + 3 * 6 + 28), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    d.text((8, 6), os.path.basename(p) + f'  ({dur:.2f}s)', fill=(255, 255, 0))
    for i, (t, im) in enumerate(tiles):
        x = 6 + (i % 4) * (tw + 6); y = 28 + (i // 4) * (th + 6)
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + 52, y + 14], fill=(0, 0, 0))
        d.text((x + 3, y + 2), f'{t:5.2f}s', fill=(255, 255, 255))
    name = os.path.splitext(os.path.basename(p))[0]
    sheet.save(os.path.join(out, name + '.jpg'), quality=82)
    print(name)
