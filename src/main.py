# import shutil
import os
import logging
import pprint
import datetime


def initialize_logger():
    log_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
    log_dir = os.path.join(os.path.curdir, 'logs')
    log_filepath = os.path.join(log_dir, f'log_{log_date}.txt')
    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
            print(f'Directory created: {log_dir}')
        except Exception as e:
            print(f'The directory {log_dir} cannot be created due to {e}')
    try:
        logging.basicConfig(
            filename=log_filepath,
            filemode='a' if os.path.exists(log_filepath) else 'w',
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s'
        )
        log_message(f'Logger initialized at location - {os.path.abspath(log_filepath)}')
        print(f'Log file created at {log_filepath}')
    except Exception as e:
        raise Exception(e)
    
def log_message(message, level='info'):
    """
    Logs a message at the specified level and ensures logging is properly shut down.
    :param message: The message to log.
    :param level: The logging level ('info', 'warning', 'error', 'debug', 'critical').
    """
    logger = logging.getLogger()
    level = level.lower()  
    try:
        match level:
            case 'info':
                logger.info(message)
            case 'warning':
                logger.warning(message)
            case 'error':
                logger.error(message)
            case 'debug':
                logger.debug(message)
            case 'critical':
                logger.critical(message)
            case _:
                logger.info(message)
    finally:
        logging.shutdown()


def delete_dest_dir(abspath):
    if not os.path.exists(abspath):
        raise ValueError(
            f"The given path of the destination directory does not exist: {abspath}"
        )
    for root, dirs, files in os.walk(abspath):
        for file in files:
            ...
            # deletion_filepath = os.path.join(root, file)
        for dir in dirs:
            ...


def move_src_to_dest_dir(src_path, dest_dir):
    pprint(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    initialize_logger()

if __name__ == "__main__":
    main()
