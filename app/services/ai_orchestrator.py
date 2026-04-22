from app.db.models import PhysicianLevel
from app.db.schemas import DiagnosisCreate


class AIOrchestrator:
    """Camada de IA com fallback mock para produção inicial."""

    @staticmethod
    def classify_level(data: DiagnosisCreate) -> PhysicianLevel:
        if data.average_ticket >= 1800 and data.schedule_capacity_weekly >= 35:
            return PhysicianLevel.avancado
        if data.average_ticket >= 900:
            return PhysicianLevel.intermediario
        return PhysicianLevel.iniciante

    @staticmethod
    def business_diagnosis(data: DiagnosisCreate, level: PhysicianLevel) -> dict:
        strengths = [
            f'Especialidade {data.specialty} com proposta de valor em {data.city_region}',
            f'Ticket médio de R$ {data.average_ticket:,.2f}',
        ]
        bottlenecks = []
        if data.current_roi is None or data.current_roi < 2:
            bottlenecks.append('ROI baixo ou não monitorado em mídia paga')
        if data.schedule_capacity_weekly < 20:
            bottlenecks.append('Baixa capacidade de agenda para ganho de escala')

        opportunities = [
            'Captar demanda de alta intenção com Google Ads local',
            'Escalar Meta Ads com criativos de prova social',
            'Implantar fluxo de follow-up em 5 tentativas + nutrição',
        ]
        return {
            'level': level.value,
            'strengths': strengths,
            'weaknesses': bottlenecks or ['Processo comercial sem padronização clara'],
            'priority_opportunities': opportunities,
        }

    @staticmethod
    def generate_action_plan(summary: dict, data: DiagnosisCreate) -> dict:
        return {
            'short_term_0_30_dias': [
                'Criar landing page com CTA para WhatsApp',
                'Subir campanha Google Search com palavras de fundo de funil',
                'Configurar CRM com pipeline e SLA de atendimento < 5 min',
            ],
            'mid_term_31_90_dias': [
                'Implementar campanha Meta com lookalike de pacientes convertidos',
                'Automatizar follow-up multicanal (WhatsApp + email)',
                'Otimizar taxa de comparecimento por lembretes automáticos',
            ],
            'long_term_90_plus_dias': [
                'Estratégia de recorrência e reativação de base',
                'SEO local para termos transacionais na região',
                'Teste de novas ofertas com IA para copy e criativos',
            ],
            'estimated_impact': {
                'leads_growth': '20-45%',
                'conversion_gain': '10-25%',
                'roi_target': '2.5x-5x',
            },
            'diagnostic_reference': summary,
            'profile': {
                'physician': data.physician_name,
                'specialty': data.specialty,
                'region': data.city_region,
            },
        }
