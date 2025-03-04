from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .forms import CheckoutContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User


def home(request):
    products_images = ProductImage.objects.filter(is_active=True, is_main=True)

    return render(request, 'landing/home.html', {'products_images': products_images})


    selected_shop = request.session.get('selected_shop', 1)  # По умолчанию первый магазин
    products = Product.objects.filter(shop__id=selected_shop)  # Фильтруем товары по магазину



def about(request):
    return render(request, 'landing/about.html')

def adresses(request):
    return render(request, 'landing/adresses.html')

def change_shop(request):
    if request.method == "POST":
        shop_id = request.POST.get("shop_id")
        request.session['selected_shop'] = shop_id  # Сохраняем выбор магазина в сессии
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

def product(request, product_id):
    product1 = Product.objects.get(id=product_id)

    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    print(request.session.session_key)
    # print(product1)

    return render(request, 'products/product.html', {'product1': product1})

def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    print (request.POST)
    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        ProductInBasket.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                                     is_active=True, defaults={"nmb": nmb})
        if not created:
            print ("not created")
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    #common code for 2 cases
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb

    return_dict["products"] = list()

    for item in  products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb
        return_dict["products"].append(product_dict)

    return JsonResponse(return_dict)


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    print (f'товары - {products_in_basket}')
    for item in products_in_basket:
        print(f'заказ - {item.order}')


    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        print(request.POST)
        if form.is_valid():
            print("yes")
            data = request.POST
            print(data)
            name = data.get("name", "default_name")
            surname = data.get("surname", "default_surname")
            email = data.get("email", "default@email.com")
            phone = data["phone"]
            #user, created = User.objects.get_or_create(username=phone, defaults={"first_name": name, "last_name": surname, "email": email})

            order = Order.objects.create(customer_name=name, customer_surname=surname, customer_phone=phone, customer_email=email, status=Status.objects.get(id=2))

            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    product_in_basket_id = name.split("product_in_basket_")[1]
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)

                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    ProductInOrder.objects.create(
                        product=product_in_basket.product,
                        nmb=product_in_basket.nmb,
                        price_per_item=product_in_basket.price_per_item,
                        total_price=product_in_basket.total_price,
                        order=order
                    )

            print()
            print(f'sessia - {request.session}')

            # Очистка корзины после переноса товаров в заказ
            request.session.flush()

        #     # Перенаправляем пользователя обратно
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        # else:
        #     print("no")
    return render(request, 'orders/checkout.html', locals())

@receiver(post_save, sender=Order)
def send_status_update_email(sender, instance, created, **kwargs):
    # Если заказ был обновлен, а не только создан
    print(f'instance - {instance}')
    print(f'created - {created}')
    if not created:
        # Проверяем, изменился ли статус на нужный
        if instance.status.name == "ready" and not instance.status_changed:
            # Отправляем письмо
            send_mail(
                subject=f"Ваш заказ #{instance.id} готов к оплате на кассе",
                message=f"Здравствуйте! Ваш заказ #{instance.id} готов к оплате на кассе.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.customer_email],
                fail_silently=False,
            )