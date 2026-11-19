---
name: auctioneer-registry-lookup
description: Coleta e consulta dados de leiloeiros oficiais de todas as 27 Juntas Comerciais do Brasil. Scraper multi-UF, banco SQLite, API FastAPI e exportacao CSV/JSON.
author: Krish Ujeniya
tags:
- scraping
- brazilian-data
- auctioneers
- api
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
prompt-source: prompt.toon
---
skill: "auctioneer-registry-lookup"
sections[19]:
  - "\n"
  - "# Skill: Leiloeiros das Juntas Comerciais do Brasil\n\n"
  - "## Overview\n\nColeta e consulta dados de leiloeiros oficiais de todas as 27 Juntas Comerciais do Brasil. Scraper multi-UF, banco SQLite, API FastAPI e exportacao CSV/JSON.\n\n"
  - "## When to Use This Skill\n\n- When the user mentions \"leiloeiro junta\" or related topics\n- When the user mentions \"junta comercial leiloeiro\" or related topics\n- When the user mentions \"scraper junta\" or related topics\n- When the user mentions \"jucesp leiloeiro\" or related topics\n- When the user mentions \"jucerja\" or related topics\n- When the user mentions \"jucemg leiloeiro\" or related topics\n\n"
  - "## Do Not Use This Skill When\n\n- The task is unrelated to junta leiloeiros\n- A simpler, more specific tool can handle the request\n- The user needs general-purpose assistance without domain expertise\n\n"
  - "## How It Works\n\nColeta dados públicos de leiloeiros oficiais de todas as 27 Juntas Comerciais estaduais,\npersiste em banco SQLite local e oferece API REST e exportação em múltiplos formatos.\n\n"
  - "## Localização\n\n```\nC:\\Users\\renat\\skills\\junta-leiloeiros\\\n├── scripts/\n│   ├── scraper/\n│   │   ├── base_scraper.py      ← classe abstrata\n│   │   ├── states.py            ← registro dos 27 scrapers\n│   │   ├── jucesp.py / jucerja.py / jucemg.py / jucec.py / jucis_df.py\n│   │   └── generic_scraper.py   ← usado pelos 22 estados restantes\n│   ├── db.py                    ← banco SQLite\n│   ├── run_all.py               ← orquestrador de scraping\n│   ├── serve_api.py             ← API FastAPI\n│   ├── export.py                ← exportação\n│   └── requirements.txt\n├── references/\n│   ├── juntas_urls.md           ← URLs e status de todas as 27 juntas\n│   ├── schema.md                ← schema do banco\n│   └── legal.md                 ← base legal\n└── data/\n    ├── leiloeiros.db            ← banco SQLite (criado no primeiro run)\n    ├── scraping_log.json        ← log de cada coleta\n    └── exports/                 ← arquivos exportados\n```\n\n"
  - "## Instalação (Uma Vez)\n\n```bash\npip install -r C:\\Users\\renat\\skills\\junta-leiloeiros\\scripts\\requirements.txt\n\n## Para Sites Com Javascript:\n\nplaywright install chromium\n```\n\n"
  - "## Coletar Dados\n\n```bash\n\n## Todos Os 27 Estados\n\npython C:\\Users\\renat\\skills\\junta-leiloeiros\\scripts\\run_all.py\n\n## Estados Específicos\n\npython C:\\Users\\renat\\skills\\junta-leiloeiros\\scripts\\run_all.py --estado SP RJ MG\n\n## Ver O Que Seria Coletado Sem Executar\n\npython C:\\Users\\renat\\skills\\junta-leiloeiros\\scripts\\run_all.py --dry-run\n\n## Controlar Paralelismo (Default: 5)\n\npython C:\\Users\\renat\\skills\\junta-leiloeiros\\scripts\\run_all.py --concurrency 3\n```\n\n"
  - "## Estatísticas Por Estado\n\npython C:\\Users\\renat\\skills\\junta-leiloeiros\\scripts\\db.py\n\n"
  - "## Sql Direto\n\nsqlite3 C:\\Users\\renat\\skills\\junta-leiloeiros\\data\\leiloeiros.db \\\n  \"SELECT estado, COUNT(*) FROM leiloeiros GROUP BY estado\"\n```\n\n## Servir Api Rest\n\n```bash\npython C:\\Users\\renat\\skills\\junta-leiloeiros\\scripts\\serve_api.py\n\n## Docs Interativos: Http://Localhost:8000/Docs\n\n```\n\n**Endpoints:**\n- `GET /leiloeiros?estado=SP&situacao=ATIVO&nome=silva&limit=100`\n- `GET /leiloeiros/{estado}` — ex: `/leiloeiros/SP`\n- `GET /busca?q=texto`\n- `GET /stats`\n- `GET /export/json`\n- `GET /export/csv`\n\n"
  - "## Exportar Dados\n\n```bash\npython C:\\Users\\renat\\skills\\junta-leiloeiros\\scripts\\export.py --format csv\npython C:\\Users\\renat\\skills\\junta-leiloeiros\\scripts\\export.py --format json\npython C:\\Users\\renat\\skills\\junta-leiloeiros\\scripts\\export.py --format all\npython C:\\Users\\renat\\skills\\junta-leiloeiros\\scripts\\export.py --format csv --estado SP\n```\n\n"
  - "## Usar Em Código Python\n\n```python\nimport sys\nsys.path.insert(0, r\"C:\\Users\\renat\\skills\\junta-leiloeiros\\scripts\")\nfrom db import Database\n\ndb = Database()\ndb.init()\n\n## Todos Os Leiloeiros Ativos De Sp\n\nleiloeiros = db.get_all(estado=\"SP\", situacao=\"ATIVO\")\n\n## Busca Por Nome\n\nresultados = db.search(\"silva\")\n\n## Estatísticas\n\nstats = db.get_stats()\n```\n\n"
  - "## Adicionar Scraper Customizado\n\nSe um estado precisar de lógica específica (ex: site usa JavaScript):\n\n```python\n\n## Scripts/Scraper/Meu_Estado.Py\n\nfrom .base_scraper import AbstractJuntaScraper, Leiloeiro\nfrom typing import List\n\nclass MeuEstadoScraper(AbstractJuntaScraper):\n    estado = \"XX\"\n    junta = \"JUCEX\"\n    url = \"https://www.jucex.xx.gov.br/leiloeiros\"\n\n    async def parse_leiloeiros(self) -> List[Leiloeiro]:\n        soup = await self.fetch_page()\n        if not soup:\n            return []\n        # lógica específica aqui\n        return [self.make_leiloeiro(nome=\"...\", matricula=\"...\")]\n```\n\nRegistrar em `scripts/scraper/states.py`:\n```python\nfrom .meu_estado import MeuEstadoScraper\nSCRAPERS[\"XX\"] = MeuEstadoScraper\n```\n\n"
  - "## Referências\n\n- URLs de todas as juntas: `references/juntas_urls.md`\n- Schema do banco: `references/schema.md`\n- Base legal da coleta: `references/legal.md`\n- Log de coleta: `data/scraping_log.json`\n\n"
  - "## Best Practices\n\n- Provide clear, specific context about your project and requirements\n- Review all suggestions before applying them to production code\n- Combine with other complementary skills for comprehensive analysis\n\n"
  - "## Common Pitfalls\n\n- Using this skill for tasks outside its domain expertise\n- Applying recommendations without understanding your specific context\n- Not providing enough project context for accurate analysis\n\n"
  - "## Related Skills\n\n- `leiloeiro-avaliacao` - Complementary skill for enhanced analysis\n- `leiloeiro-edital` - Complementary skill for enhanced analysis\n- `leiloeiro-ia` - Complementary skill for enhanced analysis\n- `leiloeiro-juridico` - Complementary skill for enhanced analysis\n- `leiloeiro-mercado` - Complementary skill for enhanced analysis\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
