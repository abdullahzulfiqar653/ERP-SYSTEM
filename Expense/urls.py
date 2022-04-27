from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet
from pprint import pprint
router = DefaultRouter()

router.register('expense', ExpenseViewSet, basename='expense')

pprint(router.urls)

urlpatterns = router.urls
