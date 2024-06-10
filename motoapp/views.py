from django.shortcuts import render,redirect,HttpResponse
from .models import Category,Sell,Buy,Bcategory,Cart,Order,Profile,ShippingAddress,SendQuotation,Request
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import random
from django import forms
from .forms import UpdateUserForm,UserInfoForm,ShippingForm,RequestForm
from django.contrib import messages
import razorpay
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def update_info(request):
    if request.user.is_authenticated:
        # Get Current User
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get Current User Shipping Info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        #Get original User form
        form = UserInfoForm(request.POST or None, instance=current_user)
        #Get User Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            # save original form
            form.save()
            # save shipping address
            shipping_form.save()
            messages.success(request,'Your Info Has Been Updated')
            return redirect('buying')
        return render(request,'update_info.html',{'form':form,'shipping_form':shipping_form})
    else:
        messages.success(request,'You Must Be Logged In'),
        return redirect('buying')

    
    return render(request,'update_info.html')

def user_login(request):
    if request.method=="POST":
        uname=request.POST['uname']
        upass=request.POST['upass']
        print(uname,":",upass)
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Field cannot be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            #print(u)
            #print(u.username)
            #print(u.password)
            #print(u.is_superuser)
            if u is not None:
                login(request,u)
                messages.success(request, ("You have logged in..."))
                return redirect('/bss')


            else:
                context['errmsg']="Invalid username/password"
                return render(request,'login.html',context)
    else:
        return render(request,'login.html')



def register(request):
    context={}
    if request.method=='POST':
        uname=request.POST['uname']
        umail=request.POST['umail']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        print(uname,umail,upass,ucpass)
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Fields cannot be empty"
            return render(request,'register.html',context)
        elif upass!=ucpass:
            context['errmsg']="pass and confirm pass is not matching"
            return render(request,'register.html',context)
        else:
            try: 
              u=User.objects.create(password=upass,username=uname,email=umail)
              u.set_password(upass)
              u.save()
              context['success']="User Registered succesfully please go ahead and login"
              return render(request,'register.html',context)   
            except Exception:
              context['errmsg']="User already registerd,please use differnt id"
              return render(request,'register.html',context)   
    else:
        return render(request,'register.html',context)

def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "User Has Been Updated!!")
			return redirect('buying')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('buying')


def update_password(request):
    return render(request,'update_password.html')

def header(request):
    return render(request,'header.html')

def home(request):
    return render(request,'home.html')

def test(request):
    return render(request,'test.html')

def bss(request):
    return render(request,'bss.html')

def buy12(request):
    return render(request,'buy12.html')

def buying(request):
    bcategory = request.GET.get('bcategory')

    if bcategory:
        buys = Buy.objects.filter(bcategory__name=bcategory)
    else:
        buys = Buy.objects.all()

    bcategories =Bcategory.objects.all()
    context = {
        'bcategories': bcategories,
        'buys': buys,
        'selected_category': bcategory,
    }
    return render(request,'buying.html', context)


def selling(request):
    category = request.GET.get('category')

    if category:
        sells = Sell.objects.filter(category__name=category)
    else:
        sells = Sell.objects.all()

    categories = Category.objects.all()
    context = {
        'categories': categories,
        'sells': sells,
        'selected_category': category,
    }
    return render(request, 'selling.html', context)

def range(request):
    # Retrieve category, min, and max parameters from request.GET
    category = request.GET.get('category')
    min_price = request.GET.get('min')
    max_price = request.GET.get('max')

    # Start with all Sell objects
    sells = Sell.objects.all()

    # Apply category filter if category parameter is provided
    if category:
        sells = sells.filter(category__name=category)

    # Apply price range filter if both min and max parameters are provided
    if min_price is not None and max_price is not None:
        # Create a Q object for price range filter
        price_filter = (Q(price__gte=min_price) & Q(price__lte=max_price))
        sells = sells.filter(price_filter)

    # Retrieve all categories to display in the template
    categories = Category.objects.all()

    # Prepare context to pass to template
    context = {
        'categories': categories,
        'sells': sells,
        'selected_category': category,
        'min_price': min_price,
        'max_price': max_price,
    }

    # Render the template with filtered sells and categories
    return render(request, 'selling.html', context)

def sort(request,sv):
    if sv=='0':
        col='price'
    else:
        col='-price'
    buys = Buy.objects.all().order_by(col)
    context={}
    context['buys']=buys
    return render(request,'buying.html',context)

def sort1(request,sv):
    if sv=='0':
        col='price'
    else:
        col='-price'
    sells = Sell.objects.all().order_by(col)
    context={}
    context['sells']=sells
    return render(request,'selling.html',context)

def range1(request):
    # Retrieve category, min, and max parameters from request.GET
    bcategory = request.GET.get('bcategory')
    min_price = request.GET.get('min')
    max_price = request.GET.get('max')

    # Start with all Sell objects
    buys = Buy.objects.all()

    # Apply category filter if category parameter is provided
    if bcategory:
        buys = buys.filter(Bcategory__name=Bcategory)

    # Apply price range filter if both min and max parameters are provided
    if min_price is not None and max_price is not None:
        # Create a Q object for price range filter
        price_filter = (Q(price__gte=min_price) & Q(price__lte=max_price))
        buys = buys.filter(price_filter)

    # Retrieve all categories to display in the template
    categories = Bcategory.objects.all()

    # Prepare context to pass to template
    context = {
        'categories': categories,
        'buys': buys,
        'selected_category': bcategory,
        'min_price': min_price,
        'max_price': max_price,
    }

    # Render the template with filtered sells and categories
    return render(request, 'buying.html', context)




    
def sell_form(request):
    categories=Category.objects.all()

    if request.method=='POST':
        data=request.POST
        image=request.FILES.get('image')
        category_id = data.get('category') 
        #print('data',data)
        #print('image',image)

        #if data['category'] != 'none':
         #   category = Category.objects.get(id=data['category'])
        #else:
         #   category = None
        if category_id :
        
            sell = Sell.objects.create (
            category_id=category_id,
            brand = data['brand'],
            modelv = data['modelv'],
            year= data['year'],
            fuel = data['fuel'],
            km_driven = data['km_driven'],
            no_owners = data['no_owner'],
            description = data['descp'],
            price = data['price'],
            image = image,
            pname = data['pname'],
            contact_number = data['contact'],
            email =data['email'],
            address = data['address'],

            )
            return redirect('selling')

    context={}
    context['categories']=categories

    return render(request,'sell_form.html',context)

def sell_details(request,pk):
    sells=Sell.objects.get(id=pk)
    context={}
    context['sells']=sells

    return render(request,'sell_details.html',context)

def buy_details(request,pk):
    buys=Buy.objects.filter(id=pk)
    context={}
    context['buys']=buys
    return render(request,'buy_details.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        #print(userid)
        #print(pid)
        u=User.objects.filter(id=userid)
        p=Buy.objects.filter(id=pid)
        #print(u)
        #print(p)
        #c=Cart.objects.create(uid=u[0],pid=p[0]) #It will give the paricular id not the full query set if we write u and p it will give value error(instance error)
        #c.save()
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)
        print(n)
        context={}
        if n==1:
            messages.success(request, ("Already exist in the cart... please go head and start booking!"))
            context['buys']=p
            return render(request,'buy_details.html',context)
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0]) #It will give the paricular id not the full query set if we write u and p it will give value error(instance error)
            c.save()
            messages.success(request, ("Vehicle Successfully added to the Cart!!!"))
            context['buys']=p
            return render(request,'buy_details.html',context)
    else:
        return redirect('/login')

def cart(request):
    c=Cart.objects.filter(uid=request.user.id)
    print('c',c)  #it gives the cart item added by the user
    print(len(c)) #number of item add by the user
    context={}
    if len(c) == 0:
        messages.success(request, ("No Product in the cart..."))
        return render(request,'cart.html',context)
    else: 
        #print(c[0]) #returns the first item from the list
        #print(c[0].pid.brand) #it will go for product details and get the name as pid is the foreign key it will refer to the Buy table 
        #print(c[0].pid.price) 
        #print('cate',c[0].pid.bcategory)
        s=0
        for x in c:
            #print('x',x)               #BMW/Dechathlon
            #print('x.pid.price',x.pid.price)     #70000/4000
            s=s+int(x.pid.price)*x.qty
        #print(s)
        context['total']=s
        context['data']=c
        context['quotation_sent']=request.session.get('quotation_sent', False)
        return render(request,'cart.html',context)




def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    print(c) 
    print(c[0],'c[0]')
    print(c[0].qty) 
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
           t=c[0].qty-1
           c.update(qty=t)
    
    return redirect('/cart')

def remove(request,uid):
    c=Cart.objects.filter(id=uid)
    c.delete()
    return redirect('/cart')

def remove_order(request,uid):
    c=Order.objects.filter(id=uid)
    c.delete()
    return redirect('/checkout')



def sendquote(request, uid):
    cart_items = Cart.objects.filter(uid=request.user.id)
    context = {
        'data': cart_items,
        'quotation_sent': request.session.get('quotation_sent', False)  # Check if quotation has been sent
    }
    return render(request, 'cart.html', context)

def checkout(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    #print(c)
    oid=random.randrange(1000,9999)
    print(oid)
    for x in c:
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save
        x.delete()
    orders_to_delete = Order.objects.filter(uid=request.user.id, pid__bcategory__name='Cars')
    orders_to_delete.delete()  # This will delete all filtered Order objects
    orders=Order.objects.filter(uid=userid)
    context={}
    context['data']=orders
    s=0
    for x in orders:
        print('x',x)               #BMW/Dechathlon
        print('x.pid.price',x.pid.price)     #70000/4000
        s=s+int(x.pid.price)*x.qty
    shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
    shipping_form = ShippingForm(request.POST or None, instance = shipping_user)
    print(s)
    context={}
    context['total']=s
    context['data']=orders
    context['shipping_form']=shipping_form
    return render(request,'placeorder.html',context)

def billing_info(request):
    #if request.POST:
        c=Cart.objects.filter(uid=request.user.id)
        orders=Order.objects.filter(uid=request.user.id)
        s=0
        for x in orders:
            s=s+int(x.pid.price)*x.qty
        shipping_form = request.POST
        context={}
        context['total']=s
        context['data']=orders
        context['shipping_form']=shipping_form
        return render(request,'billing_info.html',context)
    #else:
        #messages.success(request, ("Access Denied"))
        #return redirect('/buying')

    
def ulogout(request):
    logout(request)  # once you press logout session will be deleted 
    messages.success(request, ("You have been logged out..."))
    return redirect('/home')


def sendquote(request,pid):
    qid=random.randrange(1000,9999)
    print(qid)
    userid=request.user.id
    if SendQuotation.objects.filter(uid=userid, pid=pid).exists():
        # If a quotation already exists, show a message or redirect as needed
        messages.error(request, "You have already sent a quotation for this product.")
        return redirect('/cart')
    c=Cart.objects.filter(uid=userid)
    for x in c:
        if x.pid.bcategory.name == 'Cars':
            q=SendQuotation.objects.create(quotation_id=qid,uid=x.uid,pid=x.pid)
            q.save()
            x.delete()
            context={}
            context['data']=q
            return render(request,'sendquotation.html',context)
        else:
            return HttpResponse("Quotation else")

def search(request):
    if request.method== "POST":
        searched= request.POST['searched']
        searched=Buy.objects.filter(Q(brand__icontains=searched)|Q(color__icontains=searched))
        if not searched:
           messages.error(request,"That Vehicle does not exist")
           return render(request,'search.html',{})
        else:
           return render(request,'search.html',{'searched':searched})
    else:
       return render(request,'search.html')

def search1(request):
    if request.method== "POST":
        searched= request.POST['searched']
        searched=Sell.objects.filter(brand__icontains=searched)
        if not searched:
           messages.error(request,"That Vehicle does not exist")
           return render(request,'search1.html',{})
        else:
           return render(request,'search1.html',{'searched':searched})
    else:
       return render(request,'search1.html')

def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0  #sum for cart items 
    np=len(orders)
    for x in orders:  
       s=s+x.pid.price*x.qty
       oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_0hi0j7fF3yzMjW", "7xWqdpAw4dpGhhdNycHcsXvH"))

    data = { "amount": s*100, "currency": "INR", "receipt":oid }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    uemail=request.user.username
    context['uemail']=uemail
    return render(request,'pay.html',context)

def sendusermail(request):
    c=Cart.objects.filter(uid=request.user.id)
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s=s+int(x.pid.price)*x.qty
    context={}
    context['total']=s
    context['data']=orders
    send_mail(
        "MotoBaY-Order Confimation mail!!",
        "Your order placed successfully, Thanks for your order.. Shop with us again",
         settings.EMAIL_HOST_USER, 
        ["monishaygowda81@gmail.com"],
        fail_silently=False,
    )
    return render(request,'email.html',context)

def email(request):
        c=Cart.objects.filter(uid=request.user.id)
        orders=Order.objects.filter(uid=request.user.id)
        s=0
        for x in orders:
            s=s+int(x.pid.price)*x.qty
        context={}
        context['total']=s
        context['data']=orders
        return render(request,'email.html',context)
        

def service_dashboard(request):
    return render(request,'service_dashboard.html')

    #for x in c:
     #       q=SendQuotation.objects.create(quotation_id=qid,uid=x.uid,pid=x.pid)
      #      q.save()

def customer_add_request_view(request):
    user=User.objects.get(id=request.user.id)
    enquiry=RequestForm()
    if request.method=='POST':
        enquiry=RequestForm(request.POST)
        if enquiry.is_valid():
            user=User.objects.get(id=request.user.id)
            enquiry_x=enquiry.save(commit=False)
            enquiry_x.user=user
            enquiry_x.save()
        else:
            print("form is invalid")
        return redirect('/service_dashboard')
    return render(request,'customer_add_request.html',{'enquiry':enquiry,'user':user})

def customer_view_request_view(request):
    user=User.objects.get(id=request.user.id)
    enquiries=Request.objects.all().filter(user_id=user.id , status="Pending")
    return render(request,'customer_view_request.html',{'user':user,'enquiries':enquiries})

def customer_delete_request_view(request,pk):
    user=User.objects.get(id=request.user.id)
    enquiry=Request.objects.get(id=pk)
    enquiry.delete()
    return redirect('customer-view-request')

def customer_view_approved_request_view(request):
    user=User.objects.get(id=request.user.id)
    enquiries=Request.objects.all().filter(user_id=user.id).exclude(status='Pending')
    return render(request,'customer_view_approved_request.html',{'user':user,'enquiries':enquiries})

def customer_view_approved_request_invoice_view(request):
    user=User.objects.get(id=request.user.id)
    enquiries=Request.objects.all().filter(user_id=user.id).exclude(status='Pending')
    return render(request,'customer_view_approved_request_invoice.html',{'user':user,'enquiries':enquiries})

def contact(request):
    return render(request,'contact.html')