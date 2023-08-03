from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate(request, obj, per_page):
    paginator = Paginator(obj, per_page)
    page = request.GET.get('page')
    try:
        paginated_obj = paginator.page(page)
    except PageNotAnInteger:
        paginated_obj = paginator.page(1)
        page = 1
    except EmptyPage:
        page = paginator.num_pages
        paginated_obj = paginator.page(paginator.num_pages)

    left_index = int(page)-2

    if left_index < 1:
        left_index = 1

    right_index = int(page)+2

    if right_index > paginator.num_pages:
        right_index = paginator.num_pages

    custom_range = range(left_index, right_index)

    return paginated_obj, custom_range