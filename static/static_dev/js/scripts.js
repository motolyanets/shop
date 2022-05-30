$(document).ready(function(){
    const form = $('#form_buying_product');
    
    function basketUpdating(productId, number, isDelete) {
        const data = {};
        data.product_id = productId;
        data.number = number;
        const csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;

        if (isDelete) {
            data['isDelete'] = true
        }

        const url = form.attr("action");
        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cash: true,
            success: function (data) {
                if (data.productsTotalNumber || data.productsTotalNumber == 0) {
                    $('#basket_total_number').text('('+data.productsTotalNumber+')')
                    $('.basket-items ul').html('')
                    $.each(data.products, function(k, v) {
                        $('.basket-items ul').append('<li>'+v.name+', '+v.number+' шт. по '+v.pricePerItem+' BYN '+
                            '<a class="delete-item" href="/" data-product_id="'+v.id+'">X</a>'+
                            '</li>')
                    })
                }
                
            }
        });

    }
    
    form.on('submit', function(element) {
        element.preventDefault();
        const number = $('#number').val();
        const submitBtn = $('#submit_btn');
        const productId = submitBtn.data('product_id');
        const productName = submitBtn.data('name');
        const productPrice = submitBtn.data('price');

        basketUpdating(productId, number, isDelete=false)
    })



    function showingBasket() {
        $('.basket-items').toggleClass('hidden');
    }

    $('.basket-container').on('click', function(e){
        e.preventDefault();
        showingBasket();
    })

    $('.basket-container').mouseover(function(){
        showingBasket();
    })

    $('.basket-container').mouseout(function(){
        showingBasket();
    })

    $(document).on('click', '.delete-item', function(e) {
        e.preventDefault();
        productId = $(this).data('product_id')
        number = 0
        basketUpdating(productId, number, isDelete=true)
    })

});