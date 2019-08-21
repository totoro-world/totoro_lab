import usd_data
import usd_train

if __name__ == '__main__':
    print('### fetch data ###')
    usd_data.fetch_data()
    print('### train ###')
    usd_train.predict(30)
