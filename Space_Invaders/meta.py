import logging
import config
#from logging.handlers import RotatingFileHandler


def create_logger(name, level='DEBUG'):
    """Creates, configures, and returns a log object for `log.debug('error message')` style logging."""

    # Rename __main__ to main
    if name.startswith('__') and name.endswith('__'):
        name = name[2:-2]

    justified_name = name.ljust(config.logging.name_justify_length)
    logger = logging.getLogger(justified_name)

    # Set the level of the entire logger so each handler can correctly set their level.
    logger.setLevel(logging.getLevelName(level))

    # Console logger
    c_handler = logging.StreamHandler()

    terminal_level = logging.getLevelName(config.logging.terminal_log_level)
    c_handler.setLevel(terminal_level)
    if name in config.logging.logger_specific_levels:
        level = logging.getLevelName(config.logging.logger_specific_levels[name])
        c_handler.setLevel(level)
    c_format = logging.Formatter(config.logging.terminal_format)
    c_handler.setFormatter(c_format)


    # File logger
    # f_handler = RotatingFileHandler(config.Logging.file,
    #                               maxBytes=config.Logging.MaxFileSize,
    #                               backupCount=config.Logging.MaxFiles)
    # f_handler.setLevel(config.Logging.terminal_level)
    # f_format = logging.Formatter(config.Logging.file_format)
    # f_handler.setFormatter(f_format)

    logger.addHandler(c_handler)
    # logger.addHandler(f_handler)

    return logger
