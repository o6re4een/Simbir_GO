from api.user_routes import router as router_users
from api.admin import router as router_admin


all_routers = [
    router_users,
    router_admin,
    # router_auth
]

