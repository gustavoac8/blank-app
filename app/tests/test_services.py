from fastapi.testclient import TestClient

from app.db.schemas import DiagnosisCreate
from app.main import app
from app.services.ai_orchestrator import AIOrchestrator


client = TestClient(app)


def test_health():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_classification_and_plan():
    payload = DiagnosisCreate(
        physician_name='Dra Teste',
        specialty='Estética',
        average_ticket=2000,
        schedule_capacity_weekly=40,
        city_region='Curitiba',
        key_differentials='diferencial',
        main_services='servicos',
        marketing_history='historico',
        current_roi=1.5,
    )
    level = AIOrchestrator.classify_level(payload)
    assert level.value == 'avancado'
    summary = AIOrchestrator.business_diagnosis(payload, level)
    plan = AIOrchestrator.generate_action_plan(summary, payload)
    assert 'short_term_0_30_dias' in plan
    assert plan['estimated_impact']['roi_target']
