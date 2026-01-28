import os
import django
import random
from decimal import Decimal
from datetime import datetime, timedelta

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'house_kg.settings')
django.setup()

from house_app.models import UserProfile, Region, City, District, Property, PropertyImages, Review
from django.contrib.auth.hashers import make_password


def clear_data():
    """Очистка существующих данных"""
    print("Очистка базы данных...")
    try:
        Review.objects.all().delete()
        PropertyImages.objects.all().delete()
        Property.objects.all().delete()
        District.objects.all().delete()
        City.objects.all().delete()
        Region.objects.all().delete()
        UserProfile.objects.filter(is_superuser=False).delete()
        print("База данных очищена!\n")
    except Exception as e:
        print(f"Предупреждение при очистке: {e}")
        print("Продолжаем создание данных...\n")


def create_regions():
    """Создание регионов Кыргызстана"""
    print("Создание регионов...")
    regions_data = [
        {'ru': 'Бишкек', 'en': 'Bishkek', 'ky': 'Бишкек'},
        {'ru': 'Чуйская область', 'en': 'Chuy Region', 'ky': 'Чүй областы'},
        {'ru': 'Ошская область', 'en': 'Osh Region', 'ky': 'Ош областы'},
        {'ru': 'Джалал-Абадская область', 'en': 'Jalal-Abad Region', 'ky': 'Жалал-Абад областы'},
        {'ru': 'Иссык-Кульская область', 'en': 'Issyk-Kul Region', 'ky': 'Ысык-Көл областы'},
        {'ru': 'Нарынская область', 'en': 'Naryn Region', 'ky': 'Нарын областы'},
        {'ru': 'Таласская область', 'en': 'Talas Region', 'ky': 'Талас областы'},
        {'ru': 'Баткенская область', 'en': 'Batken Region', 'ky': 'Баткен областы'},
        {'ru': 'Ош', 'en': 'Osh', 'ky': 'Ош'},
    ]

    regions = []
    for region_data in regions_data:
        region = Region.objects.create(
            region_name=region_data['ru'],
            region_name_ru=region_data['ru'],
            region_name_en=region_data['en'],
            region_name_ky=region_data['ky']
        )
        regions.append(region)
    print(f"Создано {len(regions)} регионов\n")
    return regions


def create_cities(regions):
    """Создание городов"""
    print("Создание городов...")
    cities_data = {
        'Бишкек': [
            {'ru': 'Бишкек', 'en': 'Bishkek', 'ky': 'Бишкек'}
        ],
        'Чуйская область': [
            {'ru': 'Токмок', 'en': 'Tokmok', 'ky': 'Токмок'},
            {'ru': 'Кант', 'en': 'Kant', 'ky': 'Кант'},
            {'ru': 'Кара-Балта', 'en': 'Kara-Balta', 'ky': 'Кара-Балта'},
            {'ru': 'Ысык-Ата', 'en': 'Ysyk-Ata', 'ky': 'Ысык-Ата'},
            {'ru': 'Беловодское', 'en': 'Belovodskoye', 'ky': 'Беловодское'},
            {'ru': 'Сокулук', 'en': 'Sokuluk', 'ky': 'Сокулук'}
        ],
        'Ошская область': [
            {'ru': 'Кара-Суу', 'en': 'Kara-Suu', 'ky': 'Кара-Суу'},
            {'ru': 'Узген', 'en': 'Uzgen', 'ky': 'Өзгөн'},
            {'ru': 'Ноокат', 'en': 'Nookat', 'ky': 'Ноокат'},
            {'ru': 'Кара-Кульджа', 'en': 'Kara-Kulja', 'ky': 'Кара-Кулжа'},
            {'ru': 'Алай', 'en': 'Alai', 'ky': 'Алай'}
        ],
        'Джалал-Абадская область': [
            {'ru': 'Джалал-Абад', 'en': 'Jalal-Abad', 'ky': 'Жалал-Абад'},
            {'ru': 'Базар-Коргон', 'en': 'Bazar-Korgon', 'ky': 'Базар-Коргон'},
            {'ru': 'Таш-Кумыр', 'en': 'Tash-Kumyr', 'ky': 'Таш-Көмүр'},
            {'ru': 'Кок-Жангак', 'en': 'Kok-Jangak', 'ky': 'Көк-Жаңгак'},
            {'ru': 'Кара-Кол', 'en': 'Kara-Kol', 'ky': 'Кара-Кол'}
        ],
        'Иссык-Кульская область': [
            {'ru': 'Каракол', 'en': 'Karakol', 'ky': 'Каракол'},
            {'ru': 'Балыкчы', 'en': 'Balykchy', 'ky': 'Балыкчы'},
            {'ru': 'Чолпон-Ата', 'en': 'Cholpon-Ata', 'ky': 'Чолпон-Ата'},
            {'ru': 'Ак-Суу', 'en': 'Ak-Suu', 'ky': 'Ак-Суу'},
            {'ru': 'Тюп', 'en': 'Tyup', 'ky': 'Түп'}
        ],
        'Нарынская область': [
            {'ru': 'Нарын', 'en': 'Naryn', 'ky': 'Нарын'},
            {'ru': 'Ат-Башы', 'en': 'At-Bashy', 'ky': 'Ат-Башы'},
            {'ru': 'Кочкор', 'en': 'Kochkor', 'ky': 'Кочкор'}
        ],
        'Таласская область': [
            {'ru': 'Талас', 'en': 'Talas', 'ky': 'Талас'},
            {'ru': 'Кара-Буура', 'en': 'Kara-Buura', 'ky': 'Кара-Буура'},
            {'ru': 'Манас', 'en': 'Manas', 'ky': 'Манас'}
        ],
        'Баткенская область': [
            {'ru': 'Баткен', 'en': 'Batken', 'ky': 'Баткен'},
            {'ru': 'Кызыл-Кия', 'en': 'Kyzyl-Kiya', 'ky': 'Кызыл-Кыя'},
            {'ru': 'Сулюкта', 'en': 'Sulukta', 'ky': 'Сүлүктү'},
            {'ru': 'Исфана', 'en': 'Isfana', 'ky': 'Исфана'}
        ],
        'Ош': [
            {'ru': 'Ош', 'en': 'Osh', 'ky': 'Ош'}
        ],
    }

    cities = []
    for region in regions:
        region_name_ru = region.region_name_ru if hasattr(region, 'region_name_ru') else region.region_name
        if region_name_ru in cities_data:
            for city_data in cities_data[region_name_ru]:
                city = City.objects.create(
                    region=region,
                    city_name=city_data['ru'],
                    city_name_ru=city_data['ru'],
                    city_name_en=city_data['en'],
                    city_name_ky=city_data['ky']
                )
                cities.append(city)
    print(f"Создано {len(cities)} городов\n")
    return cities


def create_districts(cities):
    """Создание районов"""
    print("Создание районов...")
    districts_data = {
        'Бишкек': [
            {'ru': 'Ленинский', 'en': 'Leninsky', 'ky': 'Ленин'},
            {'ru': 'Первомайский', 'en': 'Pervomaisky', 'ky': 'Биринчи Май'},
            {'ru': 'Октябрьский', 'en': 'Oktyabrsky', 'ky': 'Октябрь'},
            {'ru': 'Свердловский', 'en': 'Sverdlovsky', 'ky': 'Свердлов'}
        ],
        'Ош': [
            {'ru': 'Центральный', 'en': 'Central', 'ky': 'Борбордук'},
            {'ru': 'Северный', 'en': 'Northern', 'ky': 'Түндүк'},
            {'ru': 'Южный', 'en': 'Southern', 'ky': 'Түштүк'},
            {'ru': 'Восточный', 'en': 'Eastern', 'ky': 'Чыгыш'}
        ],
        'Джалал-Абад': [
            {'ru': 'Центральный', 'en': 'Central', 'ky': 'Борбордук'},
            {'ru': 'Северный', 'en': 'Northern', 'ky': 'Түндүк'},
            {'ru': 'Южный', 'en': 'Southern', 'ky': 'Түштүк'}
        ],
        'Каракол': [
            {'ru': 'Центральный', 'en': 'Central', 'ky': 'Борбордук'},
            {'ru': 'Восточный', 'en': 'Eastern', 'ky': 'Чыгыш'},
            {'ru': 'Западный', 'en': 'Western', 'ky': 'Батыш'}
        ],
        'Токмок': [
            {'ru': 'Центральный', 'en': 'Central', 'ky': 'Борбордук'},
            {'ru': 'Северный', 'en': 'Northern', 'ky': 'Түндүк'},
            {'ru': 'Южный', 'en': 'Southern', 'ky': 'Түштүк'}
        ],
        'Кара-Балта': [
            {'ru': 'Центральный', 'en': 'Central', 'ky': 'Борбордук'},
            {'ru': 'Промышленный', 'en': 'Industrial', 'ky': 'Өнөр жай'}
        ],
        'Талас': [
            {'ru': 'Центральный', 'en': 'Central', 'ky': 'Борбордук'},
            {'ru': 'Западный', 'en': 'Western', 'ky': 'Батыш'}
        ],
        'Нарын': [
            {'ru': 'Центральный', 'en': 'Central', 'ky': 'Борбордук'}
        ],
        'Баткен': [
            {'ru': 'Центральный', 'en': 'Central', 'ky': 'Борбордук'}
        ],
    }

    default_districts = [
        {'ru': 'Центральный', 'en': 'Central', 'ky': 'Борбордук'},
        {'ru': 'Северный', 'en': 'Northern', 'ky': 'Түндүк'},
        {'ru': 'Южный', 'en': 'Southern', 'ky': 'Түштүк'}
    ]

    districts = []
    for city in cities:
        city_name_ru = city.city_name_ru if hasattr(city, 'city_name_ru') else city.city_name
        city_districts = districts_data.get(city_name_ru, default_districts)
        for district_data in city_districts:
            district = District.objects.create(
                city=city,
                district_name=district_data['ru'],
                district_name_ru=district_data['ru'],
                district_name_en=district_data['en'],
                district_name_ky=district_data['ky']
            )
            districts.append(district)
    print(f"Создано {len(districts)} районов\n")
    return districts


def create_users(count=50):
    """Создание пользователей"""
    print(f"Создание {count} пользователей...")

    first_names = [
        'Айбек', 'Бакыт', 'Данияр', 'Эрлан', 'Жаныбек', 'Кубат', 'Нурлан', 'Темир',
        'Айгуль', 'Гульнара', 'Жамиля', 'Нургуль', 'Салтанат', 'Айжан', 'Бермет', 'Динара',
        'Алексей', 'Дмитрий', 'Иван', 'Сергей', 'Елена', 'Наталья', 'Ольга', 'Светлана'
    ]

    last_names = [
        'Асанов', 'Бекмуратов', 'Джумабаев', 'Иманалиев', 'Касымов', 'Мамбетов', 'Орозбеков', 'Садыков',
        'Токтогулов', 'Усенов', 'Шаршеев', 'Эргешов', 'Иванов', 'Петров', 'Сидоров', 'Козлов'
    ]

    users = []
    for i in range(count):
        role = random.choice(['seller', 'buyer'])
        user = UserProfile.objects.create(
            username=f'user_{i + 1}',
            email=f'user{i + 1}@example.com',
            password=make_password('password123'),
            first_name=random.choice(first_names),
            last_name=random.choice(last_names),
            phone_number=f'+996{random.randint(500000000, 799999999)}',
            role=role,
            created_date=datetime.now().date() - timedelta(days=random.randint(1, 365))
        )
        users.append(user)

    print(f"Создано {len(users)} пользователей\n")
    return users


def create_properties(users, districts, count=150):
    """Создание объявлений о недвижимости"""
    print(f"Создание {count} объявлений...")

    # Проверка наличия районов
    if not districts:
        print("ОШИБКА: Нет районов для создания объявлений!")
        return []

    sellers = [u for u in users if u.role == 'seller']
    if not sellers:
        sellers = users[:10]
        for seller in sellers:
            seller.role = 'seller'
            seller.save()

    property_titles = {
        'apartment': {
            'ru': [
                '1-комнатная квартира в центре',
                '2-комнатная квартира с ремонтом',
                '3-комнатная квартира улучшенной планировки',
                'Студия в новостройке',
                'Квартира с панорамным видом',
                'Уютная квартира рядом с парком',
                'Светлая квартира в спальном районе',
                '4-комнатная квартира для большой семьи',
            ],
            'en': [
                '1-room apartment in the center',
                '2-room apartment with renovation',
                '3-room apartment with improved layout',
                'Studio in a new building',
                'Apartment with panoramic view',
                'Cozy apartment near the park',
                'Bright apartment in residential area',
                '4-room apartment for large family',
            ],
            'ky': [
                'Борбордогу 1-бөлмөлүү квартира',
                'Оңдолгон 2-бөлмөлүү квартира',
                'Жакшыртылган пландуу 3-бөлмөлүү квартира',
                'Жаңы үйдөгү студия',
                'Панорамалуу көрүнүштүү квартира',
                'Парктын жанындагы ыңгайлуу квартира',
                'Жашоочу райондогу жарык квартира',
                'Чоң үй-бүлөгө 4-бөлмөлүү квартира',
            ]
        },
        'house': {
            'ru': [
                'Дом с участком 6 соток',
                'Коттедж в элитном районе',
                'Уютный дом с садом',
                'Двухэтажный дом',
                'Дом с евроремонтом',
                'Загородный дом с бассейном',
                'Современный таунхаус',
            ],
            'en': [
                'House with 6 acres of land',
                'Cottage in elite area',
                'Cozy house with garden',
                'Two-story house',
                'House with European renovation',
                'Country house with pool',
                'Modern townhouse',
            ],
            'ky': [
                '6 сотих аянты бар үй',
                'Элиталык райондогу коттедж',
                'Бакчасы бар ыңгайлуу үй',
                'Эки кабаттуу үй',
                'Евро оңдолгон үй',
                'Бассейни бар загород үйү',
                'Заманбап таунхаус',
            ]
        },
        'area': {
            'ru': [
                'Участок под строительство',
                'Земельный участок 10 соток',
                'Участок в пригороде',
                'Земля в зеленой зоне',
            ],
            'en': [
                'Land for construction',
                'Land plot 10 acres',
                'Plot in the suburb',
                'Land in green zone',
            ],
            'ky': [
                'Куруулуш үчүн жер',
                '10 сотих жер',
                'Шаар четиндеги жер',
                'Жашыл аймактагы жер',
            ]
        },
        'commercial real estate': {
            'ru': [
                'Торговое помещение в центре',
                'Офис с отдельным входом',
                'Магазин на первой линии',
                'Складское помещение',
            ],
            'en': [
                'Commercial space in the center',
                'Office with separate entrance',
                'Shop on the first line',
                'Warehouse space',
            ],
            'ky': [
                'Борбордогу соода жайы',
                'Өзүнчө кире бериши бар офис',
                'Биринчи линиядагы дүкөн',
                'Кампа жайы',
            ]
        }
    }

    descriptions = {
        'apartment': {
            'ru': 'Продается {rooms}-комнатная квартира площадью {area} кв.м. на {floor} этаже {total_floor}-этажного дома. {condition_desc}. Развитая инфраструктура, рядом школы, детские сады, супермаркеты.',
            'en': '{rooms}-room apartment for sale with an area of {area} sq.m. on the {floor} floor of a {total_floor}-story building. {condition_desc}. Developed infrastructure, near schools, kindergartens, supermarkets.',
            'ky': '{rooms}-бөлмөлүү квартира сатылат, аянты {area} кв.м., {total_floor}-кабаттуу үйдүн {floor}-кабатында. {condition_desc}. Өнүккөн инфраструктура, мектептер, балдар бакчалары, супермаркеттер жакын.'
        },
        'house': {
            'ru': 'Продается {property_type} площадью {area} кв.м. на участке. {condition_desc}. Все коммуникации проведены. Тихий район, хорошие соседи.',
            'en': '{property_type} for sale with an area of {area} sq.m. on a plot. {condition_desc}. All utilities connected. Quiet area, good neighbors.',
            'ky': '{area} кв.м. аянтка ээ {property_type} сатылат. {condition_desc}. Бардык коммуникациялар киргизилген. Тынч район, жакшы кошуналар.'
        },
        'area': {
            'ru': 'Продается земельный участок площадью {area} соток. Подходит для строительства жилого дома. Все коммуникации рядом.',
            'en': 'Land plot for sale with an area of {area} acres. Suitable for residential construction. All utilities nearby.',
            'ky': '{area} сотих аянттагы жер сатылат. Турак үй курууга ылайыктуу. Бардык коммуникациялар жакын.'
        },
        'commercial real estate': {
            'ru': 'Продается коммерческое помещение площадью {area} кв.м. {condition_desc}. Отличное место для бизнеса, высокая проходимость.',
            'en': 'Commercial space for sale with an area of {area} sq.m. {condition_desc}. Great location for business, high traffic.',
            'ky': '{area} кв.м. аянтка ээ соода жайы сатылат. {condition_desc}. Бизнес үчүн мыкты жер, жогорку өтүү.'
        }
    }

    condition_descriptions = {
        'homemade': {
            'ru': 'Состояние домашнее, требуется косметический ремонт',
            'en': 'Home condition, cosmetic repair needed',
            'ky': 'Үй абалы, косметикалык оңдоо керек'
        },
        'renovation': {
            'ru': 'Сделан качественный евроремонт',
            'en': 'Quality European renovation done',
            'ky': 'Сапаттуу евро оңдоо жасалган'
        },
        'good': {
            'ru': 'Хорошее состояние',
            'en': 'Good condition',
            'ky': 'Жакшы абалда'
        },
        'average': {
            'ru': 'Среднее состояние',
            'en': 'Average condition',
            'ky': 'Орточо абалда'
        },
        'unfinished': {
            'ru': 'Требуется ремонт',
            'en': 'Repair needed',
            'ky': 'Оңдоо керек'
        }
    }

    streets = {
        'ru': ['Чуй', 'Манас', 'Киевская', 'Московская', 'Ибраимова', 'Жибек-Жолу', 'Исанова', 'Токтогула', 'Фрунзе',
               'Ахунбаева', 'Ленина', 'Советская', 'Гагарина', 'Горького'],
        'en': ['Chui', 'Manas', 'Kievskaya', 'Moskovskaya', 'Ibraimova', 'Jibek-Jolu', 'Isanova', 'Toktogula', 'Frunze',
               'Akhunbaeva', 'Lenina', 'Sovetskaya', 'Gagarina', 'Gorkogo'],
        'ky': ['Чүй', 'Манас', 'Киев', 'Москва', 'Ибраимов', 'Жибек-Жолу', 'Исанов', 'Токтогул', 'Фрунзе', 'Ахунбаев',
               'Ленин', 'Совет', 'Гагарин', 'Горький']
    }

    properties = []
    for i in range(count):
        property_type = random.choice(['apartment', 'house', 'area', 'commercial real estate'])
        condition = random.choice(['homemade', 'renovation', 'good', 'average', 'unfinished'])
        district = random.choice(districts)

        # Генерация параметров в зависимости от типа
        if property_type == 'apartment':
            rooms = random.choice([1, 1, 2, 2, 2, 3, 3, 4, 5])
            area = Decimal(str(random.randint(35, 150)))
            floor = random.randint(1, 16)
            total_floor = random.randint(floor, 16)
            price = random.randint(25000, 120000)
        elif property_type == 'house':
            rooms = random.choice([3, 4, 5, 6, 7, 8])
            area = Decimal(str(random.randint(80, 350)))
            floor = random.choice([1, 1, 2, 2, 3])  # Для домов: количество этажей дома
            total_floor = floor  # Для домов это то же самое
            price = random.randint(40000, 300000)
        elif property_type == 'area':
            rooms = 0  # Для участков нет комнат
            area = Decimal(str(random.randint(3, 20)))
            floor = 1  # Для участков можно указать 1
            total_floor = 1  # Для участков можно указать 1
            price = random.randint(10000, 100000)
        else:  # commercial
            rooms = random.randint(1, 10)
            area = Decimal(str(random.randint(30, 500)))
            floor = random.randint(1, 10)
            total_floor = random.randint(floor, 12)
            price = random.randint(50000, 500000)

        title = random.choice(property_titles[property_type]['ru'])
        title_en = random.choice(property_titles[property_type]['en'])
        title_ky = random.choice(property_titles[property_type]['ky'])

        condition_desc_ru = condition_descriptions[condition]['ru']
        condition_desc_en = condition_descriptions[condition]['en']
        condition_desc_ky = condition_descriptions[condition]['ky']

        property_type_word = {
            'ru': 'дом' if property_type == 'house' else 'помещение',
            'en': 'house' if property_type == 'house' else 'space',
            'ky': 'үй' if property_type == 'house' else 'жай'
        }

        description_ru = descriptions[property_type]['ru'].format(
            rooms=rooms,
            area=area,
            floor=floor,
            total_floor=total_floor,
            property_type=property_type_word['ru'],
            condition_desc=condition_desc_ru
        )

        description_en = descriptions[property_type]['en'].format(
            rooms=rooms,
            area=area,
            floor=floor,
            total_floor=total_floor,
            property_type=property_type_word['en'],
            condition_desc=condition_desc_en
        )

        description_ky = descriptions[property_type]['ky'].format(
            rooms=rooms,
            area=area,
            floor=floor,
            total_floor=total_floor,
            property_type=property_type_word['ky'],
            condition_desc=condition_desc_ky
        )

        street_ru = random.choice(streets['ru'])
        street_en = random.choice(streets['en'])
        street_ky = random.choice(streets['ky'])
        building_number = random.randint(1, 200)

        address_ru = f'ул. {street_ru}, {building_number}'
        address_en = f'{street_en} str., {building_number}'
        address_ky = f'{street_ky} көч., {building_number}'

        property_obj = Property.objects.create(
            title=title,
            title_ru=title,
            title_en=title_en,
            title_ky=title_ky,
            description=description_ru,
            description_ru=description_ru,
            description_en=description_en,
            description_ky=description_ky,
            property_type=property_type,
            region=district.city.region,
            city=district.city,
            district=district,
            address=address_ru,
            address_ru=address_ru,
            address_en=address_en,
            address_ky=address_ky,
            area=area,
            price=price,
            rooms=rooms,
            floor=floor,
            total_floor=total_floor,
            condition=condition,
            documents=random.choice([True, True, True, False]),
            seller=random.choice(sellers),
            created_date=datetime.now().date() - timedelta(days=random.randint(1, 180))
        )
        properties.append(property_obj)

    print(f"Создано {len(properties)} объявлений\n")
    return properties


def create_reviews(users, properties):
    """Создание отзывов - по 10-15 на каждое объявление"""
    print(f"Создание отзывов для {len(properties)} объявлений...")

    buyers = [u for u in users if u.role == 'buyer']
    if not buyers:
        buyers = users[10:20]
        for buyer in buyers:
            buyer.role = 'buyer'
            buyer.save()

    review_comments = [
        'Отличная квартира, очень довольны покупкой! Продавец адекватный, все прошло быстро.',
        'Хорошее предложение за свою цену. Рекомендую этого продавца.',
        'Все соответствует описанию. Спасибо за честность!',
        'Квартира понравилась, но торговаться не получилось. В целом неплохо.',
        'Отличное расположение, рядом вся инфраструктура. Советую!',
        'Продавец очень отзывчивый, показал все детали. Остались довольны.',
        'Нормальный вариант, но есть недочеты в ремонте.',
        'Прекрасная квартира в хорошем районе! Очень рады покупке.',
        'Цена немного завышена, но в целом устроило.',
        'Отличный продавец, все четко и по делу. Рекомендую!',
        'Смотрели несколько вариантов, этот оказался лучшим. Довольны!',
        'Продавец профессионал, помог с оформлением документов.',
        'Хорошая недвижимость, соответствует фотографиям.',
        'Район тихий, спокойный. Для семьи идеально подходит.',
        'Немного торговались, но пришли к компромиссу. Все хорошо.',
        'Быстро и без проблем провели сделку. Спасибо!',
        'Чистая, ухоженная квартира. Въехали сразу после покупки.',
        'Соседи хорошие, дом добротный. Рекомендую!',
        'За эти деньги отличный вариант. Не пожалели о покупке.',
        'Продавец честный, все рассказал как есть. Уважение!',
        'Ремонт свежий, техника новая. Очень понравилось!',
        'Немного дороговато, но качество того стоит.',
        'Удобная планировка, светлые комнаты. Советуем!',
        'Инфраструктура развита, до центра близко. Супер!',
        'Документы все в порядке, оформили быстро.',
        'Хороший вариант для инвестиций. Покупали для сдачи в аренду.',
        'Тихий двор, есть парковка. Это большой плюс!',
        'Рядом школа и детский сад. Для нас это важно было.',
        'Балкон с видом на горы - просто сказка!',
        'Теплая квартира, батареи греют хорошо.',
    ]

    reviews = []

    # Для каждого объявления создаем 10-15 отзывов
    for property_obj in properties:
        reviews_count = random.randint(10, 15)
        used_buyers = set()

        for i in range(reviews_count):
            # Выбираем покупателя, который еще не оставлял отзыв на это объявление
            available_buyers = [b for b in buyers if b.id not in used_buyers]

            # Если все покупатели уже оставили отзывы, начинаем заново
            if not available_buyers:
                available_buyers = buyers
                used_buyers.clear()

            buyer = random.choice(available_buyers)
            used_buyers.add(buyer.id)

            review = Review.objects.create(
                property=property_obj,
                author=buyer,
                seller=property_obj.seller,
                rating=random.choice([3, 3, 4, 4, 4, 5, 5, 5, 5]),
                comment=random.choice(review_comments),
                created_date=property_obj.created_date + timedelta(days=random.randint(1, 60))
            )
            reviews.append(review)

    print(f"Создано {len(reviews)} отзывов\n")
    return reviews


def main():
    """Главная функция"""
    print("=" * 50)
    print("Начало заполнения базы данных")
    print("=" * 50)
    print()

    # Очистка
    clear_data()

    # Создание данных
    regions = create_regions()  # 9 регионов
    cities = create_cities(regions)  # ~30 городов
    districts = create_districts(cities)  # ~50 районов
    users = create_users(50)  # 50 пользователей
    properties = create_properties(users, districts, 150)  # 150 объявлений
    reviews = create_reviews(users, properties)  # 10-15 отзывов на каждое объявление

    print("=" * 50)
    print("Заполнение базы данных завершено!")
    print("=" * 50)
    print(f"Регионов: {len(regions)}")
    print(f"Городов: {len(cities)}")
    print(f"Районов: {len(districts)}")
    print(f"Пользователей: {len(users)}")
    print(f"Объявлений: {len(properties)}")
    print(f"Отзывов: {len(reviews)}")
    print("=" * 50)


if __name__ == '__main__':
    main()