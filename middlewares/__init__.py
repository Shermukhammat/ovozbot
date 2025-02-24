from loader import dp
from .subscription import ForcedSubscribtion



if __name__ == 'middlewares':
    print("[Middleware set up] : True")
    dp.middleware.setup(ForcedSubscribtion())