# coding=utf-8
import uuid
import diamond.collector


class NFSAvailabilityCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(self.__class__, self).get_default_config_help()
        config_help.update({
            'test_path': 'Path to test NFS read / writes to',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(self.__class__, self).get_default_config()
        config.update({
            'test_path': '/data/project/canary/nfs-availability-test',
        })
        return config

    def collect(self):
        content = str(uuid.uuid4())
        with open(self.config['test_path'], 'w') as f:
            f.write(content)

        with open(self.config['test_path']) as f:
            actual_content = f.read()

        if actual_content == content:
            self.publish('home_nfs_availability', 100)
