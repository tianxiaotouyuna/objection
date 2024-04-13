from objection.state.connection import state_connection


def _should_be_quiet(args: list) -> bool:
    """
        Checks if --quiet is part of the 检查是否包含了"--quiet"参数。
        commands arguments. 命令参数。

        :param args:
        :return:
    """

    return '--quiet' in args


def ios_disable(args: list = None) -> None:
    """
        Starts a new objection job that hooks common classes and functions, 启动一个新的objection任务，该任务挂钩常见的类和函数，
        applying new logic in an attempt to bypass SSL pinning. 尝试应用新逻辑以绕过SSL锁定。

        :param args:
        :return:
    """

    api = state_connection.get_api()
    api.ios_pinning_disable(_should_be_quiet(args))
