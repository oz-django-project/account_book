import matplotlib

matplotlib.use("Agg")
from datetime import date, timedelta
from io import BytesIO

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from accounts.models import TransactionHistory

from .models import Analysis
from .tasks import generate_ai_summary_for_analysis

User = get_user_model()

# 한글 깨짐 방지 (macOS용)
plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False


class Analyzer:
    def __init__(
        self,
        user: User,
        about: str,
        analysis_type: str,
        start_date: date,
        end_date: date,
    ):
        self.user = user
        self.about = about.lower()
        self.analysis_type = analysis_type
        self.start_date = start_date
        self.end_date = end_date

    def run(self):
        transaction_type = self._map_about_to_transaction_type()
        df = self._get_dataframe(transaction_type)

        if df.empty:
            return None

        if self.analysis_type == "monthly-category":
            df_grouped = self._aggregate_by_category(df)
            image = self._visualize_category(df_grouped)
        elif self.analysis_type == "weekly":
            df_grouped = self._aggregate_by_day(df)
            image = self._visualize_weekly(df_grouped)
        else:
            raise ValueError("Invalid analysis_type")

        return self._save_analysis(df_grouped, image)

    def _map_about_to_transaction_type(self):
        return {"expense": "WITHDRAW", "income": "DEPOSIT"}.get(self.about, self.about)

    def _get_dataframe(self, transaction_type):
        queryset = TransactionHistory.objects.filter(
            account__user=self.user,
            transaction_type=transaction_type,
            created_at__date__range=(self.start_date, self.end_date),
        ).values("created_at", "amount", "category")

        if not queryset.exists():
            return pd.DataFrame()

        df = pd.DataFrame.from_records(queryset)
        df["created_at"] = pd.to_datetime(df["created_at"]).dt.tz_localize(None)
        df.set_index("created_at", inplace=True)
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        return df.sort_index()

    def _aggregate_by_day(self, df):
        return df.resample("D").sum()

    def _aggregate_by_category(self, df):
        return df.groupby("category")["amount"].sum().sort_values(ascending=False)

    def _get_user_display_name(self):
        return getattr(self.user, "username", None) or getattr(
            self.user, "email", "사용자"
        )

    def _korean_label(self):
        type_map = {"weekly": "주간", "monthly-category": "월간 카테고리별"}
        about_map = {
            "expense": "소비",
            "income": "수입",
            "withdraw": "소비",
            "deposit": "수입",
            "WITHDRAW": "소비",
            "DEPOSIT": "수입",
        }
        return f"{type_map.get(self.analysis_type, self.analysis_type)} {about_map.get(self.about, self.about)}"

    def _visualize_weekly(self, df_grouped):
        fig, ax = plt.subplots(figsize=(10, 5))

        ax.plot(df_grouped.index, df_grouped["amount"], marker="o")
        ax.set_title(f"{self._get_user_display_name()}의 {self._korean_label()} 분석")
        ax.set_xlabel("날짜")
        ax.set_ylabel("금액")
        ax.grid(True)

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        fig.autofmt_xdate()

        if self.start_date == self.end_date:
            ax.set_xlim(
                self.start_date - timedelta(days=1), self.end_date + timedelta(days=1)
            )
        else:
            ax.set_xlim(self.start_date, self.end_date)

        plt.tight_layout()
        buf = BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        plt.close(fig)
        return buf

    def _visualize_category(self, df_grouped):
        fig, ax = plt.subplots(figsize=(10, 5))

        category_labels = {
            "food": "식비",
            "transport": "교통",
            "entertainment": "여가",
            "shopping": "쇼핑",
            "saving": "저축",
            "etc": "기타",
        }

        labels = [category_labels.get(cat, cat) for cat in df_grouped.index]
        x = range(len(labels))  # 카테고리 위치 지정

        bars = ax.bar(x, df_grouped.values, width=0.3, edgecolor="none")
        ax.set_ylabel("금액")
        ax.set_xlabel("카테고리")
        ax.set_title(
            f"{self._get_user_display_name()}의 월간 카테고리별 {self._korean_label().split()[-1]} 분석"
        )
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=0)
        ax.grid(False)

        plt.tight_layout()
        buf = BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        plt.close(fig)
        return buf

    def _save_analysis(self, df_grouped, image_buf):
        result = Analysis(
            user=self.user,
            about=self.about,
            type=self.analysis_type,
            period_start=self.start_date,
            period_end=self.end_date,
            description=f"{self._get_user_display_name()}의 {self._korean_label()} 분석 결과입니다.",
        )
        filename = f"{self.about}_{self.analysis_type}_{self.start_date}.png"
        result.result_image.save(filename, ContentFile(image_buf.read()), save=True)
        image_buf.close()

        generate_ai_summary_for_analysis.delay(result.id)
        return result
