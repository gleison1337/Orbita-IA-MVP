# 🪐 Órbita IA - MVP

**Sistema Inteligente de Análise de Incidentes e Suporte Técnico**

O **Órbita IA** é uma solução desenvolvida em Python projetada para revolucionar a triagem e a análise preliminar de chamados de TI (Service Desk). Utilizando inteligência artificial, o sistema processa filas de incidentes brutos e entrega análises técnicas, priorização e sugestões de solução em segundos.

---

## 🚀 Performance e Eficiência

O sistema foi otimizado para alta performance na análise individual de tickets. Considerando um tempo médio de processamento de **10 segundos por chamado**, o Órbita IA oferece uma capacidade de vazão muito superior à triagem manual humana:

| Tempo Decorrido | Chamados Analisados |
| :--- | :--- |
| **1 Minuto** | 6 chamados |
| **10 Minutos** | **60 chamados** |
| **20 Minutos** | **120 chamados** |
| **1 Hora** | 360 chamados |

> *Enquanto um analista humano gastaria minutos lendo e categorizando apenas um incidente complexo, o Órbita IA já processou dezenas, permitindo que a equipe foque na resolução e não na triagem.*

---

## 🎯 Impacto Estratégico no N1 (Nível 1)

O objetivo principal deste MVP é **empoderar o Suporte Nível 1**. Ao invés de receber um chamado "cru" e perder tempo investigando o problema do zero, o analista já recebe:

1.  **Diagnóstico Pré-Processado:** O sistema já leu o JSON do incidente.
2.  **Análise de Humor:** Identifica se o usuário está crítico/irritado para priorização de atendimento.
3.  **Sugestão de Solução:** Baseado em padrões anteriores, a IA já sugere o *fix* provável.

Isso transforma o N1 de um "atendedor de telefone" para um **analista estratégico**, reduzindo drasticamente o MTTR (Mean Time to Repair) e aumentando a satisfação do cliente.

---

## 🛠️ Como Funciona

O fluxo de funcionamento do MVP é direto:

1.  **Input:** O sistema lê um arquivo `incidents.json` contendo o dump da fila de chamados.
2.  **Processamento:** O script `orbita.py` itera sobre cada objeto JSON (chamado).
3.  **Análise:**
    * Interpretação da descrição do erro.
    * Cálculo de prioridade técnica.
    * Análise de sentimento do solicitante.
4.  **Output:** Gera um relatório técnico detalhado para cada incidente.

---

## 💻 Tecnologias

* **Python 3**
* **Integração via JSON**
* **Lógica de IA para Processamento de Linguagem Natural (NLP)**

---

### Status do Projeto
✅ MVP Funcional (V2)
🚧 Integração via API (Em Roadmap)

---
*Desenvolvido com foco em agilidade e inteligência para operações de TI.*