from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class EducationalProgram(models.Model):
    title = models.CharField("Название программы", max_length=200)
    description = models.TextField("Описание программы")

    class Meta:
        verbose_name = "Образовательная программа"
        verbose_name_plural = "Образовательные программы"

    def __str__(self):
        return self.title


class Person(models.Model):
        class Role(models.TextChoices):
            ME = "me", "Я"
            HEAD = "head", "Руководитель"
            MANAGER = "manager", "Менеджер"
            CLASSMATE = "classmate", "Сокурсник"

        fio = models.CharField("ФИО", max_length=200)
        role = models.CharField("Роль", max_length=20, choices=Role.choices)
        email = models.EmailField("Email")
        phone = models.CharField("Телефон", max_length=50, blank=True)
        city = models.CharField("Город", max_length=100, blank=True)
        photo = models.URLField("Фото", blank=True)
        program = models.ForeignKey(
            EducationalProgram,
            on_delete=models.CASCADE,
            related_name="people",
            null=True,
            blank=True,
        )

        class Meta:
            verbose_name = "Человек"
            verbose_name_plural = "Люди"
            ordering = ["role", "fio"]

        def __str__(self):
            return f"{self.fio} - {self.get_role_display()}"

class ProgramReview(models.Model):
    nickname = models.CharField("Ник комментатора", max_length=80)
    text = models.TextField("Содержание отзыва")
    rating = models.PositiveSmallIntegerField(
        "Оценка по десятибалльной шкале",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    created_at = models.DateTimeField("Дата отправки отзыва", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв об образовательной программе"
        verbose_name_plural = "Отзывы об образовательной программе"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.nickname}: {self.rating}/10"

class SitePage(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    slug = models.SlugField("Адрес страницы", unique=True)
    category = models.CharField("Категория", max_length=100)
    content = models.TextField("Уникальный контент страницы")
    order = models.PositiveIntegerField("Порядок", default=0)
    is_published = models.BooleanField("Опубликовано", default=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = "Страница сайта"
        verbose_name_plural = "Страницы сайта"
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

