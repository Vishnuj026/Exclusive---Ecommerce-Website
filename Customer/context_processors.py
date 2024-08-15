from Marketing.models import Logo, SocialMedia, Homepageslideshowbanner
from Merchant.models import Review, Category, Product, Merchantgtsdetail
from Customer.models import FavoriteProduct
from .searchengine import SearchForm


def Customer(request):

    products = Product.objects.all()
    if request.user.is_authenticated:
        favorite_products = FavoriteProduct.objects.filter(
            user=request.user
        ).values_list("product_id", flat=True)
    else:
        favorite_products = []
    is_merchant = False
    if request.user.is_authenticated:
        is_merchant = Merchantgtsdetail.objects.filter(
            MerchantName=request.user
        ).exists()
    return {"products": products, "is_favorite_products": favorite_products, "is_merchant" : is_merchant}


def Marketing(request):
    logo_instance = Logo.objects.first()
    social_media_links = SocialMedia.objects.all()
    slideshow_banners = Homepageslideshowbanner.objects.all()

    return {
        "logo": logo_instance,
        "slideshow_banners": slideshow_banners,
        "social_media_links": social_media_links,
    }


def Merchant(request):
    category_list = Category.objects.all()

    return {"category_list": category_list}


def search(request):
    form = SearchForm()

    return {'SearchForm': form}



def currency(request):
    currency = request.currency

    return {'currency': currency,}