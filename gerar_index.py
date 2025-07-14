import os
import re
from datetime import datetime
from collections import defaultdict
import html

PASTA_BASE = "./pdfs"

# Regex para datas: YYYY-MM-DD ou DD-MM-YYYY ou com underline
PADRAO_DATA = re.compile(r"(\d{4})[-_](\d{2})[-_](\d{2})|(\d{2})[-_](\d{2})[-_](\d{4})")

def limpar_id(texto):
    return re.sub(r'\W+', '_', texto.strip().lower())

def extrair_data(nome_arquivo):
    match = PADRAO_DATA.search(nome_arquivo)
    if not match:
        return None
    try:
        if match.group(1):  # formato AAAA-MM-DD
            return datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        else:  # formato DD-MM-AAAA
            return datetime(int(match.group(6)), int(match.group(5)), int(match.group(4)))
    except:
        return None

# Coleta os arquivos organizados por pasta (podcast)
entradas = []

for root, dirs, files in os.walk(PASTA_BASE):
    nome_podcast = os.path.basename(root).strip()
    if not nome_podcast or nome_podcast.lower() == "pdfs":
        continue
    for file in files:
        if file.lower().endswith(".pdf"):
            data = extrair_data(file)
            if not data:
                print(f"❌ Ignorado (sem data no nome): {file}")
                continue
            caminho_relativo = os.path.join(root, file).replace("\\", "/")
            entradas.append({
                "podcast": nome_podcast,
                "podcast_id": limpar_id(nome_podcast),
                "data": data,
                "arquivo": caminho_relativo
            })

# Agrupa por podcast
entradas.sort(key=lambda x: x["data"], reverse=True)
agrupado = defaultdict(list)

for ep in entradas:
    agrupado[ep["podcast_id"]].append(ep)

# Mapeia nome bonito
nomes_exibicao = {ep["podcast_id"]: ep["podcast"] for ep in entradas}

# Geração do HTML
html_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <title>Biblioteca de Podcasts</title>
  <style>
    body {
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      margin: 0; padding: 0;
      background: #f8f9fa;
      color: #212529;
    }
    header {
      background-color: #343a40;
      padding: 20px;
      color: white;
      text-align: center;
    }
    h1 {
      margin: 0;
      font-size: 28px;
    }
    .tabs {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      background: #e9ecef;
      padding: 10px;
    }
    .tab {
      margin: 5px;
      padding: 10px 20px;
      background: #dee2e6;
      border-radius: 5px;
      cursor: pointer;
      transition: background 0.3s ease;
    }
    .tab:hover {
      background: #ced4da;
    }
    .tab.active {
      background: #495057;
      color: white;
    }
    .tabela {
      display: none;
      margin: 20px auto;
      width: 90%;
      max-width: 900px;
      border-collapse: collapse;
    }
    .tabela.active {
      display: table;
    }
    table {
      width: 100%;
    }
    th, td {
      padding: 12px;
      border: 1px solid #dee2e6;
      text-align: left;
    }
    th {
      background-color: #f1f3f5;
    }
    tr:hover {
      background-color: #f8f9fa;
    }
    a {
      color: #007bff;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
    footer {
      margin-top: 40px;
      text-align: center;
      padding: 20px;
      font-size: 13px;
      color: #868e96;
    }
  </style>
  <script>
    function selecionarAba(id) {
      document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.tabela').forEach(el => el.classList.remove('active'));
      document.getElementById("tab-" + id).classList.add("active");
      document.getElementById("tabela-" + id).classList.add("active");
    }
  </script>
</head>
<body>
  <header>
    <h1>📚 Biblioteca de Podcasts</h1>
  </header>
  <div class="tabs">
"""

ids_ordenados = sorted(nomes_exibicao.keys())
for i, podcast_id in enumerate(ids_ordenados):
    nome = nomes_exibicao[podcast_id]
    classe = "tab active" if i == 0 else "tab"
    html_content += f'<div class="{classe}" id="tab-{podcast_id}" onclick="selecionarAba(\'{podcast_id}\')">{html.escape(nome)}</div>\n'

html_content += "</div>\n"

for i, podcast_id in enumerate(ids_ordenados):
    episodios = agrupado[podcast_id]
    classe = "tabela active" if i == 0 else "tabela"
    html_content += f'<table class="{classe}" id="tabela-{podcast_id}">\n'
    html_content += "<tr><th>Data</th><th>Download</th></tr>\n"
    for ep in episodios:
        data_str = ep["data"].strftime("%d/%m/%Y")
        arquivo = html.escape(ep["arquivo"])
        html_content += f'<tr><td>{data_str}</td><td><a href="{arquivo}" download>Baixar</a></td></tr>\n'
    html_content += "</table>\n"

html_content += """
<footer>
  &copy; 2025 Biblioteca de Podcasts. Todos os direitos reservados.
</footer>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ Página gerada com sucesso!")
