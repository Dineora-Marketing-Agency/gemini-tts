"""Count design/motion patterns across MotionSites prompt files.
Usage: python3 -I prompts_stats.py <dir> [<dir> ...]"""
import sys, os, re, collections, json

files = []
for d in sys.argv[1:]:
    for n in sorted(os.listdir(d)):
        if n.endswith('.md'):
            files.append(os.path.join(d, n))

PAT = {
    # stack
    'framer-motion': r'framer[- ]?motion|motion/react',
    'gsap': r'\bgsap\b|ScrollTrigger',
    'lenis': r'\blenis\b',
    'hls.js': r'hls\.js|\.m3u8|\bHLS\b',
    'three.js / r3f': r'three\.js|react-three|@react-three|\bR3F\b|webgl',
    'spline': r'spline',
    # video handling
    'video autoplay loop muted': r'autoplay.{0,40}(loop|muted)|loop.{0,40}muted',
    'object-cover': r'object-cover|object-fit:\s*cover',
    'custom fade at loop (JS)': r'(fade|opacity).{0,120}(loop|end of|ended|currentTime|duration)|requestAnimationFrame.{0,200}opacity',
    'video overlay gradient': r'(gradient|overlay).{0,80}(over|on top of|above).{0,40}video|video.{0,120}(overlay|gradient)',
    'bottom fade to bg': r'(bottom|to-b|to-t).{0,60}(fade|gradient).{0,60}(black|background|#0|bg-)',
    'video opacity reduced': r'opacity[- :]*(0?\.\d|[1-9]0%)[^\n]{0,60}video|video[^\n]{0,80}opacity[- :]*(0?\.\d|[1-9]0)',
    'mix-blend': r'mix-blend|blend-mode',
    # glass & surfaces
    'liquid glass': r'liquid[- ]glass',
    'backdrop-blur': r'backdrop[- ]blur|backdrop-filter',
    'glassmorphism': r'glassmorph',
    'noise/grain': r'\bnoise\b|\bgrain\b',
    # type
    'Instrument Serif': r'Instrument Serif',
    'Inter': r'\bInter\b',
    'Geist': r'\bGeist\b',
    'General Sans': r'General Sans',
    'Manrope': r'Manrope',
    'Satoshi': r'Satoshi',
    'Poppins': r'Poppins',
    'DM Sans': r'DM Sans',
    'Playfair': r'Playfair',
    'Space Grotesk': r'Space Grotesk',
    'Plus Jakarta': r'Plus Jakarta',
    'Barlow': r'Barlow',
    'italic serif accent': r'italic',
    'tight tracking (negative letter-spacing)': r'tracking-tight|tracking-tighter|letter-spacing:\s*-|tracking-\[-',
    'huge headline (clamp / >64px / text-7xl+)': r'clamp\(|text-[789]xl|text-\[(7|8|9|1\d)\d px|\b(7[2-9]|[89]\d|1\d\d)px',
    'gradient text': r'bg-clip-text|background-clip:\s*text|text-transparent',
    'uppercase': r'uppercase',
    # motion grammar
    'fade + slide up (y)': r'(fade|opacity).{0,60}(slide|y:|translateY|y-)|initial=\{\{\s*opacity:\s*0,\s*y',
    'blur-in (filter blur→0)': r'blur\(\d+px\).{0,80}blur\(0|filter.{0,40}blur.{0,80}(0px|none)|blur-in|blurIn',
    'stagger': r'stagger',
    'word/letter split reveal': r'(word|letter|character|char)[- ]by[- ]|split.{0,20}(word|letter|char)|per[- ](word|letter|char)',
    'scroll-linked (useScroll/scroll-trigger)': r'useScroll|useTransform|scroll[- ](linked|driven|triggered|progress)|whileInView|ScrollTrigger',
    'marquee / infinite scroll': r'marquee|infinite(ly)? scroll',
    'spring physics': r'spring|stiffness|damping',
    'custom cubic-bezier ease': r'\[\s*0?\.\d+\s*,\s*[01]?\.?\d*\s*,\s*0?\.\d+\s*,\s*[01]\.?\d*\s*\]|cubic-bezier',
    'hover scale': r'hover:scale|whileHover',
    'cursor/mouse follow': r'mouse|cursor[- ]follow|onMouseMove|pointer',
    'counter/number animation': r'count[- ]?up|counter|animate.{0,30}number',
    'typewriter': r'typewriter|typing animation|typing effect',
    # theme
    'dark theme': r'dark[- ](theme|mode|background|aesthetic)|#0[0-9a-f]{5}\b|bg-black|#000\b',
    'light theme': r'light (theme|background)|bg-white|#fff\b|#ffffff',
    'pill buttons (rounded-full)': r'rounded-full|9999px|pill',
}

counts = collections.Counter()
per = {}
durs, delays, eases, hexes, sizes = [], [], collections.Counter(), collections.Counter(), []
for f in files:
    t = open(f, encoding='utf-8', errors='replace').read()
    hit = [k for k, p in PAT.items() if re.search(p, t, re.I | re.S)]
    per[os.path.basename(f)] = hit
    counts.update(hit)
    durs += [float(x) for x in re.findall(r'duration[^0-9\n]{0,12}(\d*\.?\d+)\s*s\b', t, re.I)]
    durs += [float(x) / 1000 for x in re.findall(r'duration[^0-9\n]{0,12}(\d{3,4})\s*ms', t, re.I)]
    delays += [float(x) for x in re.findall(r'delay[^0-9\n]{0,12}(\d*\.?\d+)\s*s\b', t, re.I)]
    for e in re.findall(r'\[\s*0?\.\d+\s*,\s*-?[01]?\.?\d*\s*,\s*0?\.\d+\s*,\s*[01]\.?\d*\s*\]', t):
        eases[re.sub(r'\s', '', e)] += 1
    for e in re.findall(r'\b(easeOut|easeInOut|easeIn|linear|anticipate|backOut|circOut|expo\.out|power\d\.out)\b', t):
        eases[e] += 1
    hexes.update(h.lower() for h in re.findall(r'#[0-9a-fA-F]{6}\b', t))
n = len(files)
print(f'{n} prompt files')
for k, v in sorted(counts.items(), key=lambda x: -x[1]):
    print(f'{v:3d} ({v / n * 100:3.0f}%)  {k}')
import statistics as st
print('\nanimation durations (s): n=%d median=%.2f p25=%.2f p75=%.2f' % (len(durs), st.median(durs), st.quantiles(durs, n=4)[0], st.quantiles(durs, n=4)[2]))
print('durations histogram:', collections.Counter(round(d, 2) for d in durs).most_common(12))
print('delays (s): n=%d median=%.2f' % (len(delays), st.median(delays)), collections.Counter(round(d, 2) for d in delays).most_common(12))
print('eases:', eases.most_common(12))
print('top hex:', hexes.most_common(30))
json.dump(per, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', 'prompt_features.json'), 'w'), indent=0)
