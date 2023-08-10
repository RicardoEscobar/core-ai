 Logging Levels

Explain and list all logging levels in the logging module in python:

In Python, the logging module provides a flexible logging system that allows developers to control how and where log messages are emitted. The module defines several log levels, each of which represents a different severity level of a log message. The levels, in increasing order of severity, are:

- __DEBUG__: Detailed information, typically of interest only when diagnosing problems.

- __INFO__: General information about the operation of a program.

- __WARNING__: An indication that something unexpected happened or indicative of some problem in the near future (e.g., disk space low). The software is still working as expected.

- __ERROR__: Due to a more serious problem, the software has not been able to perform some function.

- __CRITICAL__: A very serious error, indicating that the program itself may be unable to continue running.

The logging levels are used to determine which log messages are emitted. By setting the logging level for a logger, you can control which messages are emitted based on their severity level. By default, the logging level is set to WARNING, which means that messages with a severity level of WARNING or higher will be emitted.

2023-08-10 17:19:09

Default levels and level names, these can be replaced with any positive set of values having corresponding names. There is a pseudo-level, NOTSET, which is only really there as a lower limit for user-defined levels. Handlers and loggers are initialized with NOTSET so that they will log all messages, even at user-defined levels.


CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0