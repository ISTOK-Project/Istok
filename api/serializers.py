from rest_framework import serializers
from Istok_app.models import (Furniture, Tags, Purpose, Description, ProjectImage, News, Order)
from rest_framework.response import Response
from rest_framework import status


class TagsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label="ID объекта", read_only=True, required=False)

    class Meta:
        model = Tags
        fields = ['id', 'name', 'highlight']


class PurposeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label="ID объекта", read_only=True, required=False)

    class Meta:
        model = Purpose
        fields = ['id', 'name']


class ProjectImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label="ID объекта", read_only=True, required=False)

    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'image_medium', 'image_small', 'only_one_image']


class ProjectImageCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label="ID объекта", read_only=True, required=False)

    class Meta:
        model = ProjectImage
        fields = ['id', 'image']


class ChoiceField(serializers.ChoiceField):
    """Для отображения читаемой переменной из полей с прописанным выбором модели Furniture"""
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class ListFurnitureSerializer(serializers.ModelSerializer):
    type = ChoiceField(choices=Furniture.TYPES)
    form = ChoiceField(choices=Furniture.FORMS)
    style = ChoiceField(choices=Furniture.STYLES)
    body_material = ChoiceField(choices=Furniture.MATERIAL)
    facades_material = ChoiceField(choices=Furniture.MATERIAL)
    tabletop_material = ChoiceField(choices=Furniture.MATERIAL)

    class Meta:
        model = Furniture
        fields = ['id', 'name', 'type', 'form', 'style', 'body_material', 'facades_material',
                  'tabletop_material', 'price', 'text', 'tags', 'purposes', 'images']
        depth = 1  # для полного отображения моделей M2M


class NewsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ['id', 'title', 'text', 'time_created', 'image']



class ListOrdersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'number', 'create_date', 'shipment_date', 'status', 'address', 'contract', 'images']
        depth = 1  # для полного отображения моделей M2M









#todo разобраться с валидациями

# class ListFurnitureSerializer(serializers.Serializer):
#     id = serializers.IntegerField(label="ID объекта", read_only=True, required=False)
#
#     name = serializers.CharField(max_length=100, label='Название', help_text='Не более 100 символов')
#     type = serializers.ChoiceField(choices=Furniture.TYPES, default='1', label='Тип мебели')
#
#     form = serializers.ChoiceField(choices=Furniture.FORMS, default='1', label='Форма мебели')
#     style = serializers.ChoiceField(choices=Furniture.STYLES, default='1', label='Стиль мебели')
#     body_material = serializers.ChoiceField(choices=Furniture.MATERIAL, default='1',
#         label='Материал корпуса')
#     facades_material = serializers.ChoiceField(choices=Furniture.MATERIAL, default='1',
#         label='Материал фасадов')
#     tabletop_material = serializers.ChoiceField(choices=Furniture.MATERIAL, default='1',
#         label='Материал столешницы')
#     price = serializers.IntegerField(default=0, label='Стоимость', min_value=0)
#     text = serializers.CharField(label='Описание')
#
#     tags = TagsSerializer(many=True, read_only=True)
#     purposes = PurposeSerializer(many=True, read_only=True)
#     images = ProjectImageSerializer(many=True, read_only=True)


    ####
    # пример автозаполнения поля создателя
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    ####






    # @staticmethod
    # def create_image(kwargs):
    #     try:
    #         new_project_image = ProjectImage.objects.create(**kwargs)
    #         return new_project_image
    #     except Exception as e:
    #         mess = f"ERROR!:{e}\nFrom: ListFurnitureSerializer.create_image" \
    #                f"\nkwargs=={kwargs}"
    #         print(mess)
    #         return None


    # def create(self, validated_data):
    #     tags = self.initial_data.get('tags', None)
    #     purposes = self.initial_data.get('purposes', None)
    #     images = self.initial_data.get('images', None)
    #     try:
    #         new = Furniture.objects.create(**validated_data)
    #         # if tags or tags == []:
    #         if tags:
    #             try:
    #                 tags_id_list = [obj['id'] for obj in tags]
    #                 new.tags.set(tags_id_list)
    #             except Exception as e:
    #                 mess = f"ERROR!:{e}\nFrom: ListFurnitureSerializer.create" \
    #                        f"\ntags=={tags}\nvalidated_data=={validated_data}"
    #                 new.delete()
    #                 print(mess)
    #                 return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #         # if purposes or purposes == []:
    #         if purposes:
    #             try:
    #                 purposes_id_list = [obj['id'] for obj in purposes]
    #                 new.purposes.set(purposes_id_list)
    #             except Exception as e:
    #                 mess = f"ERROR!:{e}\nFrom: ListFurnitureSerializer.create" \
    #                        f"\ntags=={purposes}\nvalidated_data=={validated_data}"
    #                 new.delete()
    #                 print(mess)
    #                 return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #         if images:
    #             try:
    #                 images_id_list = [obj['id'] for obj in images]
    #                 print('images_id_list == ', images_id_list)
    #                 new.images.set(images_id_list)
    #             except Exception as e:
    #                 mess = f"ERROR!:{e}\nFrom: ListFurnitureSerializer.create" \
    #                        f"\nimages=={images}"
    #                 new.delete()
    #                 print(mess)
    #                 return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #
    #         # if images:
    #         #     print('images == ', images)
    #         #     images_id = []
    #         #     for kwargs in images:
    #         #         new_project_image = self.create_image(kwargs)
    #         #         if new_project_image:
    #         #             images_id.append(new_project_image.pk)
    #         #
    #         #     print('images_id == ', images_id)
    #         #     new.images.set(images_id)
    #         #     print(new.images.set().all())
    #
    #
    #     except Exception as e:
    #         mess = f"ERROR!:{e}\nvalidated_data=={validated_data}"
    #         print(mess)
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     return new


    # def update(self, instance, validated_data):
    #     tags = self.initial_data.get('tags', None)
    #     purposes = self.initial_data.get('purposes', None)
    #
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.type = validated_data.get("type", instance.type)
    #     instance.form = validated_data.get("form", instance.form)
    #     instance.form = validated_data.get("style", instance.style)
    #     instance.body_material = validated_data.get("body_material", instance.body_material)
    #     instance.facades_material = validated_data.get("facades_material", instance.facades_material)
    #     instance.tabletop_material = validated_data.get("tabletop_material", instance.tabletop_material)
    #     instance.price = validated_data.get("price", instance.price)
    #     # instance.image_1 = validated_data.get("image_1", instance.image_1)
    #     # instance.image_2 = validated_data.get("image_2", instance.image_2)
    #     # instance.image_3 = validated_data.get("image_3", instance.image_3)
    #     # instance.image_4 = validated_data.get("image_4", instance.image_4)
    #     instance.text = validated_data.get("text", instance.text)
    #
    #     if tags or tags == []:
    #         try:
    #             tags_id_list = [obj['id'] for obj in tags]
    #             instance.tags.set(tags_id_list)
    #         except Exception as e:
    #             mess = f"ERROR!:{e}\ninstance=={instance}\nvalidated_data=={validated_data}\n"
    #             print(mess)
    #             return Response(status=status.HTTP_400_BAD_REQUEST)
    #     if purposes or purposes == []:
    #         try:
    #             purposes_id_list = [obj['id'] for obj in purposes]
    #             instance.purposes.set(purposes_id_list)
    #         except Exception as e:
    #             mess = f"ERROR!:{e}\ninstance=={instance}\nvalidated_data=={validated_data}\n"
    #             print(mess)
    #             return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     try:
    #         # todo в дальнейшем для таких неизвестных ошибок, задать функцию рассылки админам на email.
    #         instance.save()
    #     except Exception as e:
    #         mess = f"ERROR!:{e}\ninstance=={instance}\nvalidated_data=={validated_data}\n"
    #         print(mess)
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     # print(new.images.values_list(flat=True))
    #
    #     return instance






















#
# # Проверяем, равен ли набор тегов у существующего объекта, новому списку тегов из PUT запроса.
# # Так-же для правильного сравнения, оба варианта преобразуем в упорядоченный список картежей.
# tags = validated_data.get("tags", None)
# #todo переделать по https://www.youtube.com/watch?v=4ThiXOWyea0&list=PLA0M1Bcd0w8yU5h2vwZ4LO7h1xt8COUXl
# if tags:
#     sorted_list = sorted([(tag.pk, tag.tag)for tag in set(tags)])
#     if sorted(list(instance.tags.all().order_by('pk').values_list())) != sorted_list:
#         FurnitureTags.objects.filter(finished_furniture=instance).delete()
#         for tag in validated_data.get("tags"):
#             try:
#                 FurnitureTags.objects.create(furniture=instance, tag=tag)
#             except Exception as e:
#
#                 print(f"\nНеизвестная ошибка при создании таблицы отношений!!"
#                       f"\ninstance == {instance}"
#                       f"\ntag == {tag}"
#                       f"\nError=={e}")
#                 pass
# instance.save()
















