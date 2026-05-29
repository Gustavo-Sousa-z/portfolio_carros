#!/usr/bin/env python3
"""Lê as pastas em /carros e gera o index.html do portfólio."""

import json
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent
CARROS_DIR = ROOT / "carros"
OUTPUT = ROOT / "index.html"


def formatar_preco(valor: int) -> str:
    return f"R$ {valor:,.0f}".replace(",", ".")


def card_fotos(slug: str, fotos: list[str]) -> str:
    if not fotos:
        return '<div class="sem-foto">Sem foto</div>'

    slides = ""
    indicadores = ""
    for i, foto in enumerate(fotos):
        ativo = "active" if i == 0 else ""
        slides += f'<div class="slide {ativo}"><img src="carros/{slug}/{foto}" alt="Foto {i+1}" loading="lazy"></div>\n'
        indicadores += f'<span class="dot {ativo}" onclick="mudarFoto(this, {i})"></span>\n'

    return f"""
    <div class="galeria">
      <div class="slides">{slides}</div>
      <button class="nav prev" onclick="navFoto(this, -1)">&#8249;</button>
      <button class="nav next" onclick="navFoto(this, 1)">&#8250;</button>
      <div class="dots">{indicadores}</div>
    </div>"""


def gerar_card(slug: str, dados: dict) -> str:
    fotos_html = card_fotos(slug, dados.get("fotos", []))
    badge_cambio = dados.get("cambio", "")
    badge_comb = dados.get("combustivel", "")
    return f"""
    <article class="card">
      {fotos_html}
      <div class="card-body">
        <h2 class="card-titulo">{dados['nome']} <span class="ano">{dados['ano']}</span></h2>
        <p class="preco">{formatar_preco(dados['preco'])}</p>
        <ul class="specs">
          <li><span class="label">KM</span> {f"{dados.get('km', 0):,}".replace(",",".")}</li>
          <li><span class="label">Cor</span> {dados.get('cor', '-')}</li>
          <li><span class="label">Câmbio</span> {badge_cambio}</li>
          <li><span class="label">Combustível</span> {badge_comb}</li>
        </ul>
        <p class="descricao">{dados.get('descricao', '')}</p>
        <a href="https://wa.me/?text=Olá, tenho interesse no {dados['nome']} {dados['ano']}!" class="btn-whatsapp" target="_blank">
          Tenho interesse
        </a>
      </div>
    </article>"""


def carregar_carros() -> list[tuple[str, dict]]:
    resultado = []
    for pasta in sorted(CARROS_DIR.iterdir()):
        json_path = pasta / "dados.json"
        if pasta.is_dir() and json_path.exists():
            dados = json.loads(json_path.read_text(encoding="utf-8"))
            resultado.append((pasta.name, dados))
    return resultado


def gerar_html(carros: list[tuple[str, dict]]) -> str:
    cards = "\n".join(gerar_card(slug, dados) for slug, dados in carros)
    total = len(carros)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Portfólio de Veículos</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: #f0f2f5;
      color: #1a1a1a;
    }}

    header {{
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
      color: white;
      padding: 2.5rem 1rem;
      text-align: center;
    }}
    header h1 {{ font-size: 2rem; letter-spacing: 1px; }}
    header p {{ margin-top: .5rem; opacity: .75; font-size: .95rem; }}

    .filtros {{
      display: flex;
      flex-wrap: wrap;
      gap: .75rem;
      justify-content: center;
      padding: 1.5rem 1rem;
      background: white;
      border-bottom: 1px solid #e0e0e0;
    }}
    .filtros input, .filtros select {{
      padding: .5rem .9rem;
      border: 1px solid #ccc;
      border-radius: 8px;
      font-size: .9rem;
      outline: none;
      transition: border-color .2s;
    }}
    .filtros input:focus, .filtros select:focus {{ border-color: #0f3460; }}

    .contador {{
      text-align: center;
      padding: .75rem;
      font-size: .85rem;
      color: #666;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 1.5rem;
      padding: 1.5rem;
      max-width: 1280px;
      margin: 0 auto;
    }}

    .card {{
      background: white;
      border-radius: 14px;
      overflow: hidden;
      box-shadow: 0 2px 12px rgba(0,0,0,.08);
      transition: transform .2s, box-shadow .2s;
    }}
    .card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,.14); }}

    /* Galeria */
    .galeria {{ position: relative; height: 220px; background: #eee; overflow: hidden; }}
    .slides {{ height: 100%; }}
    .slide {{ display: none; height: 100%; }}
    .slide.active {{ display: block; }}
    .slide img {{ width: 100%; height: 100%; object-fit: cover; }}
    .sem-foto {{
      height: 220px; display: flex; align-items: center; justify-content: center;
      color: #aaa; font-size: .9rem; background: #f5f5f5;
    }}
    .nav {{
      position: absolute; top: 50%; transform: translateY(-50%);
      background: rgba(0,0,0,.45); color: white; border: none;
      width: 32px; height: 32px; border-radius: 50%; cursor: pointer;
      font-size: 1.2rem; line-height: 1; display: flex; align-items: center; justify-content: center;
      opacity: 0; transition: opacity .2s;
    }}
    .galeria:hover .nav {{ opacity: 1; }}
    .prev {{ left: 8px; }}
    .next {{ right: 8px; }}
    .dots {{ position: absolute; bottom: 8px; width: 100%; display: flex; justify-content: center; gap: 5px; }}
    .dot {{
      width: 8px; height: 8px; border-radius: 50%; background: rgba(255,255,255,.6);
      cursor: pointer; transition: background .2s;
    }}
    .dot.active {{ background: white; }}

    .card-body {{ padding: 1.1rem 1.2rem 1.4rem; }}
    .card-titulo {{ font-size: 1.1rem; font-weight: 700; }}
    .ano {{ font-weight: 400; color: #666; font-size: .95rem; }}
    .preco {{ font-size: 1.5rem; font-weight: 800; color: #0f3460; margin: .4rem 0 .8rem; }}

    .specs {{
      display: grid; grid-template-columns: 1fr 1fr;
      gap: .3rem .6rem; list-style: none; font-size: .82rem;
      margin-bottom: .9rem;
    }}
    .specs li {{ color: #555; }}
    .label {{ font-weight: 600; color: #333; }}

    .descricao {{ font-size: .83rem; color: #666; line-height: 1.5; margin-bottom: 1rem; }}

    .btn-whatsapp {{
      display: block; text-align: center; background: #25d366;
      color: white; padding: .65rem; border-radius: 8px;
      text-decoration: none; font-weight: 600; font-size: .9rem;
      transition: background .2s;
    }}
    .btn-whatsapp:hover {{ background: #1da851; }}

    .nenhum {{
      text-align: center; padding: 3rem; color: #999; grid-column: 1/-1;
    }}

    footer {{
      text-align: center; padding: 2rem; color: #999; font-size: .8rem;
      border-top: 1px solid #e0e0e0; margin-top: 1rem;
    }}

    @media (max-width: 480px) {{
      header h1 {{ font-size: 1.4rem; }}
      .grid {{ padding: 1rem .75rem; gap: 1rem; }}
    }}
  </style>
</head>
<body>

<header>
  <h1>🚗 Portfólio de Veículos</h1>
  <p>{total} veículos disponíveis</p>
</header>

<section class="filtros">
  <input type="text" id="busca" placeholder="Buscar por nome, cor..." oninput="filtrar()">
  <select id="cambio" onchange="filtrar()">
    <option value="">Câmbio (todos)</option>
    <option>Manual</option>
    <option>Automático</option>
    <option>CVT</option>
  </select>
  <select id="combustivel" onchange="filtrar()">
    <option value="">Combustível (todos)</option>
    <option>Flex</option>
    <option>Diesel</option>
    <option>Elétrico</option>
    <option>Gasolina</option>
  </select>
  <select id="ordem" onchange="filtrar()">
    <option value="nome">Ordenar: Nome</option>
    <option value="preco_asc">Menor preço</option>
    <option value="preco_desc">Maior preço</option>
    <option value="km_asc">Menor KM</option>
    <option value="ano_desc">Mais novo</option>
  </select>
</section>

<p class="contador" id="contador"></p>

<main class="grid" id="grid">
{cards}
</main>

<footer>Portfólio atualizado automaticamente · Gerado em {__import__('datetime').date.today().strftime('%d/%m/%Y')}</footer>

<script>
  // Galeria por card
  function mudarFoto(dot, idx) {{
    const galeria = dot.closest('.galeria');
    galeria.querySelectorAll('.slide').forEach((s, i) => s.classList.toggle('active', i === idx));
    galeria.querySelectorAll('.dot').forEach((d, i) => d.classList.toggle('active', i === idx));
  }}
  function navFoto(btn, dir) {{
    const galeria = btn.closest('.galeria');
    const slides = [...galeria.querySelectorAll('.slide')];
    const dots   = [...galeria.querySelectorAll('.dot')];
    const atual  = slides.findIndex(s => s.classList.contains('active'));
    const prox   = (atual + dir + slides.length) % slides.length;
    slides.forEach((s, i) => s.classList.toggle('active', i === prox));
    dots.forEach((d, i)   => d.classList.toggle('active', i === prox));
  }}

  // Filtros
  const todosCards = [...document.querySelectorAll('.card')];
  function filtrar() {{
    const busca   = document.getElementById('busca').value.toLowerCase();
    const cambio  = document.getElementById('cambio').value;
    const comb    = document.getElementById('combustivel').value;
    const ordem   = document.getElementById('ordem').value;

    let visiveis = todosCards.filter(card => {{
      const txt   = card.textContent.toLowerCase();
      const specs = [...card.querySelectorAll('.specs li')].map(l => l.textContent);
      const okBusca  = !busca  || txt.includes(busca);
      const okCambio = !cambio || specs.some(s => s.includes(cambio));
      const okComb   = !comb   || specs.some(s => s.includes(comb));
      return okBusca && okCambio && okComb;
    }});

    visiveis.sort((a, b) => {{
      const preco = el => parseInt(el.querySelector('.preco').textContent.replace(/\\D/g,''));
      const km    = el => parseInt([...el.querySelectorAll('.specs li')].find(l=>l.textContent.includes('KM'))?.textContent.replace(/\\D/g,'') || 0);
      const ano   = el => parseInt(el.querySelector('.ano')?.textContent || 0);
      if (ordem === 'preco_asc')  return preco(a) - preco(b);
      if (ordem === 'preco_desc') return preco(b) - preco(a);
      if (ordem === 'km_asc')     return km(a) - km(b);
      if (ordem === 'ano_desc')   return ano(b) - ano(a);
      return a.querySelector('.card-titulo').textContent.localeCompare(b.querySelector('.card-titulo').textContent);
    }});

    const grid = document.getElementById('grid');
    todosCards.forEach(c => c.style.display = 'none');
    visiveis.forEach(c => {{ c.style.display = ''; grid.appendChild(c); }});

    const contador = document.getElementById('contador');
    if (visiveis.length === 0) {{
      contador.textContent = '';
      if (!grid.querySelector('.nenhum')) {{
        const msg = document.createElement('p');
        msg.className = 'nenhum'; msg.textContent = 'Nenhum veículo encontrado com esses filtros.';
        grid.appendChild(msg);
      }}
    }} else {{
      grid.querySelector('.nenhum')?.remove();
      contador.textContent = `Exibindo ${{visiveis.length}} de {total} veículos`;
    }}
  }}

  filtrar();
</script>
</body>
</html>"""


if __name__ == "__main__":
    carros = carregar_carros()
    if not carros:
        print("Nenhuma pasta de carro encontrada em /carros/")
        raise SystemExit(1)
    html = gerar_html(carros)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"✅ index.html gerado com {len(carros)} veículos.")
