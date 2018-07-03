

# -------------------------------------------------
# 段階式デコレータ実行クラス
class LeveledDecoratorExecutor:
    __name__ = 'LeveledDecoratorExecutor'

    def __init__(
            self,
            activator,
            pre_hook,
            post_hook,
            exception_handler
    ):
        self.activator = activator
        self.pre_hook = pre_hook
        self.post_hook = post_hook
        self.exception_handler = exception_handler
        self.func = None

    def set_function(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        if self.activator() and callable(self.pre_hook):
            self.pre_hook(*args, **kwargs)
        try:
            retval = self.func(*args, **kwargs)

            if self.activator() and callable(self.post_hook) and retval is not None:
                self.post_hook(retval)
                return retval
        except BaseException as e:
            if callable(self.exception_handler):
                self.exception_handler(e)


# -------------------------------------------------
# 段階式デコレータクラス
class LeveledDecorator:
    __name__ = 'LeveledDecorator'

    def __init__(
            self,
            activator,
            pre_hook,
            post_hook,
            exception_handler
    ):
        self.executor = LeveledDecoratorExecutor(activator, pre_hook, post_hook, exception_handler)

    def __call__(self, func):
        self.executor.set_function(func)
        return self.executor

