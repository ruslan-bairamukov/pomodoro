from handlers.ping import router as ping_router
from handlers.tasks import router as tasks_router


routers = [
    ping_router,
    tasks_router,
]
