import configparser

def _check(item):
  config_ini = configparser.ConfigParser()
  config_ini.read('config.ini',encoding='utf-8')
  read_keys = config_ini['KEY']
  MAIN_PATH = read_keys.get('MAIN_PATH')
  BONO_IP = read_keys.get('BONO_IP')
  if(item=="MAIN_PATH"):
    return MAIN_PATH
  if(item=="BONO_IP"):
    return BONO_IP

def get_ip():
  return _check("BONO_IP")

def get_main_path():
  return _check("MAIN_PATH")

if __name__ == '__main__':
  string=get_main_path()+"ml_data/open.csv"
  print(string)
