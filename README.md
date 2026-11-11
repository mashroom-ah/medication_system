# «Мой приём» — ПР10: Django Admin и Django ORM

Проект учёта пользователей, лекарств, расписаний и фактической истории приёмов. Методичка описывает Roomly (Room/User/Booking), но исходный проект имеет другую предметную область. Поэтому требования ПР10 перенесены на реальные связанные сущности проекта без добавления искусственных таблиц:

| Сущность методички | Аналог в «Мой приём» | Обоснование связи |
|---|---|---|
| Room | Medicine | Справочник объекта, к которому относятся расписания |
| User | User | Пользователь системы |
| Booking | Schedule / Intake | Schedule связывает User и Medicine; Intake фиксирует результат по расписанию |

Ключевые связи: `User 1—N Schedule`, `Medicine 1—N Schedule`, `Schedule 1—N Intake`. Внешние ключи используют `PROTECT`.

## Установка и запуск

Из каталога, где находится `manage.py`:

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py check
python manage.py makemigrations --check
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Если PowerShell блокирует активацию:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Linux/macOS: `python3 -m venv .venv`, `source .venv/bin/activate`, затем те же команды через `python`.

Откройте `http://127.0.0.1:8000/` и `http://127.0.0.1:8000/admin/`. Для Debug Toolbar пакет устанавливается из `requirements.txt`; при `DEBUG=True` и локальном запросе появится панель.

## Миграции и сохранность данных

В ПР10 добавлены миграции:

- `intakes.0003_intake_status_choices`: создаёт поле `status`, переносит `taken=True` в `taken`, `taken=False` в `missed`, затем удаляет старое поле `taken`;
- `schedules.0003_schedule_total_minutes`: добавляет вычисляемый столбец `total_minutes`;
- `medicines.0003_medicine_slug`: добавляет `slug` и заполняет его уникальными значениями для уже существующих лекарств.

**Перед миграцией сделайте копию `db.sqlite3`.** Существующие миграции не удалять и не пересоздавать. После обновления исходников выполните `python manage.py migrate`: Django применит только три новые миграции. Не запускайте `makemigrations` для ручного создания дублей — миграционные файлы уже включены в архив.

Старые данные о факте приёма не теряются: data migration копирует значения boolean в статус. Совместимое свойство `Intake.taken` оставлено для старых шаблонов, но ORM-фильтры и новые записи должны использовать `status`.

## ПР10 — реализация по разделам и пунктам таблицы 6.6

### 1. Пункт 5.2 — административная панель

Зарегистрированы все модели `User`, `Medicine`, `Schedule`, `Intake`. Настроены `ModelAdmin`, `list_display`, `search_fields`, `list_filter`, `ordering`, `list_per_page`, `list_select_related`, русские подписи и заголовки сайта. Inline-связи отражают структуру данных: расписания в карточках пользователя и лекарства; история приёмов в карточке расписания. Счётчики связей используют `annotate(Count(...))`.

Адаптация: вместо Room/User/Booking используются User/Medicine/Schedule/Intake. В админке статус приёма редактируется через `TextChoices`.

### 2. Пункт 5.3 — Django ORM

Реализованы и используются `all`, `filter`, `exclude`, `get_object_or_404`, `Q`, `order_by`, срезы QuerySet, `values`, `select_related`, `Exists`, `OuterRef`, `F`, `annotate`, `aggregate`, `Count`, `Avg`, `Min`, `Max`, `Paginator`. Каталог лекарств фильтруется по имени/единице и дозировке, история — по дате, статусу, конкретному пользователю и конкретному лекарству; поиск работает по имени пользователя/лекарства. История поддерживает сортировку по дате, пользователю и лекарству и пагинацию. Статистика рассчитывается по связанным таблицам.

### 3. Пункт 5.4.1 — Django Debug Toolbar

Зависимость `django-debug-toolbar` вынесена в отдельную строку `requirements.txt`. При установленном пакете и `DEBUG=True` добавляются приложение, middleware, `INTERNAL_IPS` и маршрут `/__debug__/`. При отсутствии пакета сайт всё ещё может стартовать, но для выполнения проверки Toolbar пакет обязателен.

### 4. Пункт 5.4.2 — оптимизация запросов и F()

Списки расписаний и истории используют `select_related` по связям, а счётчики — `annotate`. В расписаниях применены `F("hour") * 60 + F("minute")` и `Exists` для статуса на текущую дату. `Schedule.total_minutes` — вычисляемый столбец БД. Тест `test_select_related_avoids_n_plus_one` проверяет получение связанных user/medicine одним SQL-запросом. Для визуального сравнения SQL до/после используйте Debug Toolbar на `/schedules/` и `/intakes/`.

### 5. Пункт 5.4.3 — TextChoices и QuerySet Manager

У `Intake` добавлено перечисление `Status` (`TAKEN`, `MISSED`, `SKIPPED`) и `IntakeQuerySet` с методами `taken()`, `missed()`, `skipped()`, `for_date(date)`. Миграция переносит старое поле `taken` в новое поле `status` и удаляет прежнее поле. Тесты проверяют методы менеджера и совместимое свойство `taken`.

Адаптация: вместо статусов Booking используются статусы фактического приёма лекарства; значения описывают доменную логику проекта, а не бронирование.

### 6. Пункт 5.4.4 — GeneratedField

В `Schedule` добавлены два поля `GeneratedField`: `total_minutes` (`hour * 60 + minute`) и булев `is_night` (22:00–05:59). Второе поле — адаптация учебного вычисляемого признака: оно выводится из полей той же строки и не редактируется вручную. База пересчитывает значения при изменении `hour`/`minute`; тесты проверяют пересчёт через `refresh_from_db()`. Миграция `schedules.0003_schedule_total_minutes` создаёт оба generated columns. SQLite должен поддерживать generated columns (версия 3.31 или новее; проверить можно командой `python -c "import sqlite3; print(sqlite3.sqlite_version)"`).

### 7. Пункт 5.4.5 — SlugField и get_absolute_url()

В `Medicine` добавлено уникальное ASCII-поле `slug`; библиотека `Unidecode` транслитерирует русские названия в латиницу, а `slugify()` нормализует их. `save()` автоматически генерирует slug для новых записей и добавляет суффикс при совпадении. Миграция заполняет slug существующим записям, добавляя ID для уникальности. `get_absolute_url()` возвращает адрес `/medicines/<slug>/`; подробная страница получает объект через `get_object_or_404`. Карточки каталога и Django Admin используют `get_absolute_url()`; в админке есть публичная ссылка. Тест проверяет открытие страницы по URL и 404 для неизвестного slug.

### 8. Пункт 5.4.6 — контекстный процессор

Создан `homepage.context_processors.room_context` — адаптация обязательного `room_context` к предметной области приложения. Он возвращает заголовок «Мой приём» и актуальное количество лекарств. Зарегистрирован в `TEMPLATES[...]["OPTIONS"]["context_processors"]` и используется в общем шаблоне `base.html`. Запрос ограничен `count()` и не загружает все объекты.

### 9. Пункт 6.1 — проверка Admin

Автоматический тест проверяет регистрацию моделей. Ручная проверка: открыть `/admin/`, открыть списки User/Medicine/Schedule/Intake, проверить поиск, фильтры, сортировку, пагинацию и inline на карточках. Проверить, что названия интерфейса русские.

### 10. Пункт 6.2 — проверка ORM

Добавлены тесты статусов QuerySet, связей, slug URL, generated field, 404, статистики и отсутствия N+1 для связанного чтения. Для ручного подтверждения выполните shell-сценарии ниже и проверьте результаты на собственных данных.

### 11. Пункт 6.3 — пользовательские сценарии

Сохранены и проверяются маршруты главной страницы, каталога и карточки лекарства, списка и карточки расписания, истории приёмов и статистики. Фильтрация истории поддерживает дату, статус, выбранного пользователя, выбранное лекарство и поиск по связанным полям; каталог поддерживает поиск, минимальную дозировку, сортировку и пагинацию. Несуществующие подробные записи возвращают 404.

### 12. Пункт 6.4 — качество, тесты и миграции

Добавлены/обновлены тесты; `requirements.txt` исправлен (каждая зависимость на отдельной строке, добавлен `pytest-django`). Выполните `check`, `makemigrations --check`, `migrate`, `test`, `pytest` и Flake8. Перед коммитом проверьте `git status` и `git diff`; не включайте `.venv`, секреты и локальные копии БД.

## Django Shell — демонстрация ORM (пункты 5.3, 5.4.3 и 6.2)

```powershell
python manage.py shell
```

```python
from datetime import date
from django.db.models import Q, Count, Avg, F
from homepage.models import User
from medicines.models import Medicine
from schedules.models import Schedule
from intakes.models import Intake

# all / filter / exclude / order_by / срез
User.objects.all()
User.objects.filter(age__gte=18)
User.objects.exclude(age__gte=18)
Medicine.objects.filter(Q(name__icontains="витамин") | Q(unit__iexact="мг")).order_by("name")[:10]

# get и filter
Medicine.objects.get(pk=1)            # один объект или исключение
Medicine.objects.filter(dosage__gte=100)  # QuerySet, в том числе пустой

# фильтрация по связанным моделям и select_related
Schedule.objects.select_related("user", "medicine").filter(user__name__icontains="ан")
Intake.objects.select_related("schedule__user", "schedule__medicine").filter(schedule__medicine__name__icontains="витамин")

# QuerySet manager и статусы
Intake.objects.taken()
Intake.objects.missed()
Intake.objects.skipped()
Intake.objects.for_date(date.today())

# F, annotate и aggregate
Schedule.objects.annotate(minutes=F("hour") * 60 + F("minute")).values("id", "minutes")
Medicine.objects.annotate(schedule_count=Count("schedules")).order_by("-schedule_count")
Schedule.objects.annotate(intake_count=Count("intakes")).aggregate(avg=Avg("intake_count"))

# GeneratedField и абсолютный URL
schedule = Schedule.objects.select_related("user", "medicine").first()
if schedule:
    print(schedule.total_minutes, schedule.is_night)
    schedule.hour = 23
    schedule.save(update_fields=["hour"])
    schedule.refresh_from_db()
    print(schedule.total_minutes, schedule.is_night)  # is_night=True
medicine = Medicine.objects.first()
if medicine:
    print(medicine.get_absolute_url())
```

`pk=1` в примере `get()` замените на реально существующий ID; если такого объекта нет, `DoesNotExist` является ожидаемым поведением.

## Проверка SQL и Debug Toolbar

1. Запустите сервер: `python manage.py runserver`.
2. Откройте `/schedules/`, `/intakes/`, затем `/statistics/`.
3. В панели Debug Toolbar выберите SQL.
4. На списках проверьте, что связанные `User`, `Medicine` и `Schedule` извлекаются JOIN-запросами, а не отдельным запросом на каждую строку.
5. Откройте подробную страницу расписания и истории приёма, сравните SQL и число запросов.
6. Сравните список до/после `select_related` только в экспериментальном shell-запросе; не удаляйте оптимизацию из рабочего кода.

## Команды финальной проверки

```powershell
python manage.py check
python manage.py makemigrations --check
python manage.py showmigrations
python manage.py migrate
python manage.py test
python -m pytest -v
python -m flake8 homepage medicines schedules intakes medication_site manage.py
```

Успешный результат: `check` без ошибок, `makemigrations --check` сообщает `No changes detected`, все миграции отмечены `[X]`, тесты завершаются `OK`/`passed`, Flake8 не выводит замечаний.

## Ручной чек-лист для защиты

- [ ] `/admin/`: все четыре модели видны; поиск, фильтры, сортировка и inline работают.
- [ ] На странице User видны расписания; на Medicine — связанные расписания; на Schedule — Intake.
- [ ] `/medicines/`: поиск, минимальная дозировка, сортировка, пагинация; открыть карточку лекарства и проверить slug URL.
- [ ] `/schedules/`: список отсортирован по времени, связанные пользователь/лекарство отображаются корректно.
- [ ] `/intakes/`: фильтр по дате, статусу `taken/missed/skipped`, поиск по имени и лекарству, пагинация.
- [ ] `/statistics/`: числа и агрегаты меняются после добавления тестовой записи.
- [ ] Несуществующий slug лекарства, ID расписания и ID приёма дают HTTP 404.
- [ ] Debug Toolbar отображает SQL на локальных страницах.
- [ ] `git status` и `git diff` проверены; миграции и исходники включены в коммит.

Файл `.flake8` исключает автоматически созданные каталоги миграций из проверки стиля; исходные Python-модули приложений проверяются с ограничением 100 символов.

## Git

```bash
# Если проект ещё не является Git-репозиторием:
git init
# Затем:
git status
git diff
git add homepage medicines schedules intakes medication_site templates requirements.txt README.md pytest.ini PR10_REPORT.md
git commit -m "PR10: Django Admin, ORM и оптимизация связанных запросов"
```
