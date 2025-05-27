from rest_framework import serializers

from lessons.models import Grade
from goals.models import Goal, Icon, FieldOfStudy, PurposeChoices, StudyHoursChoices, RankRangeChoices, IconTypeChoices
import logging

logger = logging.getLogger(__name__)


class GoalSerializer(serializers.ModelSerializer):
    purpose_icon = serializers.SerializerMethodField()
    study_hours_icon = serializers.SerializerMethodField()
    grade = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all())  # ✅ Allows grade input

    class Meta:
        model = Goal
        fields = [
            "id",
            "field_of_study",
            "study_hours_icon",
            "grade",
            "purpose",
            "purpose_icon",
            "from_rank_range",
            "to_rank_range",
            "study_hours",
            "average_eleventh",
            "average_tenth",
        ]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)

    def get_purpose_icon(self, obj):
        return obj.get_purpose_icon()

    def get_study_hours_icon(self, obj):
        return obj.get_study_hours_icon()


class GoalChoicesSerializer(serializers.Serializer):

    def get_icon(self, icon_type, choice_value):
        """Fetch icon URL based on type and choice value, with logging."""
        try:
            icon = Icon.objects.filter(
                icon_type=icon_type,
                choice_value=choice_value
            ).first()

            if icon and icon.icon:
                icon_url = icon.icon.url
                logger.info(f"Found icon for {icon_type} - {choice_value}: {icon_url}")
                return icon_url  # Returns media URL

            logger.warning(f"No icon found for {icon_type} - {choice_value}")
            return None

        except Exception as e:
            logger.error(f"Error retrieving icon for {icon_type} - {choice_value}: {e}")
            return None

    def to_representation(self, instance):
        """Manually structure the serializer output to avoid using SerializerMethodField."""
        return {
            "field_of_study": [
                {"value": choice[0], "label": choice[1]}
                for choice in FieldOfStudy.choices
            ],
            "purpose": [
                {
                    "value": choice[0],
                    "label": choice[1],
                    "icon": self.get_icon(IconTypeChoices.PURPOSE.value, choice[0]),
                }
                for choice in PurposeChoices.choices
            ],
            "study_hours": [
                {
                    "value": choice[0],
                    "label": choice[1],
                    "icon": self.get_icon(IconTypeChoices.STUDY_HOURS.value, choice[0]),
                }
                for choice in StudyHoursChoices.choices
            ],
            "rank_range": [
                {"value": choice[0], "label": choice[1]}
                for choice in RankRangeChoices.choices
            ]
        }
