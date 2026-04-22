from app.db.models import PipelineStage


def generate_followup_sequence(patient_name: str) -> list[dict]:
    messages = [
        f'Oi {patient_name}, temos horários disponíveis esta semana. Posso te ajudar com o agendamento?',
        f'{patient_name}, passando para lembrar da sua avaliação. Quer que eu reserve o melhor horário?',
        f'{patient_name}, última chamada para sua condição especial desta semana.',
        f'{patient_name}, seguimos com agenda aberta. Posso confirmar em 2 minutos pelo WhatsApp?',
        f'{patient_name}, encerrando seu atendimento ativo. Posso mover para lista de conteúdos e ofertas?',
    ]
    return [
        {'attempt': index + 1, 'channel': 'whatsapp' if index < 3 else 'email', 'message': msg}
        for index, msg in enumerate(messages)
    ]


def stage_after_followup(converted: bool) -> PipelineStage:
    return PipelineStage.agendamento if converted else PipelineStage.nutricao
