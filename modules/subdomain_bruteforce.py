import json
import time

from src import core_serialization
from src import module_helpers

from src import core_scrub


# use RequestsHelpers() class to make requests to target URL
class DynamicModule(module_helpers.RequestsHelpers):
    """
    Dynamic module class that will be loaded and called
    at runtime. This will allow modules to easily be independent of the
    core runtime.
    """

    def __init__(self, json_entry):
        """
        Init class structure. Each module takes a JSON entry object which
        can pass different values to the module with out changing up the API.
        adapted form  Empire Project:
        https://github.com/EmpireProject/Empire/blob/master/lib/modules/python_template.py

        :param json_entry: JSON data object passed to the module.
        """
        module_helpers.RequestsHelpers.__init__(self)
        self.json_entry = json_entry
        self.info = {
            # mod name
            'Module': 'subdomain_bruteforce.py',

            # long name of the module to be used
            'Name': 'Recursive Subdomain Bruteforce Using Wordlist',

            # version of the module to be used
            'Version': '1.0',

            # description
            'Description': ['Uses lists from dnspop',
                            'with high quality dns resolvers.'],

            # authors or sources to be quoted
            'Authors': ['@Killswitch-GUI'],

            # list of resources or comments
            'comments': [
                'Searches and performs recursive dns-lookup.'
            ]
        }

        self.options = {
        }

    def dynamic_main(self, queue_dict):
        """
        Main entry point for process to call.

        core_serialization.SubDomain Attributes:
            name: long name of method
            module_name: name of the module that performed collection
            source: source of the subdomain or resource of collection
            module_version: version from meta
            source: source of the collection
            time: time the result obj was built
            subdomain: subdomain to use
            valid: is domain valid

        :return: NONE
        """
        core_args = self.json_entry['args']
        task_output_queue = queue_dict['task_output_queue']
        cs = core_scrub.Scrub()