$(document).ready(function(){
    var form = $('#form_buying_product');
    console.log(form);

    // Маска для телефона
    $('input[type="tel"]').inputmask("+7 (999) 999-99-99");

    // Валидация email
    $('input[type="email"]').inputmask({
        alias: "email"
    });

    $('#shopToggle').change(function() {
        let shop_id = $(this).is(':checked') ? 2 : 1; // Определяем магазин
        $.ajax({
            url: "{% url 'change_shop' %}", // Делаем AJAX-запрос
            type: "POST",
            data: { shop_id: shop_id, csrfmiddlewaretoken: '{{ csrf_token }}' },
            success: function(response) {
                location.reload(); // Обновляем страницу, чтобы обновился ассортимент
            }
        });
    });


    function basketUpdating(product_id, nmb, is_delete){
        var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();  // Получаем CSRF-токен глобально
        var data = {
            product_id: product_id,
            nmb: nmb,
            csrfmiddlewaretoken: csrf_token
        };

        if (is_delete){
            data["is_delete"] = true;
        }

        console.log(data)

        $.ajax({
            url: "/basket_adding/",  // Указываем URL вручную, а не из формы
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log("Товар добавлен!");
                $('#basket_total_nmb').text("(" + data.products_total_nmb + ")");
                $('.basket-items ul').html("");
                $.each(data.products, function(k, v){
                    $('.basket-items ul').append('<li>'+ v.name+', ' + v.nmb + 'шт. ' + 'по ' + v.price_per_item + '₽  ' +
                        '<a class="delete-item" href="" data-product_id="'+v.id+'">🗑</a>'+
                        '</li>');
                });
            },
            error: function () {
                console.log("Ошибка добавления товара");
            }
        });
    }

    $(document).on('click', '.btn-buy', function(e){
        e.preventDefault();  // Отменяем стандартное поведение кнопки

        var product_id = $(this).data("product_id");
        var name = $(this).data("name");
        var price = $(this).data("price");
        var nmb = $(this).data("nmb") || 1;  // Если data-nmb не указано, ставим 1

        basketUpdating(product_id, nmb, false);  // Вызываем функцию добавления в корзину
    });

    function showingBasket() {
    $('.basket-items').removeClass('hidden');
    }

    function hidingBasket() {
    setTimeout(function() {
        if (!$('.basket-container:hover').length && !$('.basket-items:hover').length) {
            $('.basket-items').addClass('hidden');
        }
    }, 100); // Задержка, чтобы дать время на переход
    }

    // Открываем корзину при наведении
    $('.basket-container').on('mouseenter', function() {
    showingBasket();
    });

    // Закрываем корзину, когда мышь уходит
    $('.basket-container, .basket-items').on('mouseleave', function() {
    hidingBasket();
    });

    // Если кликнули вне корзины — закрываем
    $(document).click(function(event) {
        if (!$(event.target).closest('.basket-container').length) {
            hidingBasket();
        }
    });

     $(document).on('click', '.delete-item', function(e){
         e.preventDefault();
         product_id = $(this).data("product_id")
         nmb = 0;
         basketUpdating(product_id, nmb, is_delete=true)
     });

    function calculatingBasketAmount(){
        var total_order_amount = 0;
        $('.total-product-in-basket-amount').each(function() {
            total_order_amount = total_order_amount + parseFloat($(this).text());
        });
        console.log(total_order_amount);
        $('#total_order_amount').text(total_order_amount.toFixed(2));
    };

    $(document).on('change', ".product-in-basket-nmb", function(){
        var current_nmb = $(this).val();
        console.log(current_nmb);

        var current_tr = $(this).closest('tr');
        var current_price = parseFloat(current_tr.find('.product-price').text()).toFixed(2);
        console.log(current_price);
        var total_amount = parseFloat(current_nmb*current_price).toFixed(2);
        console.log(total_amount);
        current_tr.find('.total-product-in-basket-amount').text(total_amount);

        calculatingBasketAmount();
    });


    calculatingBasketAmount();

});