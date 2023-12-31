from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from shop.views import CategoryAPIViewset, ProductViewset, ArticleViewset, \
    AdminCategoryViewset, AdminArticleViewset

router = routers.SimpleRouter()
# Puis lui déclarons une url basée sur le mot clé ‘category’ et notre view
# afin que l’url générée soit celle que nous souhaitons ‘/api/category/’
router.register('category', CategoryAPIViewset, basename='category')
router.register('product', ProductViewset, basename='product')
router.register('article', ArticleViewset, basename='article')
# nouvel url d'admin pour cette fois créer une category
router.register('admin/category', AdminCategoryViewset, basename='admin-category')
# nouvel url d'admin pour cette fois créer un article
router.register('admin/article', AdminArticleViewset, basename='admin-article')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls))
]
