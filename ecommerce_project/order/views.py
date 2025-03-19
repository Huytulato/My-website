from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart

@login_required
def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Giỏ hàng của bạn đang trống, vui lòng thêm sản phẩm!')
        return redirect('shop:product_list')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Xóa giỏ hàng
            cart.clear()
            messages.success(request, 'Đặt hàng thành công! Cảm ơn bạn đã mua sắm.')
            return redirect('order:order_detail', order_id=order.id)
    else:
        # Điền trước thông tin từ profile user
        initial_data = {
            'full_name': f"{request.user.first_name} {request.user.last_name}",
            'email': request.user.email,
        }
        # Nếu có profile với phone và address thì thêm vào
        if hasattr(request.user, 'profile'):
            initial_data.update({
                'phone': request.user.profile.phone,
                'address': request.user.profile.address,
                'city': request.user.profile.city,
            })
        form = OrderCreateForm(initial=initial_data)
    
    return render(request, 'order/order_create.html', {'form': form, 'cart': cart})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order/order_detail.html', {'order': order})
