#! python3


# import libraries
import requests
import yaml
import time


if __name__ == '__main__':
    # import settings
    with open('k0001appconf.yaml', 'r') as f:
        appConfig = yaml.load(f)

    #
    while True:
        try:
            if appConfig['automaat']['raspberry_pi']:
                data = requests.get('http://192.168.1.36/data/data_from_gui.json')
            else:
                data = requests.get('http://localhost/MAP_K0001/data/data_from_gui.json')

            if data.status_code == 200:
                json_data = data.json()
                yaml_data = open('data/data_from_gui.yaml', 'w+')
                yaml.dump(json_data, yaml_data)
        except:
            pass

        time.sleep(0.1)
