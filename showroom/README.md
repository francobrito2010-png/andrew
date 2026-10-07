# Showroom Virtual — v1.0 (demo)

Experiência tipo "seleção de carro" de videojogo para o stand **Daniel Pinho Automóveis**.
Um único `index.html` (HTML + CSS + JS vanilla), sem build, pronto para GitHub Pages.

```
showroom/
├── index.html   ← tudo (cena, swipe, transição, painel, CTA)
├── cars.json    ← dados dos carros (se falhar o fetch, usa a cópia dentro do JS)
└── cars/        ← PNG sem fundo de cada carro
```

## ⚠️ Dados DEMO a substituir

O site do cliente não pôde ser lido durante o desenvolvimento, por isso **todos os dados são de exemplo**:

- `cars.json`: 6 carros com `"demo": true`. Ao substituir por stock real, remover o campo `demo` (ou pôr `false`).
- `index.html` → objeto `STAND` (início do `<script>`): telefone, WhatsApp, morada, horário, Facebook, Instagram.
- Rodapé (`Financiamento`, `Sobre nós`): textos genéricos.
- Cor de acento: `--accent` em `:root` (agora dourado `#E8B84A`).
- Se mudar `cars.json`, atualizar também `FALLBACK_CARS` no JS (só é usado se o fetch falhar, ex.: abrir em `file://`).

Campo extra opcional por carro: `"cor"`, a cor da silhueta SVG que aparece enquanto não houver PNG.

## Como preparar as imagens dos carros

1. **Fotografar**: vista lateral 3/4 frente, todos os carros virados para o mesmo lado, câmara à mesma altura (~1 m, a meio da porta) e à mesma distância. Luz uniforme, sem sol direto.
2. **Remover o fundo**: com [remove.bg](https://www.remove.bg), no iPhone (manter o dedo sobre o carro na foto → "Copiar"/"Partilhar") ou no Photoshop (*Selecionar assunto* → máscara). Rever as jantes e os vidros, onde o recorte costuma falhar.
3. **Recortar e exportar**: recortar rente ao carro (sem margens), com o carro centrado. Exportar em **PNG transparente com cerca de 1600 px de largura**.
4. **Otimizar e colocar**: passar em [tinypng.com](https://tinypng.com) (objetivo: menos de 400 KB por imagem) e guardar em `cars/` com o nome indicado no campo `imagem` do `cars.json`.

A imagem assenta pela base (rodas) na plataforma, por isso o recorte rente em baixo é o que garante que todos os carros "pousam" à mesma altura.

## Vista 360° (preparada)

Se um carro tiver `"frames": ["cars/bmw/01.png", …]` (24–36 imagens tiradas à volta do carro, com o mesmo enquadramento), o botão **360°** fica ativo e arrastar sobre o carro roda-o. Sem frames, o botão mostra "Em breve".

## Publicar no GitHub Pages

Settings → Pages → Deploy from branch → escolher o branch e a pasta raiz. O showroom fica em `https://<utilizador>.github.io/<repo>/showroom/`.

Para testar localmente (o `fetch` precisa de servidor): `python3 -m http.server` dentro de `showroom/`.
