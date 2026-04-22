from app.db.schemas import DiagnosisCreate


def generate_landing_page(data: DiagnosisCreate) -> dict:
    headline = f'{data.specialty}: aumente agendamentos em {data.city_region} com previsibilidade.'
    subheadline = (
        f'Plano orientado por IA para clínicas com ticket médio de R$ {data.average_ticket:,.2f}. '
        'Diagnóstico, tráfego e conversão no mesmo lugar.'
    )
    return {
        'headline': headline,
        'subheadline': subheadline,
        'sections': [
            {'title': 'Prova social', 'content': 'Resultados mensuráveis com foco em ROI e faturamento.'},
            {'title': 'Serviços', 'content': data.main_services},
            {'title': 'Diferenciais', 'content': data.key_differentials},
            {'title': 'CTA', 'content': 'Quero aumentar minha receita com previsibilidade'},
        ],
        'conversion_elements': ['CTA fixo no topo', 'Formulário simplificado', 'Botão WhatsApp 1-clique'],
    }
