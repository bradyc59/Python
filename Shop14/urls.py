from django.urls import path, include
from . import views
from .forms import UserLoginForm
from.models import CaUser, Product
from rest_framework import routers, serializers, viewsets
from rest_framework.authtoken.views import obtain_auth_token

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CaUser
        fields = ['url', 'username', 'email', 'is_staff']

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'picture']

class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = []
    permission_classes = []


class UserViewset(viewsets.ModelViewSet):
    queryset = CaUser.objects.all()
    serializer_class = UserSerializer


router = routers.DefaultRouter()
router.register(r'users', UserViewset)
router.register(r'products', ProductViewset)

urlpatterns = [
    path('', views.index, name="index"),
    path('singleproduct/<int:prodid>', views.single_product, name="single_product"),
    path('all_product/', views.all_product, name="all_product"),
    path('myform/', views.myform),
    path('user_signup/', views.CaUserSignupView.as_view(), name="user_signup"),
    path('admin_signup/', views.AdminSignupView.as_view(), name="admin_signup"),
    path('login/', views.Login.as_view(template_name="login.html", authentication_form=UserLoginForm), name='login'),
    path('logout/', views.logout_view, name="logout"),
    path('basket/', views.get_basket, name='basket'),
    path('addbasket/<int:prodid>', views.add_to_basket, name='add_to_basket'),
    path('removebasketitem/<int:sbi>', views.remove_from_basket, name="remove_from_basket"),
    path('checkout/', views.order_form, name="checkout"),
    path('contactus/', views.contact_us, name="contact_us"),
    path('api/', include(router.urls)),
    path('token/', obtain_auth_token, name='api_token_auth')
]
