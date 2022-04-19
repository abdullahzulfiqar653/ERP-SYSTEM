from rest_framework.routers import DefaultRouter
from .views import InoviceViewSet
# from pprint import pprint
router = DefaultRouter()

router.register('invoice', InoviceViewSet, basename='Invoice')

# pprint(router.urls)

urlpatterns = router.urls
