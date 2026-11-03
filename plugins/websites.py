from core.plugin_loader import best_phrase

CONVERTER = "https://yandex.ru/search/?text=конвертер+валют+из+гривен+в+рубли&lr=194&clid=11528081&src=suggest_Pers"
TRUDVSEM = "https://trudvsem.ru/auth/candidate/"
REP4REP = "https://rep4rep.com/commentlist/1/0/subscribed"
GDZ_RU = "https://reshutka.ru/8klass/russkiy/barhudarov/"
DNEVNIK = "https://dnevnik.ru/r/saratov/marks"

WEBSITES = {
    "открой ютуб": "https://youtube.com",
    "ютуб открой": "https://youtube.com",
    "открой гугл": "https://google.com",

    "открой чанга по": "https://chatgpt.com",
    "открой чат же пяти": "https://chatgpt.com",
    "открой чат кгб": "https://chatgpt.com",
    "чат же пяти открой": "https://chatgpt.com",

    "открой твич": "https://twitch.tv",
    "открой вич": "https://twitch.tv",
    "вич открой": "https://twitch.tv",
    "твие открой": "https://twitch.tv",
    "открой твие": "https://twitch.tv",

    "открой переводчику": "https://translate.yandex.ru",
    "открой переводчик": "https://translate.yandex.ru",
    "переводчик открой": "https://translate.yandex.ru",

    "открой дип сик": "https://chat.deepseek.com",
    "дип сик открой": "https://chat.deepseek.com",
    "ди сик открой": "https://chat.deepseek.com",
    "дикси к открой": "https://chat.deepseek.com",

    "открой дневник": DNEVNIK,
    "открой дневник ру": DNEVNIK,
    "дневник открой": DNEVNIK,
    "дневник ру открой": DNEVNIK,

    "открой озон": "https://www.ozon.ru",
    "открой озона": "https://www.ozon.ru",
    "озон открой": "https://www.ozon.ru",
    "озона открой": "https://www.ozon.ru",

    "открой года знаю": "https://gdz.ru",
    "открой года за": "https://gdz.ru",
    "открой года": "https://gdz.ru",
    "открой гдз": "https://gdz.ru",
    "года за открой": "https://gdz.ru",

    "открой гдз русскому": GDZ_RU,
    "открой года за по русскому": GDZ_RU,
    "года за по узкому открой": GDZ_RU,
    "года за по русскому открой": GDZ_RU,

    "открой почту": "https://mail.yandex.ru",
    "почту открой": "https://mail.yandex.ru",

    "открой макс": "https://web.max.ru",
    "макс открой": "https://web.max.ru",

    "открой расписание": "https://солярис64.рф/расписание/",
    "расписание открой": "https://солярис64.рф/расписание/",

    "открой фан по эй": "https://funpay.com",
    "открой айфон по и": "https://funpay.com",
    "фан открой": "https://funpay.com",

    "открой авито": "https://www.avito.ru",
    "открой вита": "https://www.avito.ru",
    "авито открой": "https://www.avito.ru",
    "вито открой": "https://www.avito.ru",

    "открой карты": "https://yandex.ru/maps",
    "карты открой": "https://yandex.ru/maps",
    "яндекскарты открой": "https://yandex.ru/maps",
    "открой яндекскарты": "https://yandex.ru/maps",

    "открой грок": "https://grok.com",
    "открой игрок": "https://grok.com",
    "грок открой": "https://grok.com",
    "грог открой": "https://grok.com",

    "днс открой": "https://www.dns-shop.ru",
    "открой донец": "https://www.dns-shop.ru",
    "донец открой": "https://www.dns-shop.ru",
    "открой до нас": "https://www.dns-shop.ru",
    "открой днс": "https://www.dns-shop.ru",
    "открой донёс": "https://www.dns-shop.ru",

    "дота маркет открой": "https://market.dota2.net",
    "открой дота маркет": "https://market.dota2.net",
    "маркет дота открой": "https://market.dota2.net",

    "открой а затем": "https://lzt.market",
    "открой л затем": "https://lzt.market",
    "зато открой": "https://lzt.market",

    "коллектор шопа открой": "https://collector.shop",
    "открой коллектора шоб": "https://collector.shop",
    "открой коллектора шоп": "https://collector.shop",

    "открой конвертер валют": CONVERTER,
    "конвертор валют открой": CONVERTER,

    "пополни стим": "https://store.steampowered.com",
    "пополни с тим": "https://store.steampowered.com",
    "пополни стин": "https://store.steampowered.com",
    "стим пополни": "https://store.steampowered.com",
    "стин пополни": "https://store.steampowered.com",

    "открой гугл диск": "https://drive.google.com/drive/home",
    "открой гугл диска": "https://drive.google.com/drive/home",
    "гугл диск открой": "https://drive.google.com/drive/home",
    "гугл диска открой": "https://drive.google.com/drive/home",

    "открой ситилинк": "https://www.citilink.ru",
    "ситилинк открой": "https://www.citilink.ru",

    "открой труд всем": TRUDVSEM,
    "труд всем открой": TRUDVSEM,
    "открой работа россию": TRUDVSEM,
    "открой работа россии": TRUDVSEM,
    "открой работы россии": TRUDVSEM,
    "работа россию открой": TRUDVSEM,
    "работа россии открой": TRUDVSEM,
    "работы россия открой": TRUDVSEM,
    "открой работу россии": TRUDVSEM,

    "открой вы к": "https://vk.com",
    "вы к открой": "https://vk.com",
    "открой века": "https://vk.com",
    "века открой": "https://vk.com",

    "с генерируют пароль": "https://randomus.ru/password",
    "сгенерируй пароль": "https://randomus.ru/password",
    "сгенерировать пароль": "https://randomus.ru/password",
    "пароль с генерирует": "https://randomus.ru/password",

    "реп фор реп открой": REP4REP,
    "открой реп фо реп": REP4REP,
    "рэп рэп открой": REP4REP,
}

PHRASES = list(WEBSITES)


def run(jarvis, text):
    phrase, _ = best_phrase(text, WEBSITES)
    url = WEBSITES[phrase]
    print("🌐 OPEN WEBSITE:", url)
    jarvis.open.url(url)
    jarvis.done()
    return True