---
name: performance-monitor
description: Monitor de performance do Claude Code e sistema local. Diagnostica lentidao, mede CPU/RAM/disco, verifica API latency e gera relatorios de saude do sistema.
risk: safe
source: community
date_added: '2026-03-06'
author: "Krish Ujeniya"
tags:
- monitoring
- performance
- diagnostics
- system-health
tools:
- claude-code
- antigravity
- cursor
- gemini-cli
- codex-cli
prompt-source: prompt.toon
---
skill: "performance-monitor"
sections[22]:
  - "\n"
  - "# Claude Monitor — Diagnóstico de Performance\n\n"
  - "## Overview\n\nMonitor de performance do Claude Code e sistema local. Diagnostica lentidao, mede CPU/RAM/disco, verifica API latency e gera relatorios de saude do sistema.\n\n"
  - "## When to Use This Skill\n\n- When the user mentions \"lento\" or related topics\n- When the user mentions \"lentidao\" or related topics\n- When the user mentions \"lag\" or related topics\n- When the user mentions \"lagado\" or related topics\n- When the user mentions \"travando\" or related topics\n- When the user mentions \"claude lento\" or related topics\n\n"
  - "## Do Not Use This Skill When\n\n- The task is unrelated to claude monitor\n- A simpler, more specific tool can handle the request\n- The user needs general-purpose assistance without domain expertise\n\n"
  - "## How It Works\n\nSkill para diagnosticar e resolver problemas de lentidão no Claude Code e no sistema.\nDetermina se o gargalo é local (PC) ou remoto (API Claude) e sugere ações corretivas.\n\n"
  - "## Quando Usar\n\n- Usuário reclama que o Claude Code está lento ou travando\n- Troca de sessões de conversa demora para carregar\n- Respostas do Claude demoram muito\n- PC parece lento enquanto usa o Claude Code\n- Qualquer menção a performance, lag, lentidão\n\n"
  - "## 1. Diagnóstico Rápido (Health_Check.Py)\n\nRode SEMPRE como primeiro passo:\n\n```bash\npython C:\\Users\\renat\\skills\\claude-monitor\\scripts\\health_check.py\n```\n\nO script analisa em ~3 segundos:\n- **CPU**: Uso atual e por core. >80% = gargalo provável\n- **RAM**: Total, usada, disponível. >85% = pressão de memória\n- **Browsers**: Processos e RAM por browser. >5GB total = excesso de abas\n- **Claude Code**: Processos e RAM consumida\n- **Disco**: Espaço livre. <10% = impacto em swap/performance\n- **Rede**: Latência ao endpoint da API Claude\n- **Diagnóstico**: Classificação automática do problema com sugestões\n\n"
  - "## 2. Interpretar O Resultado\n\nO script retorna um JSON com `diagnosis` contendo:\n\n- `bottleneck`: \"cpu\" | \"ram\" | \"browsers\" | \"disk\" | \"network\" | \"claude_api\" | \"ok\"\n- `severity`: \"critical\" | \"warning\" | \"ok\"\n- `suggestions`: Lista de ações recomendadas\n- `summary`: Resumo em português para mostrar ao usuário\n\n**Mostre o `summary` ao usuário** e ofereça executar as sugestões.\n\n"
  - "## 3. Ações Corretivas Automáticas\n\nBaseado no diagnóstico, ofereça ao usuário:\n\n"
  - "#### Se CPU alta (>80%):\n- Listar processos consumindo mais CPU\n- Sugerir fechar processos pesados desnecessários\n- Verificar se Windows Update está rodando em background\n\n"
  - "#### Se browsers pesados (>5GB RAM ou >40 processos):\n```bash\npython C:\\Users\\renat\\skills\\claude-monitor\\scripts\\health_check.py --browsers-detail\n```\nMostra RAM por browser e sugere quais fechar. **Nunca fechar processos sem permissão explícita do usuário.**\n\n"
  - "#### Se disco cheio (>85%):\n- Mostrar pastas maiores\n- Sugerir limpeza de Temp, cache de browsers, lixeira\n\n"
  - "#### Se rede lenta (latência >500ms):\n- Testar conexão com api.anthropic.com\n- Sugerir verificar VPN, proxy, ou conexão WiFi\n\n"
  - "## 4. Monitor Contínuo (Opcional)\n\nSe o usuário quiser monitoramento em background:\n\n```bash\npython C:\\Users\\renat\\skills\\claude-monitor\\scripts\\monitor.py --interval 30 --duration 300\n```\n\nParâmetros:\n- `--interval`: Segundos entre cada amostra (default: 30)\n- `--duration`: Duração total em segundos (default: 300 = 5 min)\n- `--output`: Caminho do arquivo de log (default: monitor_log.json)\n- `--alert-cpu`: Threshold de CPU para alerta (default: 80)\n- `--alert-ram`: Threshold de RAM % para alerta (default: 85)\n\nO monitor salva snapshots periódicos e gera um relatório ao final com:\n- Picos de CPU e RAM\n- Tendência (melhorando/piorando/estável)\n- Eventos de alerta detectados\n- Recomendação final\n\n"
  - "## 5. Benchmark Da Api Claude (Opcional)\n\nPara testar se a lentidão é da API:\n\n```bash\npython C:\\Users\\renat\\skills\\claude-monitor\\scripts\\api_bench.py\n```\n\nMede o tempo de resposta do processo Claude Code local (não faz chamadas à API).\nCompara com tempos típicos e indica se está dentro do esperado.\n\n"
  - "## Thresholds De Referência\n\n| Métrica | OK | Warning | Critical |\n|---------|-----|---------|----------|\n| CPU % | <60% | 60-85% | >85% |\n| RAM usada % | <70% | 70-85% | >85% |\n| RAM browsers | <3 GB | 3-6 GB | >6 GB |\n| Processos browser | <30 | 30-60 | >60 |\n| Disco livre | >15% | 10-15% | <10% |\n| Latência rede | <200ms | 200-500ms | >500ms |\n\n"
  - "## Dicas Para O Usuário\n\nQuando apresentar o diagnóstico, inclua estas dicas contextuais:\n\n- **Muitas abas = muito CPU/RAM**: Cada aba de browser é um processo separado.\n  50 abas = 50 processos competindo por recursos.\n- **Claude Code é pesado**: Ele roda vários processos Electron. É normal consumir 3-5 GB.\n  Mas se estiver usando >6 GB com várias sessões, considere fechar sessões antigas.\n- **Troca de sessão lenta**: Geralmente causada por CPU alta ou muitos processos competindo.\n  A sessão precisa carregar o histórico da conversa, e se o CPU está ocupado, demora.\n- **Disco quase cheio**: Afeta a velocidade do swap (memória virtual) e pode causar\n  lentidão generalizada.\n\n"
  - "## Dependências\n\n- Python 3.10+\n- psutil (instalado automaticamente pelo script se não disponível)\n- Nenhuma API key necessária\n\n"
  - "## Best Practices\n\n- Provide clear, specific context about your project and requirements\n- Review all suggestions before applying them to production code\n- Combine with other complementary skills for comprehensive analysis\n\n"
  - "## Common Pitfalls\n\n- Using this skill for tasks outside its domain expertise\n- Applying recommendations without understanding your specific context\n- Not providing enough project context for accurate analysis\n\n"
  - "## Limitations\n- Use this skill only when the task clearly matches the scope described above.\n- Do not treat the output as a substitute for environment-specific validation, testing, or expert review.\n- Stop and ask for clarification if required inputs, permissions, safety boundaries, or success criteria are missing.\n"
