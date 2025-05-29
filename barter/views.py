# barter/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item, Offer, UserProfile
from .forms import ItemForm, OfferForm, UserProfileForm

def index(request):
    items = Item.objects.filter(is_active=True).order_by('-created_at')[:12]
    return render(request, 'barter/index.html', {'items': items})

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
def my_items(request):
    items = Item.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'barter/items/my_items.html', {'items': items})

@login_required
def my_offers(request):
    received = Offer.objects.filter(to_user=request.user).order_by('-created_at')
    sent = Offer.objects.filter(from_user=request.user).order_by('-created_at')
    return render(request, 'barter/offers/my_offers.html', {
        'received_offers': received,
        'sent_offers': sent,
    })

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