from nose.tools import eq_
from base_config import BaseConfig
import tempfile
import os


class TestBaseConfig():

    def setup(self):
        self.config_file = \
                tempfile.NamedTemporaryFile(mode="w+", delete=False)
    
    def teardown(self):
        self.config_file.close()
        os.remove(self.config_file.name)

    def test_empty_file(self):
        # If the file is empty then BaseConfig should write
        # some default value in there
        config = BaseConfig(path=self.config_file.name)
        content = self.config_file.file.read()

        assert len(content) != 0

    def test_file_missing_key(self):
        # BaseConfig should use default_config.json to
        # fill in missing config keys from the user config file

        self.config_file.file.write("{}")
        self.config_file.file.flush()
        config = BaseConfig(path=self.config_file.name)

        # Should not raise an exception here
        config["auto-capitalize-expansion"]
