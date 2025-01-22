from handlers.auth import router as auth_router
from handlers.ping import router as ping_router
from handlers.tasks import router as tasks_router
from handlers.user import router as user_router

routers = [
    auth_router,
    ping_router,
    tasks_router,
    user_router,
]
