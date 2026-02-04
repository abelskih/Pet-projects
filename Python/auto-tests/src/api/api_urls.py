from src.utils.config import get_cloud_stage, get_domain

domain = get_domain()
cloud_stage = get_cloud_stage()

API_HOST = f"https://api{domain}/"
SEZAM_AUTH_LINK = f"https://auth-ac{domain}/"
API_CLOUD = f"https://userapi.{cloud_stage}cloud{domain}/api/"


api_urls = {
    "sezam": {"auth_link": f"{SEZAM_AUTH_LINK}api/v3/pub/auth/"},
    "cloud": {
        "cloud_link": API_CLOUD,
        "plans": f"{API_CLOUD}plans",
        "games": f"{API_CLOUD}games",
        "quests": f"{API_CLOUD}quests",
    },
}
