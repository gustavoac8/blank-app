from random import randint, uniform


class AdsIntegratorMock:
    @staticmethod
    def create_campaign(channel: str, name: str, budget_daily: float) -> dict:
        return {
            'external_id': f'{channel[:2].upper()}-{randint(10000, 99999)}',
            'channel': channel,
            'name': name,
            'budget_daily': budget_daily,
            'status': 'active',
            'metrics': {
                'impressions': randint(4000, 18000),
                'clicks': randint(90, 700),
                'leads': randint(10, 90),
                'cpl': round(uniform(15, 120), 2),
                'roi': round(uniform(1.1, 4.8), 2),
            },
        }

    @staticmethod
    def optimize_budget(metrics: dict, current_budget: float) -> float:
        roi = metrics.get('roi', 1)
        if roi >= 3:
            return round(current_budget * 1.15, 2)
        if roi < 1.8:
            return round(current_budget * 0.9, 2)
        return current_budget
