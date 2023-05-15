import os
import definitions


def install(logging, verbose):
    try:
        print("Installation process started")
        logging.info("Installation process started")

        # if conf file is not exists then create it
        if not os.path.exists(os.path.dirname(definitions.CONF_FILE_PATH)):
            os.makedirs(os.path.dirname(definitions.CONF_FILE_PATH))

        if not os.path.isfile(os.path.basename(definitions.CONF_FILE_PATH)):
            with open(definitions.CONF_FILE_PATH, 'w') as f:
                f.write(definitions.CONF)

        # if the service is exists, update it
        if not os.path.isfile(os.path.basename(definitions.SERVICE_PATH)):
            with open(definitions.SERVICE_PATH, 'w') as f:
                f.write(definitions.SERVICE)



        print("Installation process completed successfully")
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