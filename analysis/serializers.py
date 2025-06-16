from rest_framework import serializers
from .models import Analysis

class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = [
            'id',
            'about',
            'type',
            'period_start',
            'period_end',
            'description',
            'summary',
            'result_image',
            'created_at',
            'updated_at',
        ]

        read_only_fields = ['summary', 'result_image']

class AnalysisCreateSerializer(serializers.Serializer):
    about = serializers.ChoiceField(choices=["income", "expense"])
    type = serializers.ChoiceField(choices=["weekly", "monthly-category"])
    start_date = serializers.DateField()
    end_date = serializers.DateField()