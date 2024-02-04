import pandas as pd

class DataProcessor:
    def __init__(self):
        pass

    def get_config(self):
        
        config = {'question': ["What's your name?", "How old are you?"],
                  'colname': ['name', 'age'],
                  'q_type': ['text', 'text']}
        
        config = pd.DataFrame(config)

        return config
    
    def append_data(self, data):
        print(data)