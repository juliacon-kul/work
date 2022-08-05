from rest_framework import serializers
from app.models import Element, ElementManager
from django.utils.text import slugify

def children(value):
    s = value
    l = len(s)
    integ = []
    i = 0
    while i < l:
        s_int = ''
        a = s[i]
        while '0' <= a <= '9':
            s_int += a
            i += 1
            if i < l:
                a = s[i]
            else:
                break
        i += 1
        if s_int != '':
            integ.append(int(s_int))
    return integ
class IdField(serializers.RelatedField):
    def to_representation(self, value):
        return str(value)

class ElementSerializer(serializers.ModelSerializer):
    id = IdField(read_only=True)
    children = serializers.ListField(allow_empty=True)

    class Meta:
        model = Element
        fields = ('id','href',
                  'parent_id', 'label', 'children', 'team_id', 'company_id', 'company_name','slug')

    def create(self, validated_data):
        element = Element.objects.create_element(**validated_data)
        return element


    def update(self, instance, validated_data):
        if instance.id == 1:
            instance.label = validated_data.get('label', instance.label)
            instance.href = validated_data.get('href', instance.href)
            instance.team_id = validated_data.get('team_id',instance.team_id)
            instance.company_id = validated_data.get('company_id', instance.company_id)
            instance.company_name = validated_data.get('company_name', instance.company_name)

            instance.save()
        else:

            if instance.parent_id != validated_data.get('parent_id'):
                    instance.children_list_delete()
                    instance.label = validated_data.get('label', instance.label)
                    instance.href = validated_data.get('href', instance.href)
                    instance.parent_id = validated_data.get('parent_id', instance.parent_id)
                    instance.team_id = validated_data.get('team_id', instance.team_id)
                    instance.company_id = validated_data.get('company_id', instance.company_id)
                    instance.company_name = validated_data.get('company_name', instance.company_name)
                    instance.save()
                    instance.children_list_update()
            else:
                instance.label = validated_data.get('label', instance.label)
                instance.href = validated_data.get('href', instance.href)
                instance.parent_id = validated_data.get('parent_id', instance.parent_id)
                instance.team_id = validated_data.get('team_id', instance.team_id)
                instance.company_id = validated_data.get('company_id', instance.company_id)
                instance.company_name = validated_data.get('company_name', instance.company_name)
                instance.save()

        return instance







