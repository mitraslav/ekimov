from django.shortcuts import render

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
    me = {
        "fio": "Слава Екимова",
        "email": "slava@edu.hse.ru",
        "phone": "+7-900-000-00-00",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Guerin_Morpheus%26Iris1811.jpg/500px-Guerin_Morpheus%26Iris1811.jpg",
    }

    program = {
        "title": "ОП Психология",
        "description": "Учит понимать нелогичное поведение людей",
        "head": {
            "fio": "Александр Вечерин",
            "email": "vecherin@edu.hse.ru",
            "photo": "https://www.msses.ru/upload/resize_cache/iblock/6d4/450_500_2821712164bebe8964a3cb4f91f48bb72/Vecherin-A.V.-_-prepodavatel.png",
        },
        "manager": {
            "fio": "Наталья Калинина",
            "email": "calinina@edu.hse.ru",
            "photo": "https://social.hse.ru/org/persons/cimage/208501856",
        },
    }

    classmates = [
        {
            "fio": "Виктор Гюго",
            "email": "hugo@edu.hse.ru",
            "phone": "+7-900-111-11-11",
            "city": 'Moscow',
            "photo": "https://img.labirint.ru/images/descriptions/1207053068.jpg",
        },
        {
            "fio": "Брэм Стокер",
            "email": "stoker@edu.hse.ru",
            "phone": "+7-900-222-22-22",
            "city": 'Moscow',
            "photo": "https://fantlab.ru/images/autors/335",
        },
    ]

    return render(
        request,
        "education.html",
        {"me": me, "program": program, "classmates": classmates},
    )

def requirements(request):
    requirements_blocks = [
        {
            "title": "Я и моя образовательная программа",
            "items": [
                "Я (ФИО, фото, электронка, телефон)",
                "Название программы",
                "Описание программы",
                "Руководитель (ФИО, фото, электронка)",
                "Менеджер (ФИО, фото, электронка)",
                "Мои сокурсники (ФИО, фото, электронка, телефон)",
                "Данные получать из словарей, внедрённых в код",
            ],
        }
    ]
    return render(request, "requirements.html", {"blocks": requirements_blocks})