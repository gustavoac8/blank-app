# Domina Receita Médica

Plataforma SaaS modular para clínicas médicas (foco em estética) com diagnóstico, plano estratégico, automação de aquisição, CRM e retenção.

## Visão geral de módulos

1. **Diagnóstico Inteligente**: briefing dinâmico + classificação por IA.
2. **Plano de Ação Automático**: prioridades por horizonte e estimativa de impacto.
3. **Geração de Landing Page**: copy persuasiva orientada a conversão.
4. **Gestão de Tráfego Pago**: integração mock de Google/Meta Ads + otimização de orçamento.
5. **CRM e Funil**: pipeline de pacientes (lead → faturamento).
6. **Follow-up Automatizado**: até 5 tentativas (WhatsApp/Email) + nutrição.
7. **Pós-venda e Expansão**: base para recorrência/lookalike.
8. **Dashboard Principal**: leads, conversão, CPL, ROI, faturamento estimado.

## Arquitetura

- **Frontend**: Streamlit (dashboard SaaS responsivo para operação interna).
- **Backend**: FastAPI + autenticação JWT + multi-tenant por `organization_id`.
- **Banco**: SQLAlchemy (SQLite local, compatível com Postgres/Supabase).
- **IA**: orquestrador com heurística + ponto de extensão para OpenAI/Claude.
- **Integrações**: mocks de Google Ads e Meta Ads (`app/services/ads_mock.py`).

## Estrutura

```txt
app/
  api/          # rotas e dependências de autenticação
  core/         # config e segurança
  db/           # models SQLAlchemy e schemas Pydantic
  services/     # IA, landing generator, ads, follow-up
  tests/        # testes automatizados
streamlit_app.py
```

## Como rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# em outro terminal
streamlit run streamlit_app.py
```

## Endpoints principais

- `POST /auth/register`
- `POST /auth/token`
- `POST /diagnosis`
- `GET /plans/latest`
- `POST /landing/generate`
- `POST /campaigns`
- `POST /crm/patients`
- `PATCH /crm/patients/{id}/stage`
- `POST /crm/patients/{id}/follow-up`
- `GET /dashboard`

## Deploy (produção)

### Opção recomendada (Vercel + Supabase + Railway)

1. **Supabase (Postgres)**
   - Criar projeto e copiar `DATABASE_URL`.
   - Ajustar `database_url` no `.env`.
2. **Railway (API FastAPI)**
   - Deploy do repositório.
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
   - Variáveis: `SECRET_KEY`, `DATABASE_URL`, `ENVIRONMENT=production`.
3. **Vercel (front web)**
   - Pode hospedar frontend web dedicado consumindo esta API.
   - Para esta entrega, o dashboard operacional está em `streamlit_app.py`.

## Roadmap para integrações reais

- OpenAI/Claude: substituir heurísticas em `AIOrchestrator` por chamadas LLM.
- Google/Meta Ads: trocar `ads_mock.py` por SDK oficial e webhooks de métricas.
- WhatsApp/Email: integrar Twilio/360Dialog + provedor SMTP/Resend.

## Qualidade

```bash
pytest
```
