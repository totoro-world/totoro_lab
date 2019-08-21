import gold_data
import gold_train

if __name__ == '__main__':
    print('### fetch data ###')
    gold_data.fetch_gold_data()
    print('### train ###')
    gold_train.predict(30)
