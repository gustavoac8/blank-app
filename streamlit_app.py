import json

import requests
import streamlit as st

st.set_page_config(page_title='Domina Receita Médica', page_icon='🩺', layout='wide')

st.title('🩺 Domina Receita Médica')
st.caption('Orquestrador SaaS de aquisição + conversão + retenção para clínicas médicas')

api_url = st.sidebar.text_input('URL da API', 'http://localhost:8000')
token = st.sidebar.text_input('Token Bearer', type='password')
headers = {'Authorization': f'Bearer {token}'} if token else {}

col1, col2, col3, col4, col5 = st.columns(5)
for col, metric in zip(
    [col1, col2, col3, col4, col5],
    ['Leads gerados', 'Taxa conversão', 'CPL', 'ROI', 'Faturamento estimado'],
):
    col.metric(metric, '—')

if st.button('Atualizar Dashboard'):
    if not token:
        st.warning('Informe o token para consultar métricas.')
    else:
        resp = requests.get(f'{api_url}/dashboard', headers=headers, timeout=10)
        if resp.ok:
            data = resp.json()
            col1.metric('Leads gerados', data['leads_gerados'])
            col2.metric('Taxa conversão', f"{data['taxa_conversao']}%")
            col3.metric('CPL', f"R$ {data['custo_por_lead']}")
            col4.metric('ROI', f"{data['roi']}x")
            col5.metric('Faturamento estimado', f"R$ {data['faturamento_estimado']}")
        else:
            st.error(resp.text)

st.divider()
st.subheader('Módulo 1: Diagnóstico Inteligente')
with st.form('diagnostico'):
    c1, c2 = st.columns(2)
    physician_name = c1.text_input('Nome do médico(a)', 'Dra. Exemplo')
    specialty = c2.text_input('Especialidade', 'Medicina Estética')
    avg_ticket = c1.number_input('Ticket médio', min_value=100.0, value=1200.0, step=50.0)
    capacity = c2.number_input('Capacidade semanal de agenda', min_value=1, value=25)
    city = c1.text_input('Cidade/Região', 'São Paulo/SP')
    diff = c2.text_area('Diferenciais', 'Tecnologia, protocolos exclusivos, alto índice de satisfação')
    services = c1.text_area('Serviços principais', 'Preenchimento, bioestimulador, harmonização')
    history = c2.text_area('Histórico de marketing', 'Campanhas esporádicas em Meta Ads')
    roi = c1.number_input('ROI atual (opcional)', min_value=0.0, value=0.0, step=0.1)
    submit = st.form_submit_button('Gerar diagnóstico + plano')

if submit:
    payload = {
        'physician_name': physician_name,
        'specialty': specialty,
        'average_ticket': avg_ticket,
        'schedule_capacity_weekly': capacity,
        'city_region': city,
        'key_differentials': diff,
        'main_services': services,
        'marketing_history': history,
        'current_roi': roi if roi > 0 else None,
    }
    if not token:
        st.warning('Informe token para enviar ao backend.')
    else:
        diag = requests.post(f'{api_url}/diagnosis', json=payload, headers=headers, timeout=15)
        plan = requests.get(f'{api_url}/plans/latest', headers=headers, timeout=15)
        if diag.ok:
            st.success('Diagnóstico gerado com sucesso!')
            st.json(diag.json())
        else:
            st.error(diag.text)
        if plan.ok:
            st.subheader('Plano de ação automático')
            st.json(plan.json())

st.divider()
st.subheader('Módulos 3-7 (Landing, Ads, CRM, Follow-up e Pós-venda)')
st.info('Todos os módulos estão disponíveis via API REST e integração mock para Google Ads/Meta/IA.')
st.code(
    """POST /landing/generate
POST /campaigns
POST /crm/patients
PATCH /crm/patients/{id}/stage
POST /crm/patients/{id}/follow-up"""
)

st.download_button('Exportar visão do produto', data=json.dumps({'produto': 'Domina Receita Médica'}, indent=2), file_name='domina-receita-medica.json')
