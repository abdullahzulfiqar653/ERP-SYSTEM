from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, PurchaseViewSet, AssetViewSet
# from pprint import pprint
router = DefaultRouter()

router.register('expense', ExpenseViewSet, basename='expense')
router.register('purchase', PurchaseViewSet, basename='purchase')
router.register('asset', AssetViewSet, basename='asset')

# pprint(router.urls)

urlpatterns = router.urls
