from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.models import TransactionHistory

from .analyzers import Analyzer
from .models import Analysis
from .serializers import AnalysisCreateSerializer, AnalysisSerializer


class AnalysisListView(ListAPIView):
    serializer_class = AnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        analysis_type = self.request.query_params.get("type", None)

        queryset = Analysis.objects.filter(user=user)

        if analysis_type in ["weekly", "monthly"]:
            queryset = queryset.filter(type=analysis_type)

        return queryset.order_by("-created_at")  # 최신순 정렬


class AnalysisCreateView(CreateAPIView):
    queryset = TransactionHistory.objects.none()
    serializer_class = AnalysisCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Analysis.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        analyzer = Analyzer(
            user=request.user,
            about=data["about"],
            analysis_type=data["type"],
            start_date=data["start_date"],
            end_date=data["end_date"],
        )

        result = analyzer.run()
        if result is None:
            return Response(
                {"message": "분석 가능한 거래 내역이 없습니다."}, status=204
            )

        result.refresh_from_db()

        response_serializer = AnalysisSerializer(result, context={"request": request})
        return Response(response_serializer.data, status=201)
