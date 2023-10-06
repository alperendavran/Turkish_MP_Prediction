
rawdata = open('22Donem_age.csv', 'rb').read()

result = chardet.detect(rawdata)
encoding = result['encoding']
