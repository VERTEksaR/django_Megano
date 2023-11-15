from django.urls import path

from authentication.views import (
    sign_up,
    sign_in,
    sign_out,
)
from editing_profile.views import (
    ProfileAPIView,
    ChangePasswordView,
    ChangeAvatarView,
)

from tags.views import (
    TagsAPIView,
)

from catalog.views import (
    CategoriesAPIView,
    CatalogAPIList,
    PopularAPIView,
    LimitedAPIView,
    BannersAPIView,
    SalesAPIList,
)

from products.views import (
    ProductsAPIView,
    ReviewAPIView,
)

from basket.views import (
    BasketAPIView,
)

from orders.views import (
    OrderAPIView,
    OneOrderAPIView,
)

from payment.views import (
    payment,
)

app_name = 'api'


urlpatterns = [
    path('sign-up', sign_up),
    path('sign-in', sign_in),
    path('sign-out', sign_out),

    path('profile', ProfileAPIView.as_view()),
    path('profile/password', ChangePasswordView.as_view()),
    path('profile/avatar', ChangeAvatarView.as_view()),

    path('tags', TagsAPIView.as_view()),

    path('categories', CategoriesAPIView.as_view()),
    path('catalog', CatalogAPIList.as_view()),
    path('products/popular', PopularAPIView.as_view()),
    path('products/limited', LimitedAPIView.as_view()),
    path('banners', BannersAPIView.as_view()),
    path('sales', SalesAPIList.as_view()),

    path('product/<int:id>', ProductsAPIView.as_view()),
    path('product/<int:id>/reviews', ReviewAPIView.as_view()),

    path('basket', BasketAPIView.as_view()),

    path('orders', OrderAPIView.as_view()),
    path('order/<int:id>', OneOrderAPIView.as_view()),

    path('payment/<int:id>', payment),
]
