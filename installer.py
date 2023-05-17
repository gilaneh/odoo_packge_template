import os
import definitions
from colorama import Fore


def install(logging, verbose):
    try:
        print(Fore.GREEN, "Installation process started 1", Fore.RESET)
        logging.info("Installation process started")

        # if conf file is not exists then create it
        # if not os.path.exists(definitions.CONF_FILE_PATH):
        #     os.touch(definitions.CONF_FILE_PATH)

        print(Fore.RED, 'create CONF 1:', os.path.isfile(definitions.CONF_FILE_PATH), Fore.RESET)

        if not os.path.isfile(definitions.CONF_FILE_PATH):
            with open(definitions.CONF_FILE_PATH, 'w') as f:
                print(Fore.RED, 'create CONF:', f.write(definitions.CONF), Fore.RESET)
        print(Fore.RED, 'create CONF 2:', os.path.isfile(definitions.CONF_FILE_PATH), Fore.RESET)

        # if the service is exists, update it
        if not os.path.isfile(definitions.SERVICE_PATH):
            with open(definitions.SERVICE_PATH, 'w') as f:
                print(Fore.BLUE, 'create SERVICE:', f.write(definitions.SERVICE), Fore.RESET)

        print(Fore.RED, 'create SERVICE_PATH 3:', os.path.isfile(definitions.SERVICE_PATH), Fore.RESET)

        print(Fore.CYAN,"Installation process completed successfully", Fore.RESET)
        logging.info("Installation process completed successfully")
        return True
    except Exception as e:
        print(f'Failed to install: {e}')
        logging.info(f'Failed to install: {e}')
        return False



def read(config_file):
    log_file = ''
    with open(config_file, 'r') as f:
        config_file = f.readlines()

    for line in config_file:
        line_splite = line.split('=')
        if len(line_splite) == 2:
            if line_splite[0].strip() == 'url':
                url = line_splite[1].strip() 
            elif line_splite[0].strip() == 'LOG_FILE': 
                log_file = line_splite[1].strip()
                if not os.path.isdir(os.path.dirname(log_file)):
                    os.makedirs(os.path.dirname(log_file))

    return (url, log_file)