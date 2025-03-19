from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request):
        """
        Khởi tạo giỏ hàng
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # lưu giỏ hàng trống vào session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, override_quantity=False):
        """
        Thêm sản phẩm vào giỏ hàng hoặc cập nhật số lượng
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()
    
    def save(self):
        # đánh dấu session là "đã sửa đổi" để đảm bảo lưu lại
        self.session.modified = True
    
    def remove(self, product):
        """
        Xóa sản phẩm khỏi giỏ hàng
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        """
        Duyệt qua các mục trong giỏ hàng và lấy các sản phẩm từ cơ sở dữ liệu
        """
        product_ids = self.cart.keys()
        # lấy các đối tượng sản phẩm và thêm vào giỏ hàng
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """
        Đếm tất cả các mục trong giỏ hàng
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """
        Tính tổng giá trị giỏ hàng
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        # xóa giỏ hàng khỏi session
        del self.session[settings.CART_SESSION_ID]
        self.save()