from rest_framework import serializers
from .models import Project, Task
from datetime import date

# Serializers for the Project and Task models, used to convert data
# to and from JSON for API requests and responses.

from rest_framework import serializers
from .models import Project, Task
from datetime import date

class TaskSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), required=True
    )

    class Meta:
        model = Task
        fields = "__all__"
        depth = 1

    # single‑field rule 
    def validate_start_date(self, value):
        today = date.today()

        # creating
        if self.instance is None and value < today:
            raise serializers.ValidationError(
                "Start date cannot be in the past."
            )

        # editing
        proj = self.instance.project if self.instance else None
        if proj and value < proj.created_at.date():
            raise serializers.ValidationError(
                "Start date cannot be before the project’s creation date."
            )

        return value

    # cross‑field rules
    def validate(self, attrs):
        start = attrs.get("start_date") or getattr(self.instance, "start_date", None)
        due   = attrs.get("due_date")   or getattr(self.instance, "due_date", None)
        status = attrs.get("status") or getattr(self.instance, "status", None)

        errors = {}

        if start and due and due <= start:
            # attach error to **due_date** so the UI can highlight that field
            errors["due_date"] = "Due date must be after start date."

        if due and due < date.today() and status != "done":
            errors["due_date"] = (
                'This task is overdue — mark it "Done" or update the due date.'
            )

        # project‑start rule for **create** when only project id is supplied
        if self.instance is None and "project" in self.initial_data:
            try:
                proj = Project.objects.get(pk=self.initial_data["project"])
                if start and start < proj.created_at.date():
                    errors["start_date"] = (
                        "Start date cannot be before the project’s creation date."
                    )
            except Project.DoesNotExist:
                pass  # FK validation will handle bad IDs

        if errors:
            # field‑wise dict raises become per‑field messages in the response
            raise serializers.ValidationError(errors)

        return attrs


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)  # Include related tasks

    class Meta:
        model = Project
        fields = '__all__'
        