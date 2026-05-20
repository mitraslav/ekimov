from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProgramReviewForm
from .models import EducationalProgram, Person, ProgramReview, SitePage


def home(request):
    return render(request, "home.html")

def info1(request):
    return render(request, "info1.html")

def info2(request):
    return render(request, "info2.html")

def task13(request):
    companies_raw = request.GET.get("companies", "")
    days_raw = request.GET.get("days", "")
    max_days_raw = request.GET.get("max_days", "")

    result = []
    error = ""

    if companies_raw and days_raw and max_days_raw:
        companies = companies_raw.split()
        try:
            days = list(map(int, days_raw.split()))
            max_days = int(max_days_raw)

            if len(companies) != len(days):
                error = "Количество компаний должно совпадать с количеством дней."
            else:
                for name, d in zip(companies, days):
                    if d <= max_days:
                        result.append(name)
        except ValueError:
            error = "Проверь: поля 'дни' и 'максимум дней' должны быть целыми числами."

    context = {
        "companies_raw": companies_raw,
        "days_raw": days_raw,
        "max_days_raw": max_days_raw,
        "result": result,
        "error": error,
    }
    return render(request, "task13.html", context)

def education(request):
    program = EducationalProgram.objects.first()
    me = Person.objects.filter(role=Person.Role.ME).first()
    head = Person.objects.filter(role=Person.Role.HEAD).first()
    manager = Person.objects.filter(role=Person.Role.MANAGER).first()
    classmates = Person.objects.filter(role=Person.Role.CLASSMATE)

    city_filter = request.GET.get("city", "")
    sort = request.GET.get("sort", "fio")

    if city_filter:
        classmates = classmates.filter(city__icontains=city_filter)

    allowed_sorts = {
        "fio": "fio",
        "city": "city",
        "email": "email",
    }
    classmates = classmates.order_by(allowed_sorts.get(sort, "fio"))

    cities = (
        Person.objects
        .filter(role=Person.Role.CLASSMATE)
        .exclude(city="")
        .values_list("city", flat=True)
        .distinct()
    )

    context = {
        "program": program,
        "me": me,
        "head": head,
        "manager": manager,
        "classmates": classmates,
        "cities": cities,
        "city_filter": city_filter,
        "sort": sort,
    }
    return render(request, "education.html", context)

def reviews(request):
    if request.method == "POST":
        form = ProgramReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("reviews")
    else:
        form = ProgramReviewForm()

    sort = request.GET.get("sort", "-created_at")
    min_rating = request.GET.get("min_rating", "")

    reviews_qs = ProgramReview.objects.all()

    if min_rating:
        reviews_qs = reviews_qs.filter(rating__gte=min_rating)

    allowed_sorts = {
        "-created_at": "-created_at",
        "created_at": "created_at",
        "-rating": "-rating",
        "rating": "rating",
        "nickname": "nickname",
    }
    reviews_qs = reviews_qs.order_by(allowed_sorts.get(sort, "-created_at"))

    stats = ProgramReview.objects.aggregate(
        count=Count("id"),
        average_rating=Avg("rating"),
    )

    rating_groups = (
        ProgramReview.objects
        .values("rating")
        .annotate(count=Count("id"))
        .order_by("-rating")
    )

    return render(
        request,
        "reviews.html",
        {
            "form": form,
            "reviews": reviews_qs,
            "sort": sort,
            "min_rating": min_rating,
            "stats": stats,
            "rating_groups": rating_groups,
        }
    )

def site_pages(request):
    pages = SitePage.objects.filter(is_published=True)

    category = request.GET.get("category", "")
    sort = request.GET.get("sort", "order")

    if category:
        pages = pages.filter(category__icontains=category)

    allowed_sorts = {
        "order": "order",
        "title": "title",
        "category": "category",
        "-updated_at": "-updated_at",
    }
    pages = pages.order_by(allowed_sorts.get(sort, "order"))

    categories = (
        SitePage.objects
        .filter(is_published=True)
        .values_list("category", flat=True)
        .distinct()
    )

    category_stats = (
        SitePage.objects
        .filter(is_published=True)
        .values("category")
        .annotate(count=Count("id"))
        .order_by("category")
    )

    return render(
        request,
        "site_pages.html",
        {
            "pages": pages,
            "categories": categories,
            "category": category,
            "sort": sort,
            "category_stats": category_stats,
        },
    )

def site_page_detail(request, slug):
    page = get_object_or_404(SitePage, slug=slug, is_published=True)
    return render(request, "site_page_detail.html", {"page": page})

def requirements(request):
    requirements_blocks = [
        {
            "title": "Приложение 1",
            "items": [
                "Модели о себе, руководстве, менеджере и сокурсниках",
                "Форма отзывов с сохранением в базе данных",
                "Табличное представление данных",
                "Фильтрация и сортировка сокурсников и отзывов",
                "Агрегированная статистика по оценкам отзывов",
                "Единая навигация",
            ],
        },
        {
            "title": "Приложение 2–3",
            "items": [
                "Уникальные страницы сайта хранятся в модели SitePage",
                "Управление контентом через Django admin",
                "Фильтрация и сортировка страниц",
                "Табличное представление страниц",
            ],
        },
    ]
    return render(request, "requirements.html", {"blocks": requirements_blocks})
# def education(request):
#     me = {
#         "fio": "Слава Екимова",
#         "email": "slava@edu.hse.ru",
#         "phone": "+7-900-000-00-00",
#         "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Guerin_Morpheus%26Iris1811.jpg/500px-Guerin_Morpheus%26Iris1811.jpg",
#     }
#
#     program = {
#         "title": "ОП Психология",
#         "description": "Учит понимать нелогичное поведение людей",
#         "head": {
#             "fio": "Александр Вечерин",
#             "email": "vecherin@edu.hse.ru",
#             "photo": "https://www.msses.ru/upload/resize_cache/iblock/6d4/450_500_2821712164bebe8964a3cb4f91f48bb72/Vecherin-A.V.-_-prepodavatel.png",
#         },
#         "manager": {
#             "fio": "Наталья Калинина",
#             "email": "calinina@edu.hse.ru",
#             "photo": "https://social.hse.ru/org/persons/cimage/208501856",
#         },
#     }
#
#     classmates = [
#         {
#             "fio": "Виктор Гюго",
#             "email": "hugo@edu.hse.ru",
#             "phone": "+7-900-111-11-11",
#             "city": 'Moscow',
#             "photo": "https://img.labirint.ru/images/descriptions/1207053068.jpg",
#         },
#         {
#             "fio": "Брэм Стокер",
#             "email": "stoker@edu.hse.ru",
#             "phone": "+7-900-222-22-22",
#             "city": 'Moscow',
#             "photo": "https://fantlab.ru/images/autors/335",
#         },
#     ]

    # return render(
    #     request,
    #     "education.html",
    #     {"me": me, "program": program, "classmates": classmates},
    # )


# def requirements(request):
#     requirements_blocks = [
#         {
#             "title": "Я и моя образовательная программа",
#             "items": [
#                 "Я (ФИО, фото, электронка, телефон)",
#                 "Название программы",
#                 "Описание программы",
#                 "Руководитель (ФИО, фото, электронка)",
#                 "Менеджер (ФИО, фото, электронка)",
#                 "Мои сокурсники (ФИО, фото, электронка, телефон)",
#                 "Данные получать из словарей, внедрённых в код",
#             ],
#         }
#     ]
#     return render(request, "requirements.html", {"blocks": requirements_blocks})