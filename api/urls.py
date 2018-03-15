from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
#from users.viewsets	import * 
#from products.viewsets import * 
from django.conf.urls import (
handler400, handler403, handler404, handler500
)

#handler400 = 'my_app.views.bad_request'
#handler403 = 'my_app.views.permission_denied'

handler404 = 'shopkeepers.views.page_not_found'
handler500 = 'shopkeepers.views.server_error' 

#router = DefaultRouter()
#router.register(r'users/register/pre', UsersViewsets)
#router.register(r'shopkeepers/', include('shopkeepers.urls'))

#router.register(r'products/category', CategoryViewsets)
#router.register(r'products/subcategory', SubcategoryViewsets)
#router.register(r'products/products', ProductFullViewsets)

urlpatterns = [
    url(r'^v2/asociado/t1/', admin.site.urls),
    url(r'^users/', include('users.urls')),
    url(r'^engineer/', include('engineer.urls')),
    url(r'^task/', include('task.urls')),
    url(r'^login/', obtain_jwt_token),
    url(r'^v2/token-refresh/', refresh_jwt_token),
    url(r'^v2/token-verify/', verify_jwt_token),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
