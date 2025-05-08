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
            filemode='w',
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s'
        )
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
        if level == 'info':
            logger.info(message)
        elif level == 'warning':
            logger.warning(message)
        elif level == 'error':
            logger.error(message)
        elif level == 'debug':
            logger.debug(message)
        elif level == 'critical':
            logger.critical(message)
        else:
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
    logging.info("Logger initialized and ready to use.")
    logging.shutdown()

if __name__ == "__main__":
    main()
