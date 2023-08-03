{% if item in wishlist.products.all %}
        <form method="POST" action="{% url 'store:remove_wishlist' item.id %}" name="remove-from-wishlist"
              id="form-remove-wishlist-{{ item.id }}">
            {% csrf_token %}
            <button type="submit" class="btn btn-default text-danger wishlist" data-toggle="tooltip"
                    data-placement="right" title="Удалить из избранного"><i class="fa fa-heart"></i>
            </button>
        </form>
        {% else %}
        <form method="POST" action="{% url 'store:add_wishlist' item.id %}" name="add-in-wishlist"
              id="form-add-wishlist-{{ item.id }}">
            {% csrf_token %}
            <button type="button" onclick="addToWishlist({{ item.id }})" class="btn btn-default wishlist" data-toggle="tooltip"
                    data-placement="right" title="Добавить в избранное"><i class="fa fa-heart"></i>
            </button>
        </form>
        {% endif %}



        <ul class="m-3 list-group list-group-flush">
                    <li class="list-group-item"><span>Полная стоимость:</span> <span class="ms-3">{{ cart.get_total_price }} руб.</span></li>
                    <li class="list-group-item"><span>СКИДКА:</span> <span class="ms-3">-{{ cart.get_discount|floatformat:'2' }} руб.</span></li>
                    <li class="list-group-item"><span>К оплате:</span> <span class="ms-3">{{ cart.get_the_final_total_price }} руб.</span></li>
                </ul>