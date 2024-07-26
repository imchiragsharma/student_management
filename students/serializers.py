from rest_framework import serializers
from .models import Student, Parent

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['id', 'parent_name', 'parent_phone_number']

class StudentSerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(write_only=True)
    parent_phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = Student
        fields = ['id', 'student_name', 'student_phone_number', 'class_name', 'parent_name', 'parent_phone_number', 'class_teacher_name', 'chemistry', 'physics', 'math']

    def create(self, validated_data):
        parent_name = validated_data.pop('parent_name')
        parent_phone_number = validated_data.pop('parent_phone_number')
        
        parent, created = Parent.objects.get_or_create(
            parent_phone_number=parent_phone_number,
            defaults={'parent_name': parent_name}
        )
        
        student = Student.objects.create(parent=parent, **validated_data)
        return student

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['parent'] = ParentSerializer(instance.parent).data
        return representation
