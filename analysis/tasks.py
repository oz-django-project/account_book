from celery import shared_task
from datetime import date, timedelta

from accounts.models import TransactionHistory
from analysis.ai import generate_ai_summary
from django.contrib.auth import get_user_model
from analysis.models import Analysis

User = get_user_model()

@shared_task
def run_weekly_analysis(user_id):
    # 순환 참조 방지
    from analysis.analyzers import Analyzer
    user = User.objects.get(id=user_id)

    today = date.today()
    start_date = today - timedelta(days=7)
    end_date = today

    results = []

    for about in ['expense', 'income']:
        analyzer = Analyzer(
            user=user,
            about=about,
            analysis_type='weekly',
            start_date=start_date,
            end_date=end_date
        )
        analysis = analyzer.run()
        if analysis:
            results.append(analysis.id)

    return results  # 분석 ID 리스트 반환

@shared_task
def run_monthly_category_analysis(user_id):
    from analysis.analyzers import Analyzer
    user = User.objects.get(id=user_id)

    # ⏱ 지난달의 시작일과 종료일 계산
    today = date.today()
    first_day_of_this_month = date(today.year, today.month, 1)
    last_day_of_last_month = first_day_of_this_month - timedelta(days=1)
    first_day_of_last_month = date(last_day_of_last_month.year, last_day_of_last_month.month, 1)

    # 분석 실행
    analyzer = Analyzer(
        user=user,
        about='expense',  # 또는 'income'도 가능
        analysis_type='monthly-category',
        start_date=first_day_of_last_month,
        end_date=last_day_of_last_month
    )
    analysis = analyzer.run()
    return analysis.id if analysis else None

@shared_task
def generate_ai_summary_for_analysis(analysis_id):
    from .models import Analysis
    from .ai import generate_ai_summary

    analysis = Analysis.objects.get(id=analysis_id)

    # 거래내역 불러오기
    transactions = TransactionHistory.objects.filter(
        account__user=analysis.user,
        transaction_type=...,
        created_at__date__gte=analysis.period_start,
        created_at__date__lte=analysis.period_end,
    )

    if not transactions.exists():
        analysis.summary = "분석 가능한 거래 내역이 없습니다."
        analysis.save()
        return

    # contents 생성
    contents = [
        {
            "role": "user",
            "parts": [
                {
                    "text": f"{t.created_at.date()} {t.amount}원 {t.category} {t.description}"
                }
            ],
        }
        for t in transactions
    ]

    # AI 요약 호출
    response = generate_ai_summary(contents)

    analysis.summary = response.text
    analysis.save()
