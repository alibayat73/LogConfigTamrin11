import logging
import configparser
import signal

iteration = 1

def signal_handler(sig, frame):
        if sig == signal.SIGUSR1:
                logging.getLogger().setLevel(logging.INFO)
        elif sig == signal.SIGUSR2:
                logging.getLogger().setLevel(logging.CRITICAL)
        elif sig == signal.SIGALRM:
                logFullName()
                signal.alarm(iteration)
        else:
                signal.raise_signal(sig)

def read_config(file, mandatory_key_list):
        config = configparser.ConfigParser()
        config.read(file)
        
        cfg = {}
        for each_section in config.sections():
                for mandatory_key in mandatory_key_list:
                        if not config.has_option(each_section, mandatory_key):
                                return False, 'Could not find ' + mandatory_key
                for (each_key, each_val) in config.items(each_section):
                        if each_key not in mandatory_key_list:
                                return False, 'One of mandatory keys is missing'
                        key = each_key.strip()
                        value = each_val.strip()
                        cfg[key] = value   
        return True, cfg

def logFullName():
        logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        status, result = read_config('config.ini', ['first_name', 'last_name'])
        if not status:
                logging.error(result)
                exit(1)
        cfg = result
        if logging.getLogger().getEffectiveLevel() == logging.INFO:
                logging.info('Full name is: ' + cfg['first_name'] + ' ' + cfg['last_name'])
        elif logging.getLogger().getEffectiveLevel() == logging.WARNING:
                logging.warning('Full name is: ' + cfg['first_name'] + ' ' + cfg['last_name'])
        else:
                logging.critical('Full name is: ' + cfg['first_name'] + ' ' + cfg['last_name'])

signal.signal(signal.SIGALRM, signal_handler)
signal.signal(signal.SIGUSR1, signal_handler)
signal.signal(signal.SIGUSR2, signal_handler)

signal.alarm(iteration)

while True:
        pass