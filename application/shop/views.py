from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django import views
from .models import Brand, Article, Customer, CartProduct, Notification
from .forms import LoginForm, RegistrationForm
from .mixins import CartMixin, NotificationsMixin
from .utils import recalc_cart


class BaseView(CartMixin, NotificationsMixin, views.View):

    def get(self, request, *args, **kwargs):
        # articles = Article.objects.all().order_by('-id')[:5]
        articles = Article.objects.all()
        context = {
            'articles': articles,
            'cart': self.cart,
            'notifications': self.notifications(request.user)
        }
        return render(request, 'base.html', context)


class BrandDetailView(views.generic.DetailView):

    model = Brand
    template_name = 'brand/brand_detail.html'
    slug_url_kwarg = 'brand_slug'
    context_object_name = 'brand'


class ArticleDetailView(views.generic.DetailView):

    model = Article
    template_name = 'article/article_detail.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'


class LoginView(views.View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'login.html', context)


class RegistrationView(views.View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'registration.html', context)


class AccountView(CartMixin, views.View):

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        wish = Customer.objects.prefetch_related('wishlist')
        for item_wish in wish:
            f = item_wish.wishlist.all()
            name_art = [article.name for article in item_wish.wishlist.all()]
            print(f)

        list_sp = [wish_i.wishlist.all() for wish_i in wish]
        print(list_sp)

        context = {
            'customer': customer,
            'cart': self.cart,
            'wish': wish,
            'f': f,
            # 'list_sp': list_sp[4]
        }
        return render(request, 'account.html', context)


class CartView(CartMixin, views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'cart.html', {"cart": self.cart})


class AddToCardView(CartMixin, views.View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner,
            cart=self.cart,
            content_type=content_type,
            object_id=product.id
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно добавлен")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class DeleteFromCartView(CartMixin, views.View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner,
            cart=self.cart,
            content_type=content_type,
            object_id=product.id
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар удален")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ChangeQTYView(CartMixin, views.View):
    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner,
            cart=self.cart,
            content_type=content_type,
            object_id=product.id
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Изменено")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class AddToWishlist(views.View):

    @staticmethod
    def get(request, *args, **kwargs):
        article = Article.objects.get(id=kwargs['article_id'])
        customer = Customer.objects.get(user=request.user)
        customer.wishlist.add(article)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ClearNotificationsView(views.View):

    @staticmethod
    def get(request, *args, **kwargs):
        Notification.objects.make_all_read(request.user.customer)
        return HttpResponseRedirect(request.META['HTTP_REFERER'])














