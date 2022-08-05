from app.models import Element, ElementManager
from app.serializers import ElementSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


class ElementView(APIView):
    permission_classes = [permissions.AllowAny,]

    def get(self, request, slug):
        element = Element.objects.all()
        for i in element:
            i.children = i.string_from_string()
        serializer = ElementSerializer(element, many = True)
        return Response(serializer.data)

    def post(self, request,slug):
        element = request.data.get('element')
        element['children'] = []
        if (type(element['parent_id']) is int and element['parent_id'] > 0):
            if Element.objects.filter(pk=element['parent_id']).exists():
                if Element.objects.get(pk=element['parent_id']).company_id == element['company_id']:
                    serializer = ElementSerializer(data = element)
                    if serializer.is_valid(raise_exception=True):
                        element_saved = serializer.save()
                    return Response({"id":"{}".format(element_saved.id),
                                     "parent_id":"{}".format(element_saved.parent_id.id),
                                     "href":"{}".format(element_saved.href),
                                     "label":"{}".format(element_saved.label),
                                     "team_id": "{}".format(element_saved.team_id),
                                     "company_id": "{}".format(element_saved.company_id),
                                     "company_name":"{}".format(element_saved.company_name)
                                })
                else: return Response({
                    "Родительский элемент не принадлежит этой компании"
                })
            else:
                return Response({
                    "Элемент с таким родительским id'{}' не существует"
                })
        else: return Response({
                    "Parent_id должен иметь тип данных int и быть больше 0"
                })

    def put(self, request, pk, slug):
        if Element.objects.filter(pk = pk).exists():
            saved_element = Element.objects.get(pk = pk)
            data = request.data.get('element')
            if pk == 1:
                serializer = ElementSerializer(instance=saved_element, data=data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    saved_element = serializer.save()
                return Response({
                    "Элемент с id'{}' успешно изменен".format(saved_element.id)
                })
            elif (type(data['parent_id']) is int and data['parent_id'] > 0):
                if Element.objects.filter(pk = data['parent_id']).exists():
                    if saved_element in Element.objects.filter(pk = data['parent_id']):
                        return Response({
                            "Родителем элемента не может быть сам элемент"
                        })
                    else:
                        if Element.objects.get(pk=data['parent_id']).company_id != data['company_id']:
                            return Response({
                                "Родительский элемент не принадлежит этой компании"
                            })
                        else:
                            serializer = ElementSerializer(instance=saved_element, data=data, partial=True)
                            if serializer.is_valid(raise_exception=True):
                                saved_element = serializer.save()
                            return Response({
                                "Элемент с id'{}' успешно изменен".format(saved_element.id)
                            })

                else:return Response({
                        "Элемент с таким родительским id'{}' не существует"
                    })
            else:
                return Response({
                    "Parent_id должен иметь тип данных int и быть больше 0"
                })
        else: return Response("Элемент с “id”: '{}' не существует, запрос не был выполнен".format(pk), status = 404)

    def delete(self, request, pk, slug):
        try:
            element = Element.objects.get(pk = pk)
            if element.id != 1:
                element.children_list_delete()
                element.delete()
                return Response({
                    "Элемент с id'{}' удален".format(pk)
                })
            else: return Response({
                    "Элемент с id=1 нельзя удалить"})
        except Element.DoesNotExist:
            return Response("Элемент с “id”: '{}' не существует, запрос не был выполнен".format(pk), status=404)






