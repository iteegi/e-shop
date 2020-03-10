"""Cart."""

from decimal import Decimal
from django.conf import settings

from shop.models import Product
from coupons.models import Coupon


class Cart(object):
    """Cart object."""

    def __init__(self, request):
        """Initializ the cart object."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем в сессии пустую корзину.
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        # Сохраняем купон.
        self.coupon_id = self.session.get('coupon_id')

    def __iter__(self):
        """Iterate for Product."""
        product_ids = self.cart.keys()
        # Получаем объекты модели Product и передаем их в корзину.
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Return the total number of items in the basket."""
        return sum(item['quantity'] for item in self.cart.values())

    @property
    def coupon(self):
        """Return the corresponding coupon object."""
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        """Return discount amount."""
        if self.coupon:
            return (self.coupon.discount / Decimal('100'))\
                * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        """Return the total cost of goods."""
        return self.get_total_price() - self.get_discount()

    def add(self, product, quantity=1, update_quantity=False):
        """Add the product to the basket or update its quantity."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Save product in basket."""
        # Помечаем сессию как измененную
        self.session.modified = True

    def remove(self, product):
        """Remove item from cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """Empty trash."""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        """Return total basket value."""
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.cart.values())
