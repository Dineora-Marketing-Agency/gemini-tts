"""Frame-level cinematic analysis of hero background videos.

Usage: python3 -I analyze.py <video> [<video> ...] > out.jsonl
Measures: cuts, camera motion (global similarity fit on patch phase-correlation),
activity, palette, luminance, composition / negative space, loop seam.
"""
import sys, json, subprocess
import numpy as np

W = 256


def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                        'stream=width,height,avg_frame_rate', '-show_entries', 'format=duration',
                        '-of', 'json', path], capture_output=True, text=True)
    j = json.loads(r.stdout)
    s = j['streams'][0]
    n, d = s['avg_frame_rate'].split('/')
    return s['width'], s['height'], int(n) / int(d), float(j['format']['duration'])


def decode(path, w, h):
    oh = int(round(W * h / w / 2)) * 2
    cmd = ['ffmpeg', '-v', 'error', '-i', path, '-vf', f'scale={W}:{oh}:flags=area',
           '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    raw = subprocess.run(cmd, capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8)
    n = fr.size // (W * oh * 3)
    return fr[:n * W * oh * 3].reshape(n, oh, W, 3).astype(np.float32) / 255.0


def luma(rgb):
    return rgb[..., 0] * 0.2126 + rgb[..., 1] * 0.7152 + rgb[..., 2] * 0.0722


def phase_shift(a, b, win):
    A = np.fft.fft2((a - a.mean()) * win)
    B = np.fft.fft2((b - b.mean()) * win)
    R = A * np.conj(B)
    R /= np.abs(R) + 1e-9
    c = np.fft.ifft2(R).real
    py, px = np.unravel_index(np.argmax(c), c.shape)
    peak = c[py, px]
    n = c.shape[0]

    def sub(cm, c0, cp):
        den = cm - 2 * c0 + cp
        return 0.0 if abs(den) < 1e-9 else 0.5 * (cm - cp) / den

    dy = py + sub(c[(py - 1) % n, px], peak, c[(py + 1) % n, px])
    dx = px + sub(c[py, (px - 1) % n], peak, c[py, (px + 1) % n])
    if dy > n / 2: dy -= n
    if dx > n / 2: dx -= n
    # shift that maps b -> a (content motion from frame b to frame a)
    return dx, dy, peak


def global_motion(Y0, Y1, P=48, S=24):
    h, w = Y0.shape
    win = np.outer(np.hanning(P), np.hanning(P))
    pts, vec, wts = [], [], []
    for y in range(0, h - P + 1, S):
        for x in range(0, w - P + 1, S):
            a, b = Y1[y:y + P, x:x + P], Y0[y:y + P, x:x + P]
            if b.std() < 0.012:
                continue
            dx, dy, pk = phase_shift(a, b, win)
            if pk < 0.12 or abs(dx) > P / 3 or abs(dy) > P / 3:
                continue
            pts.append(((x + P / 2 - w / 2) / w, (y + P / 2 - h / 2) / w))
            vec.append((dx / w, dy / w))
            wts.append(pk)
    if len(pts) < 6:
        return None
    pts, vec, wts = np.array(pts), np.array(vec), np.array(wts)
    # similarity model: u = tx + a x - b y ; v = ty + a y + b x
    X = np.zeros((2 * len(pts), 4)); Yv = np.zeros(2 * len(pts)); Wt = np.repeat(wts, 2)
    X[0::2] = np.c_[np.ones(len(pts)), np.zeros(len(pts)), pts[:, 0], -pts[:, 1]]
    X[1::2] = np.c_[np.zeros(len(pts)), np.ones(len(pts)), pts[:, 1], pts[:, 0]]
    Yv[0::2], Yv[1::2] = vec[:, 0], vec[:, 1]
    sw = np.sqrt(Wt)
    p, *_ = np.linalg.lstsq(X * sw[:, None], Yv * sw, rcond=None)
    res = (X @ p - Yv).reshape(-1, 2)
    resid = float(np.sqrt((res ** 2).sum(1)).mean())
    r = np.sqrt((pts ** 2).sum(1))
    core = r < 0.18
    core_mag = float(np.sqrt((vec[core] ** 2).sum(1)).mean()) if core.sum() >= 2 else np.nan
    edge_mag = float(np.sqrt((vec[~core] ** 2).sum(1)).mean()) if (~core).sum() >= 2 else np.nan
    return dict(tx=p[0], ty=p[1], zoom=p[2], rot=p[3], resid=resid, n=len(pts),
                core=core_mag, edge=edge_mag)


def kmeans(X, k=6, it=20, seed=0):
    rng = np.random.default_rng(seed)
    C = [X[rng.integers(len(X))]]
    for _ in range(1, k):
        d = np.min(((X[:, None, :] - np.array(C)[None]) ** 2).sum(-1), 1)
        C.append(X[rng.choice(len(X), p=d / d.sum())])
    C = np.array(C)
    for _ in range(it):
        lab = np.argmin(((X[:, None, :] - C[None]) ** 2).sum(-1), 1)
        for j in range(k):
            if (lab == j).any():
                C[j] = X[lab == j].mean(0)
    lab = np.argmin(((X[:, None, :] - C[None]) ** 2).sum(-1), 1)
    share = np.bincount(lab, minlength=k) / len(lab)
    o = np.argsort(-share)
    return C[o], share[o]


def rgb2hsv(rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx, mn = rgb.max(-1), rgb.min(-1)
    d = mx - mn + 1e-9
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    s = np.where(mx > 0, (mx - mn) / (mx + 1e-9), 0)
    return h, s, mx


HUES = [(15, 'rouge'), (40, 'orange'), (65, 'jaune/or'), (150, 'vert'), (195, 'cyan/teal'),
        (255, 'bleu'), (290, 'violet'), (335, 'magenta/rose'), (361, 'rouge')]


def hue_name(h):
    for lim, n in HUES:
        if h < lim:
            return n


def lap_var(Y):
    L = -4 * Y[1:-1, 1:-1] + Y[:-2, 1:-1] + Y[2:, 1:-1] + Y[1:-1, :-2] + Y[1:-1, 2:]
    return L


def analyze(path):
    w, h, fps, dur = probe(path)
    F = decode(path, w, h)
    T, H, Wd, _ = F.shape
    Y = luma(F)
    out = dict(file=path.split('/')[-1], w=w, h=h, fps=round(fps, 2), dur=round(dur, 2), frames=T)

    # --- cuts
    hist = np.stack([np.histogram(y, 32, (0, 1))[0] / y.size for y in Y])
    q = (F * 7.999).astype(np.int32)
    chist = np.stack([np.bincount((c[..., 0] * 64 + c[..., 1] * 8 + c[..., 2]).ravel(), minlength=512) / (H * Wd) for c in q])
    d = np.abs(np.diff(Y, axis=0)).mean((1, 2))
    hd = 0.5 * np.abs(np.diff(chist, axis=0)).sum(1)
    med = np.median(d) + 1e-4
    cut_idx = [i + 1 for i in range(len(d)) if hd[i] > 0.30 and d[i] > max(4 * med, 0.05)]
    # merge cuts closer than 3 frames (flash frames)
    cuts = []
    for c in cut_idx:
        if not cuts or c - cuts[-1] > 3:
            cuts.append(c)
    out['cuts_t'] = [round(c / fps, 2) for c in cuts]
    out['shots'] = len(cuts) + 1
    out['avg_shot_len_s'] = round(dur / (len(cuts) + 1), 2)
    out['cuts_per_s'] = round(len(cuts) / dur, 3)

    # --- activity (screen change per second, % of full scale)
    out['activity'] = round(float(np.median(d)) * fps * 100, 2)  # luma change %/s
    thirds = np.array_split(d, 3)
    out['activity_thirds'] = [round(float(np.median(t)) * fps * 100, 2) for t in thirds]
    sm = np.convolve(d, np.ones(5) / 5, 'same')
    out['activity_peak_at'] = round(float(np.argmax(sm)) / max(len(sm) - 1, 1), 2)

    # --- camera motion
    step = 8  # 1/3 s at 24 fps: validated on synthetic pan/tilt/zoom (±5%)
    gm = []
    cut_set = set(cuts)
    for t in range(0, T - step, step):
        if any(t < c <= t + step for c in cut_set):
            continue
        g = global_motion(Y[t], Y[t + step])
        if g: gm.append(g)
    if gm:
        k = fps / step  # per-second scale
        tx = np.array([g['tx'] for g in gm]) * k * 100   # % frame width per second
        ty = np.array([g['ty'] for g in gm]) * k * 100
        zm = np.array([g['zoom'] for g in gm]) * k * 100  # % scale per second
        rt = np.degrees(np.array([g['rot'] for g in gm]) * k)  # deg/s
        rs = np.array([g['resid'] for g in gm]) * k * 100
        core = np.nanmean([g['core'] for g in gm]) * k * 100
        edge = np.nanmean([g['edge'] for g in gm]) * k * 100
        span = len(gm) * step / fps
        out['cam'] = dict(
            pan_x=round(float(np.median(tx)), 2), tilt_y=round(float(np.median(ty)), 2),
            zoom=round(float(np.median(zm)), 2), roll=round(float(np.median(rt)), 2),
            total_x=round(float(tx.sum() * step / fps), 1), total_y=round(float(ty.sum() * step / fps), 1),
            total_zoom=round(float(zm.sum() * step / fps), 1),
            local_motion=round(float(np.median(rs)), 2), core=round(float(core), 2), edge=round(float(edge), 2),
            pan_consistency=round(float(abs(np.mean(np.sign(tx[np.abs(tx) > 0.3])))) if (np.abs(tx) > 0.3).any() else 0, 2),
            zoom_consistency=round(float(abs(np.mean(np.sign(zm[np.abs(zm) > 0.3])))) if (np.abs(zm) > 0.3).any() else 0, 2),
            samples=len(gm), span_s=round(span, 1))
        # thirds of the camera move to detect accel / decel (speed ramps)
        sp = np.sqrt(tx ** 2 + ty ** 2) + np.abs(zm)
        out['cam']['speed_thirds'] = [round(float(np.median(s)), 2) for s in np.array_split(sp, 3)]

    # --- palette & light
    idx = np.linspace(0, T - 1, min(16, T)).astype(int)
    px = F[idx].reshape(-1, 3)
    px = px[np.random.default_rng(1).choice(len(px), min(40000, len(px)), replace=False)]
    C, sh = kmeans(px, 6)
    out['palette'] = [('#%02x%02x%02x' % tuple((c * 255).round().astype(int)), round(float(s) * 100, 1)) for c, s in zip(C, sh)]
    Ys = Y[idx]
    out['luma_mean'] = round(float(Ys.mean()), 3)
    out['luma_median'] = round(float(np.median(Ys)), 3)
    out['pct_near_black'] = round(float((Ys < 0.06).mean()) * 100, 1)
    out['pct_dark'] = round(float((Ys < 0.18).mean()) * 100, 1)
    out['pct_highlight'] = round(float((Ys > 0.85).mean()) * 100, 1)
    out['contrast_p2_p98'] = [round(float(np.percentile(Ys, 2)), 3), round(float(np.percentile(Ys, 98)), 3)]
    hh, ss, vv = rgb2hsv(F[idx])
    out['saturation_mean'] = round(float((ss * vv).sum() / (vv.sum() + 1e-9)), 3)
    m = (ss > 0.25) & (vv > 0.15)
    out['pct_colorful'] = round(float(m.mean()) * 100, 1)
    if m.sum() > 50:
        names = [hue_name(x) for x in hh[m][::max(1, m.sum() // 20000)]]
        u, c = np.unique(names, return_counts=True)
        o = np.argsort(-c)
        out['hues'] = [(u[i], round(c[i] / c.sum() * 100)) for i in o[:4]]
        hm = hh[m]
        warm = ((hm < 70) | (hm > 320)).mean(); cool = ((hm > 160) & (hm < 300)).mean()
        out['warm_cool'] = [round(float(warm) * 100), round(float(cool) * 100)]
    # luminance arc over time
    lt = Y.mean((1, 2))
    out['luma_start_mid_end'] = [round(float(lt[:max(1, T // 10)].mean()), 3), round(float(lt[T // 2]), 3), round(float(lt[-max(1, T // 10):].mean()), 3)]
    out['fade_in_from_black'] = bool(lt[0] < 0.03 and lt[min(T - 1, int(fps))] > lt[0] + 0.03)

    # --- composition: occupancy grid & negative space
    gy, gx = np.gradient(Ys, axis=(1, 2))
    gm_ = np.sqrt(gx ** 2 + gy ** 2)
    cells_y, cells_x = 9, 16
    occ = np.zeros((cells_y, cells_x)); mass = np.zeros((cells_y, cells_x))
    for f in range(len(Ys)):
        bg = np.median(np.r_[Ys[f, 0], Ys[f, -1], Ys[f, :, 0], Ys[f, :, -1]])
        for i in range(cells_y):
            for j in range(cells_x):
                ys = slice(i * H // cells_y, (i + 1) * H // cells_y); xs = slice(j * Wd // cells_x, (j + 1) * Wd // cells_x)
                cell = Ys[f, ys, xs]; g = gm_[f, ys, xs]
                active = (g.mean() > 0.012) or (abs(cell.mean() - bg) > 0.10) or (cell.std() > 0.05)
                occ[i, j] += active
                mass[i, j] += g.mean() * (0.15 + cell.mean())
    occ /= len(Ys)
    out['fill_pct'] = round(float(occ.mean()) * 100, 1)
    mass /= mass.sum() + 1e-9
    yy, xx = np.mgrid[0:cells_y, 0:cells_x]
    out['visual_center'] = [round(float((mass * (xx + 0.5)).sum() / cells_x), 2), round(float((mass * (yy + 0.5)).sum() / cells_y), 2)]
    # 3x3 occupancy (rows top->bottom)
    g3 = [[round(float(occ[i * 3:(i + 1) * 3, j * 16 // 3:(j + 1) * 16 // 3].mean()) * 100) for j in range(3)] for i in range(3)]
    out['fill_3x3'] = g3
    # where the detail sits (mass 3x3)
    m3 = [[round(float(mass[i * 3:(i + 1) * 3, j * 16 // 3:(j + 1) * 16 // 3].sum()) * 100) for j in range(3)] for i in range(3)]
    out['mass_3x3'] = m3
    sym = np.mean([np.corrcoef(y.ravel(), y[:, ::-1].ravel())[0, 1] for y in Ys])
    out['h_symmetry'] = round(float(sym), 2)
    c = Ys[:, H // 4:3 * H // 4, Wd // 4:3 * Wd // 4].mean(); b = np.r_[Ys[:, :H // 8].ravel(), Ys[:, -H // 8:].ravel()].mean()
    out['center_vs_border_luma'] = round(float(c / (b + 1e-3)), 2)
    L = np.abs(lap_var(Ys.mean(0) if False else Ys[len(Ys) // 2]))
    lc = L[H // 4:3 * H // 4, Wd // 4:3 * Wd // 4].mean(); lb = np.r_[L[:H // 6].ravel(), L[-H // 6:].ravel(), L[:, :Wd // 8].ravel(), L[:, -Wd // 8:].ravel()].mean()
    out['sharpness_center_vs_edge'] = round(float(lc / (lb + 1e-5)), 2)

    # --- loop seam
    seam = np.abs(Y[0] - Y[-1]).mean()
    out['loop_seam_ratio'] = round(float(seam / med), 1)  # ~1-3 => seamless loop
    out['loop_seam_abs'] = round(float(seam), 3)
    return out


if __name__ == '__main__':
    for p in sys.argv[1:]:
        try:
            print(json.dumps(analyze(p), ensure_ascii=False), flush=True)
        except Exception as e:
            print(json.dumps(dict(file=p.split('/')[-1], error=repr(e))), flush=True)
