from api.user_routes import router as router_users
from api.admin import router as router_admin
from api.payment_routes import router as router_payment
from api.transport_routes import router as router_transport
from api.admin_transport import router as router_transport_admin

all_routers = [
    router_users,
    router_admin,
    router_payment,
    router_transport,
    router_transport_admin
    # router_auth
]

