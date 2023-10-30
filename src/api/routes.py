from api.user_routes import router as router_users
from api.admin import router as router_admin
from api.payment_routes import router as router_payment

all_routers = [
    router_users,
    router_admin,
    router_payment
    # router_auth
]

