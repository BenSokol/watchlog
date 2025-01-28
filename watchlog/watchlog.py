#!/usr/local/bin/python3
# @Filename: watchlog.py
# @Author:   Ben Sokol
# @Email:    ben@bensokol.com
# @Created:  January 27th, 2025 [9:01pm]
#
# Copyright (C) 2025 by Ben Sokol. All Rights Reserved.

import sys
if (sys.version_info < (3, 0)):
  print("watchlog requires python3\n\npython3 " + ' '.join(sys.argv) + "\n")
  sys.exit(100)

import argparse
import enum
import logging
import pathlib
import subprocess
import sys
import typing

__all__ = ["watchlog"]

logger = logging.getLogger(__name__)
logging.addLevelName(logging.DEBUG - 1, "DEBUG")
logging.addLevelName(logging.INFO - 1, "INFO")


def logger_debug(*args, **kwargs):
  logger.log(logging.DEBUG - 1, *args, **kwargs)


def logger_info(*args, **kwargs):
  logger.log(logging.INFO - 1, *args, **kwargs)


class ReturnCode(enum.IntEnum):
  success = 0
  error = 1


def watchlog(logfile: str, noexec: bool = False) -> ReturnCode:
  logpath = pathlib.Path(logfile).resolve()
  if not logpath.exists():
    logger_debug("Resolved path does not exist: '" + str(logpath) + "'")
    logpath = pathlib.Path("/var/log").joinpath(logfile).resolve()
    if not logpath.exists():
      logger_debug("Resolved path does not exist: '" + str(logpath) + "'")
      logger.error("ERROR: Unable to locate a logfile at either '" + str(logfile) + "' or '/var/log/" + str(logfile) + "'")
      return ReturnCode.error

  logger_debug("Resolved path: '" + str(logpath) + "'")
  proc = subprocess.run(["tail", "-f", str(logpath)])

  return proc.returncode


def main() -> typing.NoReturn:
  """ Main script entry point. """
  description = '''
Watches a logfile for changes
'''
  parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=description)
  parser.add_argument('logfile', action='store', help='Logfile to watch. (Default: /var/log/syslog)', default='/var/log/syslog')

  dev_options = parser.add_argument_group(pathlib.Path(__file__).name + " developer options")
  dev_options.add_argument('--noexec', '-n', action="store_true", help="No execute. Does not send anything to the webhook.", default=False)
  dev_options.add_argument('--verbose', '-v', action="store_true", help="Prints additional information.", default=False)

  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(level=logging.DEBUG - 1, format='%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
  else:
    logging.basicConfig(level=logging.INFO - 1, format='%(asctime)s - %(module)s - %(levelname)s - %(message)s')

  ret_code = watchlog(logfile=args.logfile, noexec=args.noexec)
  logging.shutdown()
  sys.exit(ret_code)


# Run the script
if __name__ == '__main__':
  try:
    main()
  except SystemExit:
    # SystemExit exception gets thrown on sys.exit() calls.
    # This has the exit code in the exception info.
    sys.exit(sys.exc_info()[1])
  except KeyboardInterrupt:
    # Dont print exception info for KeyboardInterrupt exceptions (CTRL + C)
    # Keyboard interrputs default to a return value of 130, so return that.
    sys.exit(130)
