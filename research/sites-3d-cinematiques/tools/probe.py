import sys, os, json, subprocess, csv

vdir, out = sys.argv[1], sys.argv[2]
rows = []
for name in sorted(os.listdir(vdir)):
    p = os.path.join(vdir, name)
    if not os.path.isfile(p):
        continue
    with open(p, 'rb') as fh:
        head = fh.read(64)
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', p],
                       capture_output=True, text=True)
    row = {'file': name, 'size_mb': round(os.path.getsize(p) / 1e6, 2)}
    if r.returncode != 0 or not r.stdout.strip():
        row['status'] = 'unreadable:' + head[:16].decode('latin1').replace('\n', ' ')
        rows.append(row)
        continue
    j = json.loads(r.stdout)
    v = next((s for s in j.get('streams', []) if s.get('codec_type') == 'video'), None)
    a = next((s for s in j.get('streams', []) if s.get('codec_type') == 'audio'), None)
    if v is None:
        row['status'] = 'no-video'
        rows.append(row)
        continue
    n, d = (v.get('avg_frame_rate') or '0/1').split('/')
    fps = int(n) / int(d) if int(d) else 0
    dur = float(j['format'].get('duration', v.get('duration', 0)) or 0)
    row.update(status='ok', w=v['width'], h=v['height'], fps=round(fps, 3), dur=round(dur, 2),
               frames=v.get('nb_frames'), codec=v['codec_name'], pix=v.get('pix_fmt'),
               kbps=round(int(j['format'].get('bit_rate', 0)) / 1000), audio=a['codec_name'] if a else 'none',
               ar=round(v['width'] / v['height'], 3))
    rows.append(row)

keys = ['file', 'status', 'w', 'h', 'ar', 'fps', 'dur', 'frames', 'codec', 'pix', 'kbps', 'audio', 'size_mb']
with open(out, 'w', newline='') as fh:
    wr = csv.DictWriter(fh, keys)
    wr.writeheader()
    for r in rows:
        wr.writerow({k: r.get(k, '') for k in keys})
for r in rows:
    print(' | '.join(str(r.get(k, '')) for k in keys))
