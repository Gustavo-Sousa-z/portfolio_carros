# Portfólio de Veículos — Documentação

## Visão geral

Este projeto é um site estático de portfólio de veículos hospedado no GitHub Pages. O conteúdo é gerenciado por pastas e arquivos JSON — sem painel administrativo, sem banco de dados. Uma pipeline no GitHub Actions lê essas pastas e gera o `index.html` automaticamente a cada atualização.

---

## Estrutura do projeto

```
carros/
├── .github/
│   └── workflows/
│       └── build.yml        ← pipeline de build e deploy
├── carros/
│   ├── gol-2022/
│   │   ├── dados.json       ← informações do veículo
│   │   └── gol-2022.webp   ← foto(s) do veículo
│   └── civic-2021/
│       ├── dados.json
│       └── civic.webp
├── scripts/
│   └── build.py             ← script que gera o index.html
└── index.html               ← gerado automaticamente (não editar à mão)
```

---

## Como adicionar um novo veículo

### 1. Criar a pasta do veículo

Dentro da pasta `carros/`, crie uma subpasta com o padrão `modelo-ano`. Use letras minúsculas e hífens, sem espaços ou acentos.

```
carros/
└── corolla-2023/
```

### 2. Adicionar as fotos

Coloque as imagens do veículo dentro da pasta criada. Formatos aceitos: `.jpg`, `.jpeg`, `.png`, `.webp`.

Recomendação: use o mesmo padrão da pasta para nomear o arquivo, ex: `corolla-2023.webp`.

```
corolla-2023/
├── corolla-2023.webp
└── corolla-2023-interior.webp   ← segunda foto (opcional)
```

### 3. Criar o arquivo `dados.json`

Dentro da pasta do veículo, crie um arquivo chamado exatamente `dados.json` com a seguinte estrutura:

```json
{
  "nome": "Toyota Corolla",
  "ano": 2023,
  "preco": 159900,
  "km": 12000,
  "cor": "Cinza",
  "cambio": "Automático",
  "combustivel": "Flex",
  "descricao": "Corolla XEi com central multimídia, câmera de ré e controle de cruzeiro. Único dono, revisões em dia.",
  "fotos": ["corolla-2023.webp", "corolla-2023-interior.webp"]
}
```

---

## Referência dos campos do `dados.json`

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `nome` | string | Sim | Nome completo do veículo (marca + modelo) |
| `ano` | número | Sim | Ano de fabricação |
| `preco` | número | Sim | Preço em reais, sem formatação (ex: `89900`) |
| `km` | número | Sim | Quilometragem atual (ex: `32000`) |
| `cor` | string | Sim | Cor do veículo |
| `cambio` | string | Sim | `"Manual"`, `"Automático"` ou `"CVT"` |
| `combustivel` | string | Sim | `"Flex"`, `"Gasolina"`, `"Diesel"` ou `"Elétrico"` |
| `descricao` | string | Sim | Texto de apresentação do veículo |
| `fotos` | array | Sim | Lista com os nomes dos arquivos de imagem da pasta |

> **Atenção:** os nomes em `fotos` precisam ser exatamente iguais aos nomes dos arquivos na pasta, incluindo a extensão (`.jpg`, `.webp`, etc.).

---

## Como remover um veículo

Basta apagar a pasta inteira do veículo dentro de `carros/`. Na próxima execução da pipeline, o veículo não aparecerá mais no site.

---

## O script de build (`scripts/build.py`)

O script é responsável por ler todas as pastas dentro de `carros/`, montar os cards HTML e gerar o `index.html` na raiz do projeto.

### O que ele faz, passo a passo

1. Percorre todas as subpastas de `carros/` em ordem alfabética
2. Lê o `dados.json` de cada pasta
3. Monta o HTML de cada card de veículo com galeria de fotos, especificações e botão de contato
4. Gera o `index.html` completo com filtros e ordenação

### Rodar o script localmente (opcional)

Requer Python 3.10 ou superior. Não há dependências externas.

```bash
python3 scripts/build.py
```

O arquivo `index.html` será gerado/atualizado na raiz do projeto.

---

## A pipeline do GitHub Actions (`.github/workflows/build.yml`)

### Quando a pipeline roda

A pipeline é disparada em três situações:

| Gatilho | Quando ocorre |
|---|---|
| **Push na branch `main`** | Sempre que houver alteração em `carros/**` ou em `scripts/build.py` |
| **Schedule automático** | Todo dia às 6h (horário de Brasília) |
| **Manual** | Pelo botão "Run workflow" na aba Actions do GitHub |

### O que a pipeline faz

**Job `build`**
1. Faz checkout do repositório
2. Instala o Python 3.12
3. Executa `python scripts/build.py` para gerar o `index.html`
4. Faz commit e push do `index.html` atualizado (somente se houve mudança)

**Job `deploy`**
1. Aguarda o job `build` terminar
2. Pega o código atualizado (incluindo o novo `index.html`)
3. Publica no GitHub Pages

### Como rodar a pipeline manualmente

1. Acesse o repositório no GitHub
2. Clique na aba **Actions**
3. Selecione **Build & Deploy Portfólio** no menu lateral
4. Clique em **Run workflow** → **Run workflow**

---

## Configuração inicial do GitHub Pages

Feita uma única vez após criar o repositório:

1. Vá em **Settings** → **Pages**
2. Em **Source**, selecione **GitHub Actions**
3. Salve

O site ficará disponível em:

```
https://SEU_USUARIO.github.io/NOME_DO_REPOSITORIO/
```

---

## Boas práticas

- **Não edite o `index.html` manualmente.** Ele é sobrescrito pela pipeline a cada build.
- **Mantenha os nomes de arquivo sem espaços ou caracteres especiais** para evitar problemas de referência nas URLs.
- **Fotos muito pesadas** (acima de 1 MB) deixam o site lento. Prefira imagens otimizadas em `.webp` com resolução de até 1200×800px.
- **O campo `preco` deve ser um número puro**, sem `R$`, pontos ou vírgulas. A formatação é aplicada automaticamente pelo script.