#!/usr/bin/python3.6
import argparse
import json
import logging
import os
import sys

from src import core_printer
from src import core_runtime

from src import module_resolvers
from src import core_logger

_config_file_name = '.config.json'


def cli_parse():
    """
    Parse the CLI args passed to the script.
    :return: args
    """
    # required
    parser = argparse.ArgumentParser()
    parser.add_argument("DOMAIN", help="domain to query")
    # opts
    parser.add_argument("-wb", "--wordlist-bruteforce", help="enable word list bruteforce module",
                        action="store_true")
    parser.add_argument("-wc", "--wordlist-count", help="set the count of the top words to use DEFAULT: 100",
                        action="store", default=100, type=int)
    parser.add_argument("-rb", "--raw-bruteforce", help="enable raw bruteforce module",
                        action="store_true")
    parser.add_argument("-m", "--module", help="module to hit",
                        action="store")
    parser.add_argument("-o", "--output", help="output directory location (Ex. /users/test/)")
    parser.add_argument("-on", "--output-name", help="output directory name (Ex. test-2017)",)
    parser.add_argument("-l", "--list", help="list loaded modules",
                        action="store_true")
    parser.add_argument("-ll", "--long-list", help="list loaded modules and info about each module",
                        action="store_true")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-d", "--debug", help="enable debug logging to .SimplyDns.log file, default WARNING only",
                        action="store_true")
    args = parser.parse_args()
    if args.verbose:
        print("[!] verbosity turned on")
    return args


def load_config(pr):
    """
    Loads .config.json file for use
    :return: dict obj
    """
    print(pr.blue_text('JSON Configuration file loaded: (NAME: %s)' % (_config_file_name)))
    json_file = json.load(open(_config_file_name))
    ds = module_resolvers.DnsServers()
    ds.populate_servers()
    json_file = ds.populate_config(json_file)
    print(pr.blue_text('Public DNS resolvers populated: (SERVER COUNT: %s)' % (str(ds.count_resolvers()))))
    return json_file


def main():
    """
    Print entry screen and pass execution to CLI, 
    and task core.
    :return: 
    """
    pr = core_printer.CorePrinters()
    pr.print_entry()
    args = cli_parse()
    logger = core_logger.CoreLogging()
    pr.print_config_start()
    config = load_config(pr)
    config['args'] = args
    if args.debug:
        pr.print_green_on_bold('[!] DEBUGGING ENABLED!')
        logger.start(logging.DEBUG)
    else:
        logger.start(logging.INFO)
    logger.infomsg('main', 'startup')
    if args.module:
        c = core_runtime.CoreRuntime(logger, config)
        c.execute_mp()
    elif args.list:
        c = core_runtime.CoreRuntime(logger, config)
        c.list_modules()
    elif args.long_list:
        c = core_runtime.CoreRuntime(logger, config)
        c.list_modules_long()
    else:
        c = core_runtime.CoreRuntime(logger, config)
        c.execute_mp()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)