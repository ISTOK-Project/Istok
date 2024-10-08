from rest_framework import serializers
from Istok_app import models
from users import models as users_models
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseForbidden, HttpResponseBadRequest



#### Exceptions
class SurveyEditException(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Проверьте наличие и правильность вводимых полей'
#### Exceptions


class TagsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(label="ID объекта", read_only=True, required=False)

    class Meta:
        model = models.Tags
        fields = ['id', 'name', 'highlight']


# class ProjectImageSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(label="ID объекта", read_only=True, required=False)
#
#     class Meta:
#         model = models.ProjectImage
#         fields = ['id', 'image', 'image_medium', 'image_small', 'only_one_image']


# class ProjectImageCreateSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(label="ID объекта", read_only=True, required=False)
#
#     class Meta:
#         model = models.ProjectImage
#         fields = ['id', 'image']


class FurnitureListSerializer(serializers.ModelSerializer):
    # recommendations = ExtraFurnitureListSerializer(read_only=True, many=True)

    class Meta:
        model = models.Furniture
        fields = ['id', 'category', 'name', 'tags', 'text', 'price', 'images',
                  'model_3d', 'time_created']
        depth = 1  # для полного отображения моделей M2M

    # def to_representation(self, instance):
    #
    #     print('def to_representation\n')
    #     ret = super(FurnitureListSerializer, self).to_representation(instance)
    #     recommendations = self.instance.recommendations.all()
    #     default_rec_len = recommendations.count()
    #     lack_of_rec = 3 - default_rec_len
    #     if lack_of_rec <= 0:
    #         ret['recommendations'] = ExtraFurnitureListSerializer(recommendations, many=True).data
    #     if lack_of_rec > 0:
    #         auto_recommendations = self.instance.get_similar(num=lack_of_rec)
    #         recommendations = recommendations.union(auto_recommendations)
    #         ret['recommendations'] = ExtraFurnitureListSerializer(recommendations.order_by('-id'), many=True).data
    #
    #     return ret


class ExtraFurnitureListSerializer(serializers.ModelSerializer):
    recommendations = FurnitureListSerializer(read_only=True, many=True)

    class Meta:
        model = models.Furniture
        fields = ['id', 'category', 'name', 'tags', 'text', 'price', 'images',
                  'model_3d', 'time_created', 'recommendations']
        depth = 1  # для полного отображения моделей M2M



class NewsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.News
        fields = ['id', 'title', 'text', 'time_created', 'image']


class OrdersListSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = ['id', 'number', 'create_date', 'shipment_date', 'status', 'address', 'contract', 'images']
        depth = 1  # для полного отображения моделей M2M


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Application
        fields = ['id', 'time_created', 'user', 'text', 'last_name', 'first_name', 'patronymic', 'phone',
                  'contact_type', 'link', 'date_time', 'python_date_time']
        # depth = 1  # для полного отображения моделей M2M



#### Сериализаторы Опросника
class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Option
        fields = ['id', 'text', 'user_input']


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(read_only=True, many=True)

    class Meta:
        model = models.Question
        fields = ['id', 'text', 'multy_choice', 'options']
        depth = 1  # для полного отображения моделей M2M


class ExtraQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Question
        fields = ['id', 'text']


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Answer
        fields = ['text', 'user_answer']


class QuestionAndAnswerSerializer(serializers.ModelSerializer):
    question = ExtraQuestionSerializer(read_only=False, many=False)
    answers = AnswerSerializer(read_only=False, many=True)

    class Meta:
        model = models.QuestionAndAnswer
        fields = ['id', 'question', 'answers']
        depth = 1  # для полного отображения моделей M2M


class SurveySerializer(serializers.ModelSerializer):
    question_and_answers = QuestionAndAnswerSerializer(read_only=True, many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    dependable = serializers.BooleanField(required=True, label='Опросник надежен',
        help_text='Статус становится положительным в случае если опросник заполняли '
                  'больше минимального времени заполнения. При аналитике ненадежные будут вычеркиваться из выборки')

    class Meta:
        model = models.Survey
        fields = ['user', 'questions_was_changed', 'dependable', 'question_and_answers']
        # depth = 1  # для полного отображения моделей M2M

    def to_representation(self, instance):
        ret = super(SurveySerializer, self).to_representation(instance)
        question_and_answers = instance.questionandanswer_set.all()
        ret['question_and_answers'] = QuestionAndAnswerSerializer(question_and_answers, many=True).data
        return ret

    def create(self, validated_data):
        user = self.validated_data.pop('user')

        try:
            dependable = validated_data.pop('dependable')
            instance = models.Survey.objects.create(user=user, dependable=dependable)
            question_and_answers = self.initial_data.pop('question_and_answers')
        except Exception:
            raise Http404("Возможные ошибки:\n"
                          "Опросник данного пользователя уже существует.\n"
                          "Отсутствует поле question_and_answers.\n"
                          "Отсутствует поле dependable.")

        for obj in question_and_answers:
            answers = []
            for answer_obj in obj['answers']:
                try:
                    text = answer_obj['text']
                    if not text:
                        raise Http404

                    user_answer = answer_obj['user_answer']
                except Exception:
                    raise Http404('Проверьте наличие полей text, user_answer')

                answer_lst = models.Answer.objects.filter(text=text)
                if answer_lst.exists():
                    new_answer = answer_lst.first()
                else:
                    new_answer = models.Answer.objects.create(text=text, user_answer=user_answer)
                answers.append(new_answer)

            try:
                question_id = obj['question']['id']
            except Exception:
                raise Http404('Отсутствует ключ question, id у answers')


            new = models.QuestionAndAnswer.objects.filter(survey=instance, question=question_id)
            if new.exists():
                new = new.first()
                new.answers.set(answers)
            else:
                new = models.QuestionAndAnswer.objects.create(survey=instance, question_id=obj['question']['id'])
                new.answers.set(answers)

        return instance


    def update(self, instance, validated_data):

        try:
            dependable = validated_data.pop('dependable')
            models.Survey.objects.update(dependable=dependable)
            question_and_answers = self.initial_data.pop('question_and_answers')
        except Exception:
            raise Http404("Возможные ошибки: "
                          "Отсутствует поле question_and_answers. "
                          "Отсутствует поле dependable.")

        for obj in question_and_answers:
            answers = []
            for answer_obj in obj['answers']:

                try:
                    text = answer_obj['text']
                    if not text:
                        raise Http404

                    user_answer = answer_obj['user_answer']
                except Exception:
                    raise Http404('Проверьте наличе полей text, user_answer у answers')

                answer_lst = models.Answer.objects.filter(text=text)
                if answer_lst.exists():
                    new_answer = answer_lst.first()
                else:
                    new_answer = models.Answer.objects.create(text=text, user_answer=user_answer)
                answers.append(new_answer)

            if not answers:
                raise Http404("Проверьте наличие поля answers")
            try:
                question_id = obj['question']['id']
            except Exception:
                raise Http404('Отсутствует ключ question или id у question_and_answers')

            new = models.QuestionAndAnswer.objects.filter(survey=instance, question=question_id)
            if new.exists():
                new = new.first()
                new.answers.set(answers)
            else:
                print('instance == ', instance)
                new = models.QuestionAndAnswer.objects.create(survey=instance, question_id=question_id)
                new.answers.set(answers)

        return instance

        
        

        
    
    
#### Сериализаторы Опросника


#### Loyalty Benefit Offer(User_app)
class BenefitSerializer(serializers.ModelSerializer):

    class Meta:
        model = users_models.Benefit
        fields = ['id', 'title', 'about']


class OfferSerializer(serializers.ModelSerializer):

    class Meta:
        model = users_models.Offer
        fields = ['id', 'title', 'about', 'offer_to_all']



class LoyaltySerializer(serializers.ModelSerializer):

    class Meta:
        model = users_models.Loyalty
        fields = ['user_id', 'card_number', 'show_user_name', 'balance', 'balance_history', 'code', 'benefits_history',
                  'offers', 'new_benefits_count', 'benefit_to_choose']
        depth = 1

    def to_representation(self, instance):
        ret = super(LoyaltySerializer, self).to_representation(instance)
        offer_to_all = users_models.Offer.objects.filter(offer_to_all=True)
        ret['offers'] = ret['offers'] + OfferSerializer(offer_to_all, many=True).data
        ret['all_benefits'] = BenefitSerializer(users_models.Benefit.objects.all(), many=True).data

        return ret


class LoyaltyBenefitSerializer(serializers.ModelSerializer):
    # loyalty = LoyaltySerializer(read_only=True, many=False)
    # benefit = BenefitSerializer(read_only=True, many=False)

    class Meta:
        model = users_models.LoyaltyBenefit
        fields = ['id', 'benefit']
        # depth = 1

#### Loyalty Benefit (User_app)


#### WebsiteSettings

class WebsiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WebsiteSettings
        fields = ['name', 'min_write_time']
        depth = 1


#### WebsiteSettings










# class LoyaltySerializer(serializers.ModelSerializer):
#     question_and_answers = QuestionAndAnswerSerializer(read_only=True, many=True)
#
#     # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
#
#     class Meta:
#         model = models.Survey
#         fields = ['id', 'user', 'balance' 'bonus' 'balance' 'balance' 'balance' 'balance' 'balance']
#         # depth = 1  # для полного отображения моделей M2M



    # {
    #     "user": 1,
    #     "question_and_answers": [
    #         {
    #             "question": 1,
    #             "answers": [
    #                 {"text": "Диван", "user_answer": false},
    #                 {"text": "Кровать", "user_answer": false},
    #                 {"text": "Свой вариант", "user_answer": true}
    #             ]
    #         },
    #
    #         {
    #             "question": 3,
    #             "answers": [
    #                 {"text": "Реклама в интернете", "user_answer": false},
    #                 {"text": "Я его создаю", "user_answer": true}
    #             ]
    #         }
    #     ]
    # }

    # def to_representation(self, instance):
    #     representation = super(EquipmentSerializer, self).to_representation(instance)
    #     representation['assigment'] = AssignmentSerializer(instance.assigment_set.all(), many=True).data
    #     return representation

#### Сериализаторы Опросника





##!! Пример использования своего класса для отображения выбора
# class ChoiceField(serializers.ChoiceField):
#     """Для отображения читаемой переменной из полей с прописанным выбором модели Furniture"""
#     def to_representation(self, obj):


  
#         if obj == '' and self.allow_blank:
#             return obj
#         return self._choices[obj]
#
#     def to_internal_value(self, data):
#         if data == '' and self.allow_blank:
#             return ''
#
#         for key, val in self._choices.items():
#             if val == data:
#                 return key
#         self.fail('invalid_choice', input=data)

# class FurnitureListSerializer(serializers.ModelSerializer):
#     type = ChoiceField(choices=Furniture.TYPES)
#     form = ChoiceField(choices=Furniture.FORMS)
#     style = ChoiceField(choices=Furniture.STYLES)
#     body_material = ChoiceField(choices=Furniture.MATERIAL)
#     facades_material = ChoiceField(choices=Furniture.MATERIAL)
#     tabletop_material = ChoiceField(choices=Furniture.MATERIAL)
#
#     class Meta:
#         model = Furniture
#         fields = ['id', 'name', 'type', 'form', 'style', 'body_material', 'facades_material',
#                   'tabletop_material', 'price', 'text', 'tags', 'purposes', 'images']
#         depth = 1  # для полного отображения моделей M2M





# class FurnitureListSerializer(serializers.Serializer):
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


##!!
# пример автозаполнения поля создателя
# user = serializers.HiddenField(default=serializers.CurrentUserDefault())
##!!






    # @staticmethod
    # def create_image(kwargs):
    #     try:
    #         new_project_image = ProjectImage.objects.create(**kwargs)
    #         return new_project_image
    #     except Exception as e:
    #         mess = f"ERROR!:{e}\nFrom: FurnitureListSerializer.create_image" \
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
    #                 mess = f"ERROR!:{e}\nFrom: FurnitureListSerializer.create" \
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
    #                 mess = f"ERROR!:{e}\nFrom: FurnitureListSerializer.create" \
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
    #                 mess = f"ERROR!:{e}\nFrom: FurnitureListSerializer.create" \
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
















