from remilia.utils.LeveledDecorator import LeveledDecorator


# ----------------------------------------
# ログレベル
#
class LogLevel:
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4


class LogHelper:
    logLevel = LogLevel.INFO

    @staticmethod
    def set_level(level):
        LogHelper.logLevel = level

    @staticmethod
    def check(level):
        return level >= LogHelper.logLevel

    @staticmethod
    def activator(level):
        def activate():
            return LogHelper.check(level)
        return activate

    @staticmethod
    def log(level, msg):
        if LogHelper.check(level):
            print(msg)

    # ------------------------------------------------------
    # 引数を出力する関数
    @staticmethod
    def dump(*args, **kwargs):
        print('-- ARGUMENTS DUMP --')
        for arg in args:
            print("[args]: {}".format(arg))

        for key in kwargs:
            print("[kwargs]: {}={}". format(key, kwargs[key]))

    # ------------------------------------------------------
    # 何もしない関数
    @staticmethod
    def silent(*args, **kwargs):
        pass

    # ------------------------------------------------------
    # 例外を送出する関数
    @staticmethod
    def exception_escalator(e):
        raise e


# -------------------------------------------------
# ロギングデコレータ（infoレベル）
def info(
        pre_hook=LogHelper.silent,
        post_hook=LogHelper.silent,
        exception_handler=LogHelper.exception_escalator
):
    return LeveledDecorator(LogHelper.activator(LogLevel.INFO), pre_hook, post_hook, exception_handler)


# -------------------------------------------------
# ロギングデコレータ（debugレベル）
def debug(
        pre_hook=LogHelper.silent,
        post_hook=LogHelper.silent,
        exception_handler=LogHelper.exception_escalator
):
    return LeveledDecorator(LogHelper.activator(LogLevel.DEBUG), pre_hook, post_hook, exception_handler)
