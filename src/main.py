import shutil
import os
import logging
import datetime
def initialize_logger():
    log_date = datetime.datetime.now().strftime('%Y-%m-%d')
    log_dir = os.path.join(os.path.curdir, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    log_filepath = os.path.join(log_dir, f'log_{log_date}.txt')
    try:
        logging.basicConfig(
            filename=log_filepath,
            filemode='a',
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s'
        )
        logging.info(f'Logger initialized at location - {os.path.abspath(log_filepath)}')
    except Exception as e:
        raise RuntimeError(f"Failed to initialize logger: {e}")

def log_message(message, level='info'):
    """
    Logs a message at the specified level.
    :param message: The message to log.
    :param level: The logging level ('info', 'warning', 'error', 'debug', 'critical').
    """
    if not isinstance(message, str):
        raise ValueError("Message must be a string.")
    if not isinstance(level, str):
        raise ValueError("Level must be a string.")
    if not message:
        raise ValueError("Message cannot be empty.")
    if not level:
        raise ValueError("Level cannot be empty.")
    if not logging.getLogger().hasHandlers():
        raise RuntimeError("Logger not initialized. Call initialize_logger() first.")
    
    assert level in ['info', 'warning', 'error', 'debug', 'critical'], "Invalid logging level."
    
    logger = logging.getLogger()
    level = level.lower()
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


def delete_dest_dir(abspath):
    if not os.path.exists(abspath):
        error = f"The given path of the destination directory does not exist: {abspath}"
        log_message(error, 'error')
        raise ValueError(error)

    if not os.listdir(abspath):
        log_message(f"The given path of the destination directory is empty: {abspath}", 'info')
        return
    
    for entry in os.listdir(abspath):
        entry_path = os.path.join(abspath, entry)
        if os.path.isfile(entry_path):
            os.remove(entry_path)
            log_message(f"File deleted: {entry_path}", 'info')
        elif os.path.isdir(entry_path):
            shutil.rmtree(entry_path)
            log_message(f"Directory deleted: {entry_path}", 'info')
    log_message(f"The deletion has been completed for the directory: {abspath}", 'info')

def move_src_to_dest_dir(src_path, dest_dir):
    # Make sure the destination directory is cleared
    if os.path.exists(dest_dir) and \
        input("Do you want to delete the destination directory? (y/n): ").strip().lower() == 'y':
        delete_dest_dir(dest_dir)
    else:
        log_message(f"Skipping deletion of the existing directory: {dest_dir}", 'info')
        
    if not os.path.exists(dest_dir):        
        os.makedirs(dest_dir)
        log_message(f"Destination directory created: {dest_dir}", 'info')

    for item in os.listdir(src_path):
        s = os.path.join(src_path, item)
        d = os.path.join(dest_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, False, None)
            log_message(f"Directory moved: {s} to {d}", 'info')
        else:
            shutil.copy2(s, d)
            log_message(f"File moved: {s} to {d}", 'info')
    log_message(f"All items from {src_path} have been moved to {dest_dir}", 'info')
    log_message(f"Source directory: {src_path}", 'info')
    log_message(f"Destination directory: {dest_dir}", 'info')
    log_message("Moving process completed", 'info')
    log_message("Moving process completed", 'info')

def main():
    initialize_logger()
    log_message("Starting the script", 'info')
    src_path = os.path.abspath(os.path.join(__file__, "../../static"))
    dest_path = os.path.abspath(os.path.join(__file__, "../../public"))
    move_src_to_dest_dir(src_path=src_path, dest_dir=dest_path)
    log_message("Script completed successfully", 'info')

if __name__ == "__main__":
    main()
