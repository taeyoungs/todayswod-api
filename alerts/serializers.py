from rest_framework import serializers
from .models import Alert


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = (
            "id",
            "updated",
            "alert_type",
            "title",
            "content",
            "user",
            "box",
        )
        read_only_fields = (
            "id",
            "created",
            "updated",
            "user",
            "box",
        )

    # serializer를 통해서 알림을 생성하는건 박스 주인이 생성하는 알림 밖에 없음
    # 회원권 만료 알림은 serializer가 아닌 model manager를 통해서 생성
    def create(self, validated_data):

        request = self.context.get("request")
        alert = Alert.objects.create(**validated_data, box=request.user.box)
        return alert