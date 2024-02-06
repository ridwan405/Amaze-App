
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
# router.register('', views.EncryptionUserViewSet, basename='users')
router.register('folders', views.FolderViewSet, basename='folders')


folders_router = routers.NestedDefaultRouter(
    router, 'folders', lookup='folder')
folders_router.register('files', views.FileViewSet,
                        basename='folder-files')

# URLConf
urlpatterns = router.urls + folders_router.urls
