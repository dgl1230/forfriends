from toredis.commands import RedisCommandsMixin


class Pipeline(RedisCommandsMixin):
    """
        Redis pipeline class
    """
    def __init__(self, client):
        """
            Constructor

            :param client:
                Client instance
        """

        self._client = client
        self._args_pipeline = []

    def send_message(self, args, callback=None):
        """
            Add command to pipeline

            :param args:
                Command arguments
            :param callback:
                Callback
        """
        self._args_pipeline.append(args)

    def send(self, callback=None):
        """
            Send command pipeline to redis

            :param callback:
                Callback
        """
        args_pipeline = self._args_pipeline
        self._args_pipeline = []
        self._client.send_messages(args_pipeline, callback)

    def reset(self):
        """
            Reset command pipeline
        """
        self._args_pipeline = []
