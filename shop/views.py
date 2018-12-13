from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.http import HttpResponse
from .models import Category, Product
from django.contrib.auth.models import Group, User
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.views.generic.edit import CreateView, FormView
from .forms import StepOneForm, StepTwoForm


# Create your views here.

def index(request):
    text_var = 'This is my first Django WebPage'
    return HttpResponse(text_var)

# Category View


def allProdCat(request, c_slug=None):
    c_page = None
    products = None
    if c_slug != None:
        c_page = get_object_or_404(Category, slug = c_slug)
        products = Product.objects.filter(category=c_page, available=True)
    else:
        products = Product.objects.all().filter(available=True)
    return render(request, 'shop/category.html', {'category':c_page, 'products': products})




# def ProdCatDetail(request, c_slug, product_slug):
#     try:
#         product = Product.objects.get(category__slug=c_slug, slug = product_slug)
#     except Exception as e:
#         raise e
#     return render(request, 'shop/product-original.html', {'product':product})
#




# Tamanos y cantidades

class StepOneView(FormView):
    form_class = StepOneForm
    template_name = 'shop/product.html'
    success_url = 'shop/subir-arte'

    def get_initials(self):
         # pre-populate form if someone goes back and forth between forms
         initial = super(StepOneView, self).get_initial()
         initial['size'] = self.request.session.get('size', None)
         initial['quantity'] = self.request.session.get('quantity', None)
         initial['product'] = Product.objects.get(
                category__slug=self.kwargs['c_slug'],
                slug=self.kwargs['product_slug']
            )
         return initial

         # pre-populate form if someone goes back and forth between forms

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(
            category__slug=self.kwargs['c_slug'],
            slug=self.kwargs['product_slug']
        )
        return context


    def form_valid(self, form):
        # In form_valid method we can access the form data in dict format
        # and will store it in django session
        self.request.session['product'] = form.cleaned_data.get('product')
        self.request.session['size'] = form.cleaned_data.get('size')
        self.request.session['quantity'] = form.cleaned_data.get('quantity')
        return HttpResponseRedirect(self.get_success_url())


# here we are going to use CreateView to save the Third step ModelForm
class StepTwoView(CreateView):
    form_class = StepTwoForm
    template_name = 'shop/subir-arte.html'
    success_url = '/'

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['initial'] = {
    #         'product': Product.objects.get(
    #             category__slug=self.kwargs['c_slug'],
    #             slug=self.kwargs['product_slug']
    #         )
    #     }
    #     return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.objects.get(
            category__slug=self.kwargs['c_slug'],
            slug=self.kwargs['product_slug']
        )
        return context

    def form_valid(self, form):
        # form.instance.product = Product.objects.get(
        #     category__slug=self.kwargs['c_slug'],
        #     slug=self.kwargs['product_slug']
        # )
        form.instance.product = self.request.session.get('product')  # get tamanios from session
        form.instance.size = self.request.session.get('size')  # get tamanios from session
        form.instance.quantity = self.request.session.get('quantity')  # get cantidades from session
        del self.request.session['product']
        del self.request.session['quantity']  # delete cantidades value from session
        del self.request.session['size']  # delete tamanios value from session
        self.request.session.modified = True
        return super(StepTwoView, self).form_valid(form)





### Registro y Login/Logout de usuarios


def signupView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username = username)
            customer_group = Group.objects.get(name = 'Customer')
            customer_group.user_set.add(signup_user)
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form':form})


def signinView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # username = request.POST['username']
            # password = request.POST['password']
            print(username)
            print(password)
            user = authenticate(username = username,
                                password = password)
            if user is not None:
                login(request, user)
                return redirect('shop:allProdCat')
            else:
                return redirect('signup')

    else:
        form = AuthenticationForm()
    return render(request, 'accounts/signin.html', {'form':form})


def signoutView(request):
    logout(request)
    return redirect('signin')


