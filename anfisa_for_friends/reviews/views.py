from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from ice_cream.models import IceCream
from .models import Review, ReviewImage, can_review
from .forms import ReviewForm


def review_list(request):
    """
    Страница со всеми опубликованными отзывами.
    Поддерживает фильтр по оценке и сортировку.
    """
    reviews = Review.objects.filter(is_published=True).select_related(
        'user', 'product'
    ).prefetch_related('images')

    rating = request.GET.get('rating')
    if rating and rating.isdigit():
        reviews = reviews.filter(rating=int(rating))

    # Сортировка
    sort = request.GET.get('sort', 'newest')
    if sort == 'oldest':
        reviews = reviews.order_by('created_at')
    elif sort == 'positive':
        reviews = reviews.order_by('-rating', '-created_at')
    elif sort == 'negative':
        reviews = reviews.order_by('rating', '-created_at')
    else:
        reviews = reviews.order_by('-created_at')

    rating_counts = Review.objects.filter(is_published=True).values(
        'rating'
    ).annotate(count=Count('id'))
    counts = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for item in rating_counts:
        counts[item['rating']] = item['count']

    return render(request, 'reviews/list.html', {
        'reviews': reviews,
        'rating_counts': counts,
        'current_rating': rating,
        'current_sort': sort,
    })


@login_required
def review_create(request, product_id):
    """
    Создание отзыва на товар.
    """
    product = get_object_or_404(IceCream, id=product_id)

    if not can_review(request.user, product):
        messages.error(request, 'Вы не можете оставить отзыв на этот товар.')
        return redirect('ice_cream:ice_cream_detail', pk=product.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()

            # Сохраняем фото, если загружено
            image = form.cleaned_data.get('image')
            if image:
                ReviewImage.objects.create(review=review, image=image)

            messages.success(request, 'Спасибо за ваш отзыв!')
            return redirect('ice_cream:ice_cream_detail', pk=product.id)
    else:
        form = ReviewForm()

    return render(request, 'reviews/create.html', {
        'form': form,
        'product': product,
    })
