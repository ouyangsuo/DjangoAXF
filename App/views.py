'''
定义路由处理逻辑
'''

import hashlib
import uuid
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, UserModel, CartModel, \
    OrderModel, OrderGoodsModel

# 首页
def home(request):

    # 查询数据
    wheels = MainWheel.objects.all()
    navs = MainNav.objects.all()
    mustbuys = MainMustBuy.objects.all()
    shops = MainShop.objects.all()
    mainshows = MainShow.objects.all()

    # 加工数据
    shop0 = shops[0:1]
    shop1_3 = shops[1:3]
    shop3_7 = shops[3:7]
    shop7_11 = shops[7:11]

    # 组织数据
    data = {
        "title": "首页",
        "wheels": wheels,
        "navs": navs,
        "mustbuys": mustbuys,
        "shop0": shop0,
        "shop1_3": shop1_3,
        "shop3_7": shop3_7,
        "shop7_11": shop7_11,
        "mainshows": mainshows,
    }

    # 携带数据渲染页面
    return render(request, 'home/home.html',context= data)

# 闪购
def market(request):
    # 重定向到marketWithParams方法所对应的路由
    # args=("104749", "0","0")处理函数参数
    return redirect(reverse("axf:marketWithParams", args=("104749", "0","0")))

# 闪购详情
def marketWithParams(request, typeid, cid, sort_rule):

    # 查询所有食品类型
    foodtypes = FoodType.objects.all()

    # 查询当前选中的食品类型
    foodtype_currents = FoodType.objects.filter(typeid=typeid)

    # 预定义食品类型中的子类
    child_type_list = []

    if foodtype_currents.exists():

        # 查询当前选中的食品类型（仅有一条数据）
        foodtype = foodtype_currents.first()

        # 获取所有子类名称
        childtypes = foodtype.childtypenames
        childtypenames = childtypes.split("#")
        # ["全部分类:0","XXX:1"]
        print(childtypenames)

        for childtypename in childtypenames:
            #  ["全部分类“,"0"]
            child_type_info = childtypename.split(":")
            child_type_list.append(child_type_info)
    # child_type_list
    # [["全部分类","0"],["进口水果","110"]]

    # 根据分类查询到对应的所有商品
    if cid == "0":
        goods_list = Goods.objects.filter(categoryid=typeid)
    # typeid 和 categoryid   并且是一对多的一个关系
    else:
        goods_list = Goods.objects.filter(categoryid=typeid).filter(childcid=cid)

    # 将商品按指定顺序排序
    if sort_rule == "0":
        pass
    elif sort_rule == "1":
        goods_list = goods_list.order_by("productnum")
    elif sort_rule == "2":
        goods_list = goods_list.order_by("-price")
    elif sort_rule == "3":
        goods_list = goods_list.order_by("price")

    # 组织数据
    data = {
        "title": "闪购",
        "foodtypes": foodtypes,
        "goods_list": goods_list,
        "typeid": typeid,
        "cid": cid,
        "child_type_list": child_type_list,
    }

    # 传递数据给页面并渲染
    return render(request, 'market/market.html', context= data)

# 购物车
def cart(request):

    user_id = request.session.get("user_id")

    if not user_id:
        return redirect(reverse("axf:user_login"))

    carts = CartModel.objects.filter(user_id=user_id)

    is_select = True

    for cart_obj in carts:
        if not cart_obj.is_select:
            is_select = False
            break

    data = {
        "title": "购物车",
        "carts": carts,
        "is_select": is_select,
    }

    return render(request, 'cart/cart.html', context= data)

# 我的
def mine(request):

    user_id = request.session.get("user_id")

    data = {
        "title": "我的"
    }

    if user_id:
        users = UserModel.objects.filter(pk=user_id)
        if users.exists():
            user = users.first()
            username = user.username
            icon = "/static/uploads/" + user.icon.url
            data["username"] = username
            data["icon"] = icon
            data["is_login"] = True
            # user = UserModel()

            orders = user.ordermodel_set.all()

            wait_pay = 0
            payed = 0

            for order in orders:
                if order.o_status == 0:
                    wait_pay += 1
                elif order.o_status == 1:
                    payed += 1
                elif order.o_status == 2:
                    pass
            data["wait_pay"] = wait_pay
            data["payed"] = payed

    return render(request, 'mine/mine.html', context= data)

# 用户注册
def user_register(request):
    if request.method == "GET":
        return render(request, 'user/user_register.html')
    elif request.method == "POST":
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            email = request.POST.get("email")
            icon = request.FILES.get("icon")

            print(username)
            print(password)
            print(email)
            print(icon)

            user = UserModel()
            user.username = username
            # 添加数据安全
            password = generate_password(password)
            print(password)
            user.password = password
            user.email = email
            user.icon = icon
            user.save()
            request.session["user_id"] = user.id

            return redirect(reverse("axf:mine"))
        except Exception as e:
            return redirect(reverse("axf:user_register"))
    else:
        raise Exception("不被支持的请求")

# TODO 生成密码
def generate_password(password):

    sha = hashlib.sha512()

    sha.update(password.encode("utf-8"))

    return sha.hexdigest()

# 用户登出
def user_logout(request):
    request.session.flush()
    return redirect(reverse("axf:mine"))

# 用户登录
def user_login(request):
    if request.method == "GET":
        return render(request, 'user/user_login.html')
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        users = UserModel.objects.filter(username=username)

        if users.exists():
            user = users.first()
            if user.password == generate_password(password):
                request.session['user_id'] = user.id
                return redirect(reverse("axf:mine"))

        return redirect(reverse("axf:user_login"))

# 校验用户名是否可用
def check_user(request):
    username = request.GET.get("username")
    users = UserModel.objects.filter(username=username)

    data = {
        "msg":"ok",
        "status":"200",
    }

    if users.exists():
        data["desc"] = "用户已存在"
        data["msg"] = "fail"
        data["status"] = "900"
    else:
        data["desc"] = "用户名可用"
    return JsonResponse(data)

# 增加购物车商品数量
def add_to_cart(request):
    goodsid = request.GET.get("goodsid")
    userid = request.session.get("user_id")

    # 加入逻辑
    data = {
        "msg": "ok",
        "status": "200",
    }

    if not userid:
        data["status"] = "901"
        data["msg"] = "not login"
    else:
        # 将数据添加到购物车中
        carts = CartModel.objects.filter(goods_id=goodsid).filter(user_id=userid)
        if carts.exists():
            cart = carts.first()
            cart.c_num = cart.c_num + 1
            cart.save()
            data["g_num"] = cart.c_num
        else:
            cart = CartModel()
            cart.user_id = userid
            cart.goods_id = goodsid
            cart.save()
            data["g_num"] = 1

    return JsonResponse(data)

# 减少购物车商品数量
def sub_to_cart(request):
    goodsid = request.GET.get("goodsid")
    userid = request.session.get("user_id")

    # 加入逻辑
    data = {
        "msg": "ok",
        "status": "200",
    }

    if not userid:
        data["status"] = "901"
        data["msg"] = "not login"
    else:
        # 将数据添加到购物车中
        carts = CartModel.objects.filter(goods_id=goodsid).filter(user_id=userid)
        if carts.exists():
            cart = carts.first()
            if cart.c_num == 1:
                cart.delete()
                data["g_num"] = 0
            else:
                cart.c_num = cart.c_num - 1
                cart.save()
                data["g_num"] = cart.c_num
        else:
            data["g_num"] = 0
            data["msg"] = "cart not exist"
            data["status"] = "902"

    return JsonResponse(data)

# 修改购物车状态
def change_cart_status(request):

    data = {
        "msg": "ok",
        "status": "200",
    }

    cart_id = request.GET.get("cart_id")

    carts = CartModel.objects.filter(pk=cart_id)

    cart_obj = carts.first()

    cart_obj.is_select = not cart_obj.is_select

    cart_obj.save()

    user_id = request.session.get("user_id")

    carts_all =CartModel.objects.filter(user_id=user_id)

    is_all_select = True

    for cart_select in carts_all:
        if not cart_select.is_select:
            is_all_select = False
            break

    data["is_all_select"] = is_all_select
    data["check"] = cart_obj.is_select

    return JsonResponse(data)

# 删除购物车记录
def sub_cart(request):
    cart_id = request.GET.get("cart_id")

    carts = CartModel.objects.filter(pk=cart_id)

    cart_obj = carts.first()

    data = {
        "msg":"ok",
        "status":"200",
    }

    if cart_obj.c_num == 1:
        cart_obj.delete()
        data["c_num"] = "0"
        data["status"] = "903"
    else:
        cart_obj.c_num = cart_obj.c_num - 1
        cart_obj.save()
        data["c_num"] = cart_obj.c_num

    return JsonResponse(data)

# 插入购物车记录
def add_cart(request):
    cart_id = request.GET.get("cart_id")

    carts = CartModel.objects.filter(pk=cart_id)

    data = {
        "msg":"ok",
        "status": "200",
    }

    cart_obj = carts.first()

    cart_obj.c_num = cart_obj.c_num + 1

    cart_obj.save()

    data["c_num"] = cart_obj.c_num

    return JsonResponse(data)

# 修改购物车选中状态
def change_cart_select(request):
    action = request.GET.get("action")

    selects = request.GET.get("selects")
    print(selects)

    select_list = selects.split("#")

    data = {
        "msg": "ok",
        "status": "200"
    }

    if action == "select":
        for select in select_list:
            cart = CartModel.objects.get(pk=select)
            cart.is_select = True
            cart.save()
        data["action"] = "select"
        data["selects"] = selects
    else:
        for select in select_list:
            cart = CartModel.objects.get(pk=select)
            cart.is_select = False
            cart.save()
        data["action"] = "unselect"
        data["selects"] = selects

    return JsonResponse(data)

# 生成订单
def generate_order(request):

    selects = request.GET.get("selects")

    select_list = selects.split("#")

    user_id = request.session.get("user_id")

    data = {
        "msg": "ok",
        "status": "200",
    }

    # 先生成一个订单
    order = OrderModel()
    order.user_id = user_id
    order.o_num = str(uuid.uuid4())
    order.save()

    # 要生成订单商品信息
    for select_obj in select_list:
        order_goods = OrderGoodsModel()
        cart_object = CartModel.objects.get(pk=select_obj)
        order_goods.goods_id = cart_object.goods_id
        order_goods.goods_num = cart_object.c_num
        order_goods.order_id = order.id
        order_goods.save()
        cart_object.delete()

    data["order_id"] = order.id
    # 移除购物车中的数据

    return JsonResponse(data=data)

# 查看订单详情
def order_info(request, order_id):

    order = OrderModel.objects.get(pk=order_id)

    data = {
        "order_id": order_id,
        "order": order,
    }

    return render(request, 'order/order_info.html', context=data)

# 修改订单状态
def change_order_status(request):

    order_id = request.GET.get("order_id")

    status = request.GET.get("status")

    print(order_id)

    data = {
        "msg": "ok",
        "status": "200",
    }

    order = OrderModel.objects.get(pk=order_id)

    order.o_status = status

    order.save()

    data["msg"] = "change success"

    return JsonResponse(data=data)

# 显示订单列表
def order_list(request):

    user_id = request.session.get("user_id")

    orders = OrderModel.objects.filter(user_id=user_id).filter(o_status=1)

    data = {
        "orders": orders,
    }

    return render(request, 'order/order_list_payed.html', context=data)

# 待支付的订单列表
def order_list_wait_pay(request):

    user_id = request.session.get("user_id")

    orders = OrderModel.objects.filter(user_id=user_id).filter(o_status=0)

    data = {
        "orders": orders,
    }

    return render(request, 'order/order_list_wait_pay.html', context=data)