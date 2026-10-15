#!/usr/bin/env python3
"""
Prepara um carro novo a partir de fotos e acrescenta-o ao site.

Dois modos:

  showroom  -> showroom 3D da página principal (cars/ + cars.json)
  poster    -> página "Coleção" em estilo poster (poster/img/ + poster/models.json)

Exemplos (a partir da raiz do repositório):

  python tools/preparar_coche.py showroom --id porsche-911-2021 \
      --fotos fotos/911-34frente.jpg fotos/911-traseira.jpg fotos/911-frente.jpg \
      --marca Porsche --modelo "911 Carrera S" --ano 2021 --km 18500 --preco 139900 \
      --combustivel Gasolina --caixa Automática --cv 450 --rotar 0

  python tools/preparar_coche.py poster --id porsche-911 --foto fotos/911-perfil.jpg \
      --esbocos fotos/911-frente.jpg fotos/911-traseira.jpg \
      --marca Porsche --modelo 911 --cursiva "CARRERA S" --cidade Stuttgart \
      --cor "#1d1d1f" --lema "THERE IS|NO|SUBSTITUTE." --eslogan "Pure performance. German precision." \
      --bandeira de --cv 450 --vmax 308 --zero100 3.5 --desde 1948 \
      --icones "engine:Motor 6 cilindros|gauge:ADN de competição|wheel:Condução precisa|heritage:Herança"

Regras das fotos (ver README):
  * Todas as fotos de um carro com o mesmo enquadramento e distância, carro inteiro.
  * Showroom: 1.ª foto = 3/4 frente (imagem principal). A ordem das restantes é a ordem do 360°.
  * Poster: foto de perfil (lado) para o carro; 1-2 fotos de pormenor para os esboços laterais.
  * Se uma foto já for PNG/WebP sem fundo, não é recortada outra vez.
"""
import argparse, json, os, re, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_session = None


# ---------------------------------------------------------------- recorte
def recortar(path):
    """Devolve RGBA sem fundo. Usa rembg só se a imagem ainda tiver fundo."""
    im = Image.open(path)
    if im.mode == 'RGBA' and np.array(im.getchannel('A')).min() < 250:
        rgba = im
    else:
        global _session
        from rembg import remove, new_session
        if _session is None:
            _session = new_session('isnet-general-use')
        rgba = remove(im.convert('RGB'), session=_session, alpha_matting=True,
                      alpha_matting_foreground_threshold=240,
                      alpha_matting_background_threshold=15, alpha_matting_erode_size=8)
    return limpar(rgba, Image.open(path).convert('RGB'))


def limpar(rgba, original):
    """Remove manchas soltas e preenche janelas transparentes com a foto original."""
    from scipy import ndimage
    a = np.array(rgba)
    m = a[..., 3] > 20
    lab, n = ndimage.label(m)
    if n:
        sizes = ndimage.sum(m, lab, range(1, n + 1))
        keep = np.isin(lab, 1 + np.flatnonzero(sizes >= 0.02 * sizes.max()))
        a[..., 3] = np.where(keep | ((a[..., 3] <= 20) & ndimage.binary_dilation(keep, iterations=3)), a[..., 3], 0)
        holes = ndimage.binary_fill_holes(keep) & ~keep
        orig = np.array(original.resize(rgba.size))
        a[holes, :3] = orig[holes]; a[holes, 3] = 255
    return Image.fromarray(a)


def bbox(im):
    return im.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()


def desvanecer_base(im, linhas=14):
    """Evita a sombra cortada a direito por baixo do carro."""
    a = np.array(im); rows = np.nonzero(a[..., 3].max(axis=1) > 40)[0]
    if len(rows):
        yb = rows.max()
        for k in range(linhas):
            y = yb - linhas + 1 + k
            a[y, :, 3] = (a[y, :, 3] * (1 - (k + 1) / linhas)).astype('uint8')
    return Image.fromarray(a)


def mesmo_enquadramento(imgs):
    """Mesmo tamanho para todas: centradas e assentes pelas rodas (sem saltos no 360°)."""
    bbs = [bbox(i) for i in imgs]
    W = max(b[2] - b[0] for b in bbs); H = max(b[3] - b[1] for b in bbs)
    out = []
    for im, b in zip(imgs, bbs):
        cx = (b[0] + b[2]) // 2
        out.append(im.crop((cx - W // 2, b[3] - H, cx - W // 2 + W, b[3])))
    return out


def guardar(im, path, largura, q=86):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im = im.resize((largura, round(im.height * largura / im.width)), Image.LANCZOS)
    im.save(path, 'WEBP', quality=q, method=6)
    return os.path.relpath(path, ROOT).replace(os.sep, '/')


# ---------------------------------------------------------------- esboço a lápis
def esboco(rgba, lado):
    """Converte uma foto recortada num esboço a lápis cinzento sobre transparente."""
    import cv2
    rgb = np.array(rgba.convert('RGB')); alpha = np.array(rgba.getchannel('A'))
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(255 - g, (0, 0), 9)
    dodge = cv2.divide(g, 255 - blur, scale=256)            # efeito "color dodge" = traço de lápis
    dodge = cv2.addWeighted(dodge, .9, cv2.Canny(g, 60, 140) ^ 255, .1, 0)
    linha = np.clip((245 - dodge.astype(float)) / 245 * 255 * 1.1, 0, 255)
    linha = cv2.GaussianBlur(linha, (0, 0), .6)               # traço mais suave, sem serrilhado
    linha = np.minimum(linha * .62, 150) * (alpha / 255.0)   # cinzento claro, como os pósters
    linha = linha.astype('uint8')
    out = Image.fromarray(np.dstack([np.full_like(linha, 40)] * 3 + [linha]), 'RGBA')
    b = bbox(rgba); out = out.crop(b)
    # pormenor ampliado: metade dianteira à esquerda, traseira à direita (como nos pósters)
    w, h = out.size
    meia = out.crop((0, 0, int(w * .55), h)) if lado == 'l' else out.crop((int(w * .45), 0, w, h))
    alvo_h = int(meia.width / .49)                            # proporção vertical dos esboços
    tela = Image.new('RGBA', (meia.width, max(alvo_h, meia.height)), (0, 0, 0, 0))
    tela.alpha_composite(meia, (0, tela.height - meia.height - int(tela.height * .25)))
    # desvanecer o terço de baixo, como nos pósters
    t = np.array(tela); hh = t.shape[0]; ini = int(hh * .55)
    t[ini:, :, 3] = (t[ini:, :, 3] * np.linspace(1, 0, hh - ini)[:, None]).astype('uint8')
    return Image.fromarray(t)


# ---------------------------------------------------------------- JSON helpers
def gravar_lista(path, item, chave='id'):
    dados = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else []
    dados = [d for d in dados if d.get(chave) != item[chave]]
    dados.append(item) if item.get('_fim') else dados.insert(0, item)
    item.pop('_fim', None)
    s = json.dumps(dados, ensure_ascii=False, indent=2)
    s = re.sub(r'"frames": \[\s*([^\]]*?)\s*\]',
               lambda m: '"frames": [' + ', '.join(x.strip() for x in m.group(1).split(',')) + ']' if m.group(1).strip() else '"frames": []',
               s, flags=re.S)
    open(path, 'w', encoding='utf-8').write(s + '\n')
    return dados


def atualizar_fallback(dados):
    """Copia cars.json para o FALLBACK_CARS do index.html (usado se o fetch falhar)."""
    p = os.path.join(ROOT, 'index.html'); h = open(p, encoding='utf-8').read()
    a = h.index('const FALLBACK_CARS = ['); b = h.index('\n];', a) + 3
    h = h[:a] + 'const FALLBACK_CARS = ' + json.dumps(dados, ensure_ascii=False) + ';' + h[b:]
    open(p, 'w', encoding='utf-8').write(h)


def escurecer(hexcor, f=.78):
    n = int(hexcor.lstrip('#'), 16)
    return '#' + ''.join(f'{int(((n >> s) & 255) * f):02x}' for s in (16, 8, 0))


def num(v):
    if v in (None, ''): return None
    return float(v) if '.' in str(v) or ',' in str(v) else int(v)


# ---------------------------------------------------------------- comandos
def cmd_showroom(a):
    print('A recortar', len(a.fotos), 'foto(s)...')
    imgs = [recortar(f) for f in a.fotos]
    if a.rotar:
        imgs = [i.rotate(a.rotar, resample=Image.BICUBIC, expand=True) for i in imgs]
    imgs = [desvanecer_base(i) for i in mesmo_enquadramento(imgs)]
    principal = guardar(imgs[0], os.path.join(ROOT, 'cars', f'{a.id}.webp'), 1600, 88)
    frames = []
    if len(imgs) > 1:
        frames = [guardar(im, os.path.join(ROOT, 'cars', a.id, f'{k + 1}.webp'), 1400, 85) for k, im in enumerate(imgs)]
    carro = {'id': a.id, 'marca': a.marca, 'modelo': a.modelo, 'ano': num(a.ano), 'km': num(a.km),
             'combustivel': a.combustivel, 'caixa': a.caixa, 'potencia_cv': num(a.cv), 'preco': num(a.preco),
             'imagem': principal, 'cor': a.cor, 'frames': frames, 'demo': a.demo, '_fim': a.no_fim}
    dados = gravar_lista(os.path.join(ROOT, 'cars.json'), carro)
    atualizar_fallback(dados)
    print(f'OK: {a.marca} {a.modelo} adicionado ao showroom ({len(frames) or 1} imagem/ns).')


def cmd_poster(a):
    print('A recortar a foto de perfil...')
    carro = recortar(a.foto)
    if a.rotar: carro = carro.rotate(a.rotar, resample=Image.BICUBIC, expand=True)
    carro = desvanecer_base(carro); carro = carro.crop(bbox(carro))
    img = os.path.join(ROOT, 'poster', 'img')
    car_path = guardar(carro, os.path.join(img, f'{a.id}-car.webp'), 1400, 90)
    fontes = a.esbocos or [a.foto]
    rec = [recortar(f) for f in fontes]
    skL = guardar(esboco(rec[0], 'l'), os.path.join(img, f'{a.id}-sketch-l.webp'), 520, 80)
    skR = guardar(esboco(rec[-1], 'r'), os.path.join(img, f'{a.id}-sketch-r.webp'), 520, 80)
    logo = None
    if a.logo:
        lg = recortar(a.logo); lg = lg.crop(bbox(lg))
        logo = guardar(lg, os.path.join(img, f'{a.id}-logo.webp'), min(600, lg.width), 92)
    rel = lambda p: os.path.relpath(os.path.join(ROOT, p), os.path.join(ROOT, 'poster')).replace(os.sep, '/')
    icones = [x.split(':', 1) for x in a.icones.split('|')] if a.icones else \
             [['engine', 'Motor'], ['gauge', 'Desempenho'], ['wheel', 'Condução precisa'], ['heritage', 'Herança']]
    modelo = {
        'id': a.id, 'marca': a.marca, 'titulo': a.titulo or a.marca.upper(), 'cidade': a.cidade,
        'logo': rel(logo) if logo else None, 'logoLargo': a.logo_largo,
        'modelo': a.modelo, 'cursiva': a.cursiva, 'lema': a.lema.split('|'),
        'cor': a.cor, 'cor2': a.cor2 or escurecer(a.cor),
        'carro': rel(car_path), 'esbocoL': rel(skL), 'esbocoR': rel(skR),
        'stats': [s for s in [
            {'l': 'Potência', 'v': num(a.cv), 'u': 'cv'} if a.cv else None,
            {'l': 'Velocidade máx.', 'v': num(a.vmax), 'u': 'km/h'} if a.vmax else None,
            {'l': '0-100 km/h', 'v': num(str(a.zero100).replace(',', '.')), 'u': 's', 'd': len(str(a.zero100).replace(',', '.').split('.')[-1]) if '.' in str(a.zero100).replace(',', '.') else 0} if a.zero100 else None,
        ] if s],
        'eslogan': a.eslogan, 'bandeira': a.bandeira,
        'icones': [[k.strip(), v.strip()] for k, v in icones],
        'rodape': f'{a.marca}<br>desde {a.desde}' if a.desde else a.marca,
        '_fim': True,
    }
    gravar_lista(os.path.join(ROOT, 'poster', 'models.json'), modelo)
    print(f'OK: {a.marca} {a.modelo} adicionado à Coleção Poster.')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)

    s = sub.add_parser('showroom', help='Adicionar/atualizar um carro no showroom 3D')
    s.add_argument('--id', required=True); s.add_argument('--fotos', nargs='+', required=True)
    s.add_argument('--marca', required=True); s.add_argument('--modelo', required=True)
    s.add_argument('--ano'); s.add_argument('--km'); s.add_argument('--preco'); s.add_argument('--cv')
    s.add_argument('--combustivel'); s.add_argument('--caixa')
    s.add_argument('--cor', default='#2a2d33', help='cor da silhueta enquanto a imagem carrega')
    s.add_argument('--rotar', type=float, default=0, help='graus para endireitar (rua inclinada); + = anti-horário')
    s.add_argument('--demo', action='store_true', help='marcar como dado de demonstração')
    s.add_argument('--no-fim', action='store_true', help='colocar no fim da lista (por omissão vai para o início)')
    s.set_defaults(func=cmd_showroom)

    q = sub.add_parser('poster', help='Adicionar/atualizar um modelo na Coleção Poster')
    q.add_argument('--id', required=True); q.add_argument('--foto', required=True, help='foto de perfil')
    q.add_argument('--esbocos', nargs='+', help='1-2 fotos para os esboços laterais (frente / traseira)')
    q.add_argument('--logo', help='imagem do logótipo (opcional)'); q.add_argument('--logo-largo', action='store_true')
    q.add_argument('--marca', required=True); q.add_argument('--titulo', help='nome gigante (por omissão: MARCA)')
    q.add_argument('--modelo', required=True); q.add_argument('--cursiva', help='parte do modelo em itálico preto')
    q.add_argument('--cidade', default=''); q.add_argument('--cor', required=True); q.add_argument('--cor2')
    q.add_argument('--lema', default='PURE|DRIVING|PLEASURE.', help='3 linhas separadas por |')
    q.add_argument('--eslogan', default='Pure performance.')
    q.add_argument('--bandeira', default='none', choices=['uk', 'it', 'de', 'fr', 'pt', 'es', 'jp', 'us', 'se', 'none'])
    q.add_argument('--cv'); q.add_argument('--vmax'); q.add_argument('--zero100')
    q.add_argument('--icones', help='4 ícones "chave:texto|..." (engine, gauge, aero, wheel, fiber, heritage, electric, seat)')
    q.add_argument('--desde', help='ano de fundação da marca')
    q.add_argument('--rotar', type=float, default=0, help='graus para endireitar a foto do carro; + = anti-horário')
    q.set_defaults(func=cmd_poster)

    a = p.parse_args(); a.func(a)


if __name__ == '__main__':
    main()
