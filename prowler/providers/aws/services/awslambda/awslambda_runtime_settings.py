import json
import os
import re


class LambdaRuntimeSettings:
    _settings_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "awslambda_runtime_settings.json")
    _settings = os.path.exists(_settings_file) and json.loads(_settings_file) or {}

    @classmethod
    def get(cls, runtime):
        settings_match = [
            cls._settings[key]
            for key in cls._settings.keys()
            if re.Match(key, runtime)
        ]
        if len(settings_match) > 0:
            return LambdaRuntime(runtime, settings_match[0])


class LambdaRuntime:
    def __init__(self, runtime, settings):
        self.runtime = runtime
        self.settings = settings

    def files_to_scan(self, files):
        return [
            file
            for file in files
            if self.__file_is_included(file)
        ]

    def __file_is_included(self, file):
        if "exclude" in self.settings:
            for exclude in self.settings["exclude"]:
                if re.Match(exclude, file):
                    return False
        return True
