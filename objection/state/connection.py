class StateConnection(object):
    """ 一个控制设备连接状态的类。 """

    def __init__(self) -> None:
        """
           初始化一个新的连接状态，默认为USB连接。
        """

        self.network = False
        self.host = None
        self.port = None
        self.device_type = 'usb'
        self.device_id = None

        self.spawn = False
        self.no_pause = False
        self.foremost = False
        self.debugger = False

        self.name = None
        self.agent = None
        self.api = None
        self.uid = None

    def use_usb(self) -> None:
        """
            设置所需的值以建立USB连接。

            :return:
        """

        self.network = False
        self.device_type = 'usb'

    def use_network(self) -> None:
        """
             设置需要建立网络连接的值。

            :return:
        """

        self.network = True
        self.device_type = 'remote'

    def get_comms_type(self) -> int:
        """
            返回当前配置的连接类型。

            :return:
        """

    def get_api(self):
        """
            返回当前配置的连接类型。
            
            :return:
        """

        if not self.agent:
            raise Exception('No session available to get API\n没有可用的会话来获取API。')

        return self.agent.exports()

    def set_agent(self, agent):
        """
            设置用于通信的活动代理。
            
            :param agent:
            :return:
        """

        self.agent = agent

    def get_agent(self):

        if not self.agent:
            raise Exception('没有可用的agent代理。')

        return self.agent

    def __repr__(self) -> str:
        return f'<State DevSerial: {self.device_id}, Network:{self.network}, Host:{self.host}, Port:{self.port}'


state_connection = StateConnection()
