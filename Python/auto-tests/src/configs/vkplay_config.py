import os

COOKIEBOT_COOKIE = (
    "{stamp:%27hHF28yKWEim9/ziy8NTp6B3Mdy4R17WcjnujeKN99WX91fsvW9DYKg==%27%2Cnecessary:true"
    "%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cver:1%2Cutc:1619708498024%2Cregion:%27ru%27}"
)

USER_DATA = {
    "user_email_2": {
        "login": "secondtestdemo@yandex.ru",
        "password": "!QAZ2wsx",
        "nickname": "sdfsdfsdfsdfsdfsdfsdfsdfs",
    },
}

COOKIE_NAMES = ("mc", "ssdc", "sdcs")
WAIT_TIMEOUT = 10
ELEMENT_PRESENT_TIMEOUT = 5
GOOGLE_PLAY_LINK = "https://play.google.com/"
RUSTORE_LINK = "https://apps.rustore.ru"
domain = ""
path_to_cookies = os.path.join(os.path.abspath(os.getcwd()), "resources", "cookies.json")


class CloudLinks:
    class Apk:
        MOBILE_APK = "vkplay/Release/android-Phone/VK-play-cloud.apk"
        TV_APK = "vkplay/Release/android-TV/VK-play-cloud-TV.apk"

    class Pages:
        DASHBOARD = "dashboard"
        TASKS = DASHBOARD + "/tasks"
        PLANS = DASHBOARD + "/plans-page"
        SETTINGS = DASHBOARD + "/settings"
        DOWNLOAD = DASHBOARD + "/download"
        FAQ = DASHBOARD + "/faq"

    class Static:
        MAC = "gcmac"
