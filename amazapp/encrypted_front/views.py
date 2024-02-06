# from my_project.example.models import Profile
# from rest_framework.renderers import TemplateHTMLRenderer
# from rest_framework.response import Response
# from rest_framework.views import APIView
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from rest_framework.decorators import action

from .models import File, Folder, EncryptionUser
from .serializers import FileSerializer, FolderSerializer, EncryptionUserSerializer

# class ProfileList(APIView):
#     renderer_classes = [TemplateHTMLRenderer]
#     template_name = 'profile_list.html'

#     def get(self, request):
#         queryset = Profile.objects.all()
#         return Response({'profiles': queryset})


class EncryptionUserViewSet(ModelViewSet):

    queryset = EncryptionUser.objects.all()
    serializer_class = EncryptionUserSerializer


    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        encryption_user = EncryptionUser.objects.select_related('user').get(
            user_id=request.user.id)
        if request.method == 'GET':
            serializer = EncryptionUserSerializer(encryption_user)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = EncryptionUserSerializer(encryption_user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)








    # queryset = EncryptionUser.objects.all()
    # def get_queryset(self):
    # #     # queryset = EncryptionUser.objects.filter(
    # #     #     user_id=self.request.user.id).select_related('user')
    # #     # print(list(EncryptionUser.objects.filter(
    # #     #     user_id=self.request.user.id).select_related('user').values_list('id', 'key', 'user' ,'user__username')))
    # #         # .values('id', 'key', 'user__id',)
    # #     # print(queryset)
    #     return EncryptionUser.objects.filter(
    #         user_id=self.request.user.id).select_related('user')


class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer


    def get_serializer_context(self):
        return {'folder_id': self.kwargs['folder_pk']}
    # search_fields = ['name']
    # ordering_fields = ['name']

    # def get_serializer_context(self):
    #     return {'request': self.request}


class FolderViewSet(ModelViewSet):
    # queryset = Folder.objects.annotate(
    #     files_count=Count('files')).all()
    queryset = Folder.objects.prefetch_related('files').all()
    
    serializer_class = FolderSerializer

    def destroy(self, request, *args, **kwargs):
        if File.objects.filter(folder_id=kwargs['pk']):
            return Response({'error': 'Folder cannot be deleted because it includes one or more Files.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)
