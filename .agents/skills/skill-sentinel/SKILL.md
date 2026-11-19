---
name: skill-sentinel
description: Auditoria e evolucao do ecossistema de skills. Qualidade de codigo, seguranca, custos, gaps, duplicacoes, dependencias e relatorios de saude.
risk: safe
source: community
date_added: '2026-03-06'
author: "Krish Ujeniya"
tags:
- governance
- audit
- quality
- skill-health
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
prompt-source: prompt.toon
---
skill: "skill-sentinel"
sections[27]:
  - "\n"
  - "# Skill Sentinel\n\n"
  - "## Overview\n\nAuditoria e evolucao do ecossistema de skills. Qualidade de codigo, seguranca, custos, gaps, duplicacoes, dependencias e relatorios de saude.\n\n"
  - "## When to Use This Skill\n\n- When the user mentions \"auditar skills\" or related topics\n- When the user mentions \"qualidade skills\" or related topics\n- When the user mentions \"verificar skills ecossistema\" or related topics\n- When the user mentions \"saude ecossistema skills\" or related topics\n- When the user mentions \"skills duplicadas\" or related topics\n- When the user mentions \"otimizar skills\" or related topics\n\n"
  - "## Do Not Use This Skill When\n\n- The task is unrelated to skill sentinel\n- A simpler, more specific tool can handle the request\n- The user needs general-purpose assistance without domain expertise\n\n"
  - "## How It Works\n\nMeta-agente que monitora, audita e evolui o ecossistema de skills. Analisa\ntodas as skills em 7 dimensoes, identifica problemas, sugere melhorias\ne recomenda novas skills especialistas.\n\n"
  - "## Resumo Rapido\n\n| Area | Script | O que faz |\n|------|--------|-----------|\n| **Discovery** | `scanner.py` | Descobre todas as skills automaticamente |\n| **Qualidade** | `analyzers/code_quality.py` | Complexidade, docstrings, error handling |\n| **Seguranca** | `analyzers/security.py` | Secrets, SQL injection, HTTPS |\n| **Performance** | `analyzers/performance.py` | API calls, caching, retry |\n| **Governanca** | `analyzers/governance_audit.py` | Rate limits, audit log, confirmacoes |\n| **Documentacao** | `analyzers/documentation.py` | SKILL.md, triggers, references |\n| **Dependencias** | `analyzers/dependencies.py` | requirements.txt, versoes |\n| **Cross-Skill** | `analyzers/cross_skill.py` | Duplicacao, padroes compartilhados |\n| **Custos** | `cost_optimizer.py` | Tokens, verbosidade, output |\n| **Recomendacoes** | `recommender.py` | Gap analysis, novas skills |\n| **Relatorio** | `report_generator.py` | Markdown estruturado |\n| **Orquestracao** | `run_audit.py` | CLI principal |\n\n"
  - "## Localizacao\n\n```\nC:\\Users\\renat\\skills\\skill-sentinel\\\n├── SKILL.md\n├── scripts/\n│   ├── requirements.txt\n│   ├── config.py\n│   ├── db.py\n│   ├── governance.py\n│   ├── scanner.py\n│   ├── analyzers/\n│   │   ├── code_quality.py\n│   │   ├── security.py\n│   │   ├── performance.py\n│   │   ├── governance_audit.py\n│   │   ├── documentation.py\n│   │   ├── dependencies.py\n│   │   └── cross_skill.py\n│   ├── recommender.py\n│   ├── cost_optimizer.py\n│   ├── report_generator.py\n│   └── run_audit.py\n├── references/\n│   ├── analysis_criteria.md\n│   ├── security_patterns.md\n│   ├── skill_template.md\n│   └── schema.md\n└── data/\n    ├── sentinel.db\n    └── reports/\n```\n\n"
  - "## Instalacao\n\n```bash\npip install -r C:\\Users\\renat\\skills\\skill-sentinel\\scripts\\requirements.txt\n```\n\n"
  - "## Comandos Principais\n\n```bash\n\n## Auditoria Completa De Todas As Skills\n\npython C:\\Users\\renat\\skills\\skill-sentinel\\scripts\\run_audit.py\n\n## Auditar Apenas Uma Skill\n\npython C:\\Users\\renat\\skills\\skill-sentinel\\scripts\\run_audit.py --skill instagram\n\n## Apenas Recomendacoes De Novas Skills\n\npython C:\\Users\\renat\\skills\\skill-sentinel\\scripts\\run_audit.py --recommend\n\n## Comparar Com Auditoria Anterior (Tendencias)\n\npython C:\\Users\\renat\\skills\\skill-sentinel\\scripts\\run_audit.py --compare\n\n## Output Em Json (Para Processamento)\n\npython C:\\Users\\renat\\skills\\skill-sentinel\\scripts\\run_audit.py --format json\n\n## Ver Historico De Auditorias\n\npython C:\\Users\\renat\\skills\\skill-sentinel\\scripts\\run_audit.py --history\n\n## Descobrir Skills Disponiveis\n\npython C:\\Users\\renat\\skills\\skill-sentinel\\scripts\\scanner.py\n\n## Ver Audit Log Do Sentinel\n\npython C:\\Users\\renat\\skills\\skill-sentinel\\scripts\\governance.py\n\n## Verificar Banco De Dados\n\npython C:\\Users\\renat\\skills\\skill-sentinel\\scripts\\db.py\n```\n\n"
  - "## 1. Qualidade De Codigo (Peso: 20%)\n\n- Complexidade ciclomatica por funcao (limiar: 10)\n- Tamanho de funcoes (limiar: 50 linhas)\n- Tamanho de arquivos (limiar: 500 linhas)\n- Cobertura de docstrings\n- Padroes de error handling (bare except, broad except)\n\n"
  - "## 2. Seguranca (Peso: 20%)\n\n- Secrets hardcoded (tokens, passwords, API keys)\n- SQL injection (f-strings em queries)\n- URLs HTTP inseguras\n- Tokens em logs\n- Validacao de input\n\n"
  - "## 3. Performance (Peso: 15%)\n\n- Retry com backoff para APIs\n- Timeouts configurados\n- Reuso de conexoes HTTP\n- N+1 queries\n- Async/concorrencia\n\n"
  - "## 4. Governanca (Peso: 15%)\n\n- Nivel 0: Nenhuma\n- Nivel 1: Action logging\n- Nivel 2: Logging + rate limiting\n- Nivel 3: Completa (+ confirmacoes 2-step)\n- Nivel 4: Avancada (+ alertas e trends)\n\n"
  - "## 5. Documentacao (Peso: 15%)\n\n- SKILL.md com frontmatter (name, description, version)\n- Trigger keywords (PT-BR e EN)\n- Secoes obrigatorias e recomendadas\n- Reference files\n\n"
  - "## 6. Dependencias (Peso: 15%)\n\n- requirements.txt presente\n- Versoes pinadas\n- Deps importadas vs listadas\n- Deps listadas vs importadas\n\n"
  - "## 7. Cross-Skill (Analise Global)\n\n- Modulos duplicados entre skills\n- Padroes de Database compartilhados\n- Governanca inconsistente\n- Oportunidades de extracao\n\n"
  - "## Otimizacao De Custos\n\nAlem das 7 dimensoes, o sentinel analisa impacto de custo:\n- Tamanho do SKILL.md (tokens consumidos por ativacao)\n- References grandes sem indice\n- Output verboso dos scripts\n- Ausencia de output JSON estruturado\n\n"
  - "## Gap Analysis E Recomendacoes\n\nO recommender identifica capacidades ausentes no ecossistema comparando\ncom uma taxonomia de 20 categorias e gera templates de SKILL.md prontos\npara novas skills sugeridas.\n\n"
  - "## Governanca Do Sentinel\n\nO proprio sentinel pratica o que prega:\n- Todas as auditorias sao registradas em action_log\n- Historico de scores em score_history para tendencias\n- Relatorios salvos em data/reports/\n\n"
  - "## Workflows Comuns\n\n**1. Primeira auditoria do ecossistema:**\n```\npython run_audit.py\n```\nGera relatorio completo com scores, findings e recomendacoes.\n\n**2. Monitorar evolucao ao longo do tempo:**\n```\npython run_audit.py --compare\n```\nMostra delta de scores entre auditorias.\n\n**3. Validar uma skill antes de deploy:**\n```\npython run_audit.py --skill nome-da-skill\n```\nAuditoria focada com findings especificos.\n\n**4. Identificar proxima skill a criar:**\n```\npython run_audit.py --recommend\n```\nGap analysis com templates prontos.\n\n"
  - "## Formato Do Relatorio\n\nO relatorio gerado em `data/reports/` contem:\n1. Resumo executivo (tabela de scores)\n2. Tendencias (se houver auditoria anterior)\n3. Findings por severidade (critico/alto/medio/baixo/info)\n4. Analise por skill (detalhada)\n5. Recomendacoes de novas skills\n6. Plano de acao priorizado\n\n"
  - "## Referencias\n\nPara detalhes tecnicos, consultar:\n- `references/analysis_criteria.md` - Rubricas de scoring\n- `references/security_patterns.md` - Padroes de seguranca\n- `references/skill_template.md` - Template para novas skills\n- `references/schema.md` - Schema do banco de dados\n\n"
  - "## Best Practices\n\n- Provide clear, specific context about your project and requirements\n- Review all suggestions before applying them to production code\n- Combine with other complementary skills for comprehensive analysis\n\n"
  - "## Common Pitfalls\n\n- Using this skill for tasks outside its domain expertise\n- Applying recommendations without understanding your specific context\n- Not providing enough project context for accurate analysis\n\n"
  - "## Related Skills\n\n- `skill-installer` - Complementary skill for enhanced analysis\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
