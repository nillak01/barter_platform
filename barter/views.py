# barter/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item, Offer, UserProfile, Category
from .forms import ItemForm, OfferForm, UserProfileForm, ItemImageForm
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
import logging




logger = logging.getLogger(__name__)


def index(request):
    items = Item.objects.filter(is_active=True).order_by('-created_at')[:12]
    return render(request, 'barter/index.html', {'items': items})


def register(request):
    if request.method == 'POST':
        logger.info(f"POST data: {request.POST}")
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            logger.info(f"User created: {user.username}")
            return redirect('barter:login')
        else:
            logger.error(f"Form errors: {form.errors}")
    else:
        form = UserCreationForm()
    return render(request, 'registration/singup_min.html', {'form': form})


def static_test(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <link href="/static/barter/css/auth.css" rel="stylesheet">
    </head>
    <body>
        <h1 style="color: red;">Если текст красный - стили не загрузились</h1>
    </body>
    </html>
    """
    return HttpResponse(html)

@login_required
def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id, is_active=True)
    user_offers = None

    if request.user == item.owner:
        user_offers = Offer.objects.filter(to_item=item).order_by('-created_at')
    else:
        user_offers = Offer.objects.filter(
            from_user=request.user,
            to_item=item
        ).exists()

    return render(request, 'barter/items/detail.html', {
        'item': item,
        'user_offers': user_offers,
    })

@login_required
def create_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            messages.success(request, 'Объявление успешно создано!')
            return redirect('item_detail', item_id=item.id)
    else:
        form = ItemForm()

    return render(request, 'barter/items/create.html', {'form': form})

@login_required
def create_offer(request, item_id):
    to_item = get_object_or_404(Item, pk=item_id, is_active=True)

    if request.method == 'POST':
        form = OfferForm(request.user, request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.from_user = request.user
            offer.to_user = to_item.owner
            offer.to_item = to_item
            offer.save()
            messages.success(request, 'Предложение отправлено!')
            return redirect('item_detail', item_id=to_item.id)
    else:
        form = OfferForm(request.user)

    return render(request, 'barter/offers/create.html', {
        'form': form,
        'to_item': to_item,
    })


@require_POST  # Разрешаем только POST-запросы
@login_required
def delete_offer(request, pk):
    """
    Удаляет предложение с подтверждением
    """
    offer = get_object_or_404(Offer, pk=pk, user=request.user)
    offer_title = offer.title
    offer.delete()

    messages.success(request, f"Предложение '{offer_title}' успешно удалено")
    return redirect('my_offers')


@login_required
def manage_offer(request, offer_id, action):
    offer = get_object_or_404(Offer, pk=offer_id, to_user=request.user)

    if action == 'accept':
        offer.status = 'accepted'
        offer.save()
        messages.success(request, 'Предложение принято!')
    elif action == 'reject':
        offer.status = 'rejected'
        offer.save()
        messages.info(request, 'Предложение отклонено.')

    return redirect('my_offers')


@login_required
def edit_offer(request, pk):
    """
    Редактирование существующего предложения
    """
    offer = get_object_or_404(Offer, pk=pk, user=request.user)

    if request.method == 'POST':
        form = OfferForm(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('my_offers')  # Или другой подходящий URL
    else:
        form = OfferForm(instance=offer)

    return render(request, 'barter/offers/edit_offer.html', {
        'form': form,
        'offer': offer,
        'title': 'Редактирование предложения'
    })


@login_required
def toggle_offer_status(request, pk):
    """
    Переключает статус активности предложения (активно/неактивно)
    """
    offer = get_object_or_404(Offer, pk=pk, user=request.user)

    # Переключаем статус
    offer.is_active = not offer.is_active
    offer.save()

    # Добавляем сообщение для пользователя
    status = "активно" if offer.is_active else "неактивно"
    messages.success(request, f"Предложение '{offer.title}' теперь {status}")

    return redirect('my_offers')


@login_required
def my_items(request):
    # Получаем параметры фильтрации
    category_id = request.GET.get('category', '')
    sort_by = request.GET.get('sort', '-created_at')

    # Получаем товары пользователя
    items = Item.objects.filter(owner=request.user)

    # Применяем фильтрацию по категории
    if category_id:
        items = items.filter(category_id=category_id)

    # Применяем сортировку
    items = items.order_by(sort_by)

    # Пагинация
    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Получаем все категории для фильтра
    categories = Category.objects.all()

    context = {
        'items': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'selected_sort': sort_by,
    }

    return render(request, 'barter/users/my_items.html', context)


@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.owner = request.user
            item.save()
            # Обработка множественных изображений, если нужно
            return redirect('my_items')
    else:
        form = ItemForm()

    return render(request, 'barter/users/add_item.html', {
        'form': form,
        'title': 'Добавить товар'
    })


@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('my_items')
    else:
        form = ItemForm(instance=item)

    return render(request, 'barter/users/add_item.html', {
        'form': form,
        'title': 'Редактировать товар'
    })

@login_required
def toggle_item_status(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    item.is_active = not item.is_active
    item.save()
    return redirect('my_items')


@login_required
def create_item(request):
    """
    Создание нового товара с возможностью загрузки нескольких изображений
    """
    if request.method == 'POST':
        item_form = ItemForm(request.POST)
        image_form = ItemImageForm(request.POST, request.FILES)

        if item_form.is_valid():
            # Сохраняем товар без коммита, чтобы установить владельца
            item = item_form.save(commit=False)
            item.owner = request.user
            item.save()

            # Обрабатываем загруженные изображения
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                ItemImage.objects.create(
                    item=item,
                    image=image,
                    is_primary=(i == 0)  # Первое изображение делаем основным
                )

            messages.success(request, 'Товар успешно добавлен!')
            return redirect('my_items')
    else:
        item_form = ItemForm()
        image_form = ItemImageForm()

    return render(request, 'barter/items/create_item.html', {
        'item_form': item_form,
        'image_form': image_form,
        'title': 'Добавить новый товар'
    })


@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk, owner=request.user)
    if request.method == 'POST':
        item.delete()
        return redirect('my_items')
    return render(request, 'barter/users/confirm_delete.html', {'item': item})

@login_required
def items_bulk_action(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            item_ids = request.POST.getlist('item_ids[]')
            action = request.POST.get('action')

            items = Item.objects.filter(id__in=item_ids, owner=request.user)

            if action == 'activate':
                items.update(is_active=True)
            elif action == 'deactivate':
                items.update(is_active=False)
            elif action == 'delete':
                items.delete()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
def my_offers(request):
    status_filter = request.GET.get('status', 'active')

    if status_filter == 'active':
        offers = Offer.objects.filter(user=request.user, is_active=True)
    elif status_filter == 'pending':
        offers = Offer.objects.filter(user=request.user, is_approved=False)
    elif status_filter == 'archived':
        offers = Offer.objects.filter(user=request.user, is_active=False, is_approved=True)
    else:
        offers = Offer.objects.filter(user=request.user, is_active=True)

    # Пагинация
    paginator = Paginator(offers, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'offers': page_obj,
        'active_filter': status_filter,
        'active_offers': Offer.objects.filter(user=request.user, is_active=True).count(),
        'pending_offers': Offer.objects.filter(user=request.user, is_approved=False).count(),
        'archived_offers': Offer.objects.filter(user=request.user, is_active=False, is_approved=True).count(),
    }

    return render(request, 'barter/users/my_offers.html', context)

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'barter/users/profile.html', {'form': form})
