from django.contrib.auth.models import User, Group
from collections import OrderedDict
from django.db.models import Q
from quickstart.models import Advice
from quickstart.serializers import UserSerializer, GroupSerializer, AdviceSerializer, \
    AdviceCreateSerializer, AdviceRetriveUpdateSerializer, AdviceUserSerializer
from quickstart.permissions import CanModerateAdvices
from quickstart.filters import AdviceFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import viewsets, status, permissions
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
import json
from history.models import History
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.utils import translation


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


def create_in_history(user_id, advice_id, advice_data):
    fields_json = json.dumps(
        {'advice': advice_data}, ensure_ascii=False
    )
    History.objects.create(
        user_id=user_id,
        action=History.ADD_FLAG,
        date=timezone.now(),
        content_type=ContentType.objects.get_for_model(Advice),
        object_id=advice_id,
        fields_json=fields_json
    )


def save_post_edit_history(user_id, advice_id, changes):
    if changes:
        record = {'post': changes}
        History.objects.create(
            user_id=user_id,
            action=History.EDIT_FLAG,
            date=timezone.now(),
            content_type=ContentType.objects.get_for_model(Advice),
            object_id=advice_id,
            fields_json=json.dumps(record, ensure_ascii=False),
        )


class AdvicePagination(PageNumberPagination):
    page_size = 10
    page_sizer_query_param = 'paginate_by'
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response(
            OrderedDict([
                ('last_page', self.page.paginator.num_pages),
                *list(data.items()),
            ])
        )


def get_advices(r):
    advices = Advice.objects.all()
    return [{
        'id': advice.id,
        'name': advice.name,

    } for advice in advices]


def get_changes(before, after):
    changes = {}
    for key, value_after in after.items():
        value_before = before and before.get(key)
        if value_after != value_before:
            changes[key] = value_after
    return changes


class AdviceViewSet(viewsets.ModelViewSet):
    serializer_class = AdviceSerializer
    permission_classes = (CanModerateAdvices,)
    pagination_class = AdvicePagination
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'is_published']

    def initial(self, request, *args, **kwargs):
        language = kwargs.get('lang')
        translation.activate(language)
        super(AdviceViewSet, self).initial(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in ['create']:
            return AdviceCreateSerializer
        if self.action in ['retrieve', 'partial_update']:
            return AdviceRetriveUpdateSerializer
        return AdviceSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        prev_data = self.get_serializer(instance).data
        is_publish = instance.is_published
        data = request.data.copy()
        # if not request.data.get('office'):
        #     data.update({'office':  None})
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        advice = serializer.data
        # if (not is_publish) and advice['is_published']:
        #     notify_new_advice.delay(advice['author'], advice['id'])

        changes = get_changes(prev_data, advice)
        save_post_edit_history(request.user.id, instance.id, changes)
        return Response(advice)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        create_in_history(
            request.user.id,
            serializer.data['id'],
            {k: serializer.data[k] for k in serializer.data}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        advice = self.get_object()

        # if request.user != advice.author:
        #     notify_delete_advice.delay(advice.author.email, context)
        self.perform_destroy(advice)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        data = dict()
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            advice = self.get_serializer(page, many=True).data
        else:
            advice = self.get_serializer(queryset, many=True).data
        data['advices'] = advice
        if request.user:
            data['current_user'] = AdviceUserSerializer(request.user).data
        return self.get_paginated_response(data)

    def get_queryset(self):
        if self.request.user.has_perm('advice.moderate_advices'):
            return Advice.objects.all().order_by('is_published')
        return Advice.objects.all()

    @action(methods=['GET'], detail=False)
    def get_data(self, request, **kwargs):
        data = dict()
        data['info'] = 'тут можем вернуть какие-то данные'
        return Response(data)

    @action(methods=['POST'], detail=True)
    def publish(self, request, **kwargs):
        advice = self.get_object()
        is_published = json.loads(request.POST.get('is_published'))
        if is_published:
            advice.is_published = True
            # if request.user != advice.author:
            #     notify_publish_advice.delay(advice.author.id, advice.id)
        else:
            advice.is_published = False
        advice.save()
        return Response()


