$(document).ready(function(){
    // add to wishlist
    $('.add-wishlist').on('click', function() {
        var _product_id = $(this).attr('data-product');
        var _btn = $(this)

        if ($(this).attr('data-type')=='detail') {
            
            $.ajax({
                url: '/shop/add_wishlist',
                data: {
                    product: _product_id
                },
                dataType: 'json',
                success: function(response) {
                    if (response.bool) {
                        _btn.html('<i class="me-1 fa fa-heart fa-lg text-danger" aria-hidden="true"></i> Удалить из избранного').change()
                    } else {
                        _btn.html('<i class="me-1 fa fa-heart fa-lg" aria-hidden="true"></i> В избранное').change()
                    };
                },
                error: function(xhr, textStatus, errorThrown) {
                    console.error('Ошибка. Не удалось добавить/удалить из избранного', errorThrown)
                }
            });

        } else {
        
            $.ajax({
                url: "/shop/add_wishlist",
                data : {
                    product: _product_id
                },
                dataType: 'json',
                success: function(response){
                    if (response.bool) {
                        _btn.prop('title', 'Удалить из избарнного');
                        _btn.addClass("text-danger");
                    } else {
                        _btn.prop('title', 'Добавить в избарнное');
                        _btn.removeClass("text-danger");
                    };
                },
                error: function(xhr, textStatus, errorThrown) {
                    console.error('Ошибка. Не удалось добавить/удалить из избранного', errorThrown)
                }
            });
        }
    });
    // end wishlist

    // add likes/dislikes
    $('.like-btn').on('click', function() {
        var _post_id = $(this).attr('data-post');
        var _btn = $(this)

        $.ajax({
            url: '/like',
            data: {
                post_id: _post_id
            },
            dataType: 'json',
            success: function(response) {
                if (response.bool) {
                    _btn.prop('title', 'Убрать лайк')
                    _btn.addClass('text-danger')
                    
                } else {
                    _btn.prop('title', 'Поставить лайк')
                    _btn.removeClass('text-danger')
                };
            },
            error: function(xhr, textStatus, errorThrown) {
                console.error('Ошибка. Не удалось поставить лайк/дизлайк', errorThrown)
            }
        });
    });
    // end likes

    // gallery
    const thumbnails = $('.thumbnail-image');
    let currentIndex = 0;
    const mainImage = $('.main-image');
    const overlayImage = $('.overlay-image');
    const overlay = $('.overlay');

    // Открыть изображение на весь экран
    function showImage(index) {

        mainImage.attr('src', thumbnails.eq(index).attr('src'));
        overlayImage.attr('src', thumbnails.eq(index).attr('src'));
        overlay.addClass('open');
    };

    // По клику по большому изображению
    $('.main-image').on('click', function() {
        showImage(currentIndex)
    });

    // Закрыть отрытое изображение
    $('.overlay').on('click', function(event) {
        if (!$(event.target).hasClass('carousel-control-prev-icon') && !$(event.target).hasClass('carousel-control-next-icon') ) {
            $(this).removeClass('open');
        }
    });

    // Подставить thumnail на место болшьшой картинки
    $('.thumbnail-image').each(function(index) {
        $(this).on('click', function() {
            const mainImage = $('.main-image')
            mainImage.attr('src', $(this).attr('src'))

            thumbnails.removeClass('border border-4 border-warning');
            thumbnails.eq(index).addClass('border border-4 border-warning');

            currentIndex = index
        });

    });

    // Кнопка влево
    $('.carousel-control-prev-icon').on('click', function() {
        currentIndex --;
        if (currentIndex < 0) {
            currentIndex = thumbnails.length-1;
        }
        showImage(currentIndex);
    });

    // Кнопка вправо
    $('.carousel-control-next-icon').on('click', function(){
        currentIndex ++ ;
        if (currentIndex > thumbnails.length-1) {
            currentIndex = 0;
        }
        showImage(currentIndex)
    });

    // end gallery

    function changeQuantity(btn, input, type) {
        let currentValue = input.val();

        if (!isNaN(currentValue)) {
            if (type=='plus') {
                if (currentValue < parseInt(input.attr('max'), 10)) {
                    currentValue ++;
                    input.val(currentValue).change();
                }
                if (currentValue == parseInt(input.attr('max'), 10)) {
                    btn.addClass('disabled');
                    console.log('OOOOOOOOOOO')
                }
            } else if (type=='minus') {
                if (currentValue > parseInt(input.attr('min'), 10)) {
                    currentValue --;
                    input.val(currentValue).change();
                }
                if (currentValue == parseInt(input.attr('min'), 10)) {
                    btn.addClass('disabled');
                }
            }
        }
    };


    // quantity input
    $('.btn-number').click(function(e) {
        e.preventDefault();

        var input = $('.input-number');
        var type = $(this).attr('data-type');

        changeQuantity($(this), input, type)
    });

    $('.input-number').focusin(function(){
        $(this).data('oldValue', $(this).val());
    });

    $('.input-number').change(function(){

        minValue = parseInt($(this).attr('min'));
        maxValue = parseInt($(this).attr('max'));
        valueCurrent = parseInt($(this).val())

        if (valueCurrent > minValue) {
            $('.btn-number[data-type="minus"]').removeClass('disabled');
        } else {
            $(this).val($(this).data('oldValue'));
        }
        
        if (valueCurrent <= maxValue) {
            $('.btn-number[data-type="plus"]').removeClass('disabled');
        } else if (!isNaN(valueCurrent)) {
            $(this).val($(this).attr('max'));
        } else {
            $(this).val($(this).data('oldValue'));
        }
    });

    // end quantity unput

    // add product to cart
    $('.add-cart').on('click', function(){
        let _product_id = $(this).attr('data-product')
        let _quantity = parseInt($('.input-number').val(), 10)
        let _btn = $(this)
        let _bool = parseInt($(this).attr('data-bool'), 10)

        $.ajax({
            url: '/shop/add_cart',
            data: {
                quantity: _quantity,
                product_id: _product_id,
                update: _bool
            },
            datatype: 'json',
            success: function(response) {
                if (response.bool) {
                    _btn.html('<i class="me-1 fa fa-shopping-basket" aria-hidden="true"></i> Добавлено').change()
                    _btn.addClass('disabled')
                } else {
                    console.log('Удалено')
                };
            },
            error: function(xhr, textStatus, errorThrown) {
                console.error('Ошибка. Не удалось добавить/удалить в корзину', errorThrown)
            }
        });

    });

    // end add product to cart

    // cart quantity

    $('.js-cart-btn').on('click', function(){
        let dataId = parseInt($(this).attr('data-id'), 10);
        let input = $('.js-cart-input[data-id="'+ dataId + '"]');
        let type = $(this).attr('data-type');
        let currentValue = input.val();

        changeQuantity($(this), input, type);

    });

    $('.js-cart-input').focusin(function(){
        $(this).data('oldValue', $(this).val());
    });

    $('.js-cart-input').change(function(){
        minValue = parseInt($(this).attr('min'), 10);
        maxValue = parseInt($(this).attr('max'), 10);
        valueCurrent = parseInt($(this).val());
        dataId = $(this).attr('data-id');



        if (valueCurrent >= minValue) {
            $('.js-cart-btn[data-id="' + dataId + '"][data-type="minus"').removeClass('disabled');
        } else {
            $(this).val($(this).data('oldValue'));
        };
        if (valueCurrent <= maxValue) {
            $('.js-cart-btn[data-id="' + dataId + '"][data-type="plus"').removeClass('disabled');
        } else if (!isNaN(valueCurrent)) {
            $(this).val($(this).attr('max'));
        } else {
            $(this).val($(this).data('oldValue'));
        }

        $.ajax({
            url: '/shop/update_cart',
            data: {
                product_id: dataId,
                quantity: $(this).val(),
                update: 1
            },
            dataType: 'json',
            success: function(response) {
                // Подставляю тотал цену товара
                $('.itotal[data-id="' + dataId + '"]').html(response['itotal'].replace('.', ',') + ' руб');
                // Подставляю скидку
                $('.js-discount').html(response['discount'].replace('.', ','));
                // Подставляю общий тотал
                $('.total-price').html(response['total'].replace('.', ','));
            },
            error: function(xhr, textStatus, errorThrown) {
                console.error('Ошибка. Не удалось изменить корзину', errorThrown);
            }

        });

    });

    // end cart quantity
});


function confirmDelete() {
    return confirm("Вы точно хотите удалить этот комментарий?");
}