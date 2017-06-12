import shutil
import requests
import time
import numpy as np
from random import randint

minX = 153145
minY = 132718
maxX = 153731
maxY = 133208
zoomLev = 18

# 오류시 다시 시작할 시점. Default는 -1
restart = 166185
count = 0
start_time = time.time()

# Numpy로 List 생성
xArray = np.arange(minX, maxX+1, 1)
yArray = np.arange(minY, maxY+1, 1)
urlArray = []

totalLength = len(xArray) * len(yArray)

# h = roads only
# m = standard roadmap
# p = terrain
# r = somehow altered roadmap
# s = satellite only
# t = terrain only
# y = hybrid
mapType = 'y'

# URL 생성
# url = 'http://mt1.google.com/vt/lyrs=m@377000000&hl=x-local&src=app&sGa&x=306291&y=265444&z=19'
for x in xArray:
    for y in yArray:
        if count > restart-1:
            statusStr = 'count: ' + str(count) + '/' + str(totalLength) + '(' + str(round(count/totalLength*100, 4)) + '%)'
            url = 'http://mt' + str(randint(0, 3)) + '.google.com/vt/lyrs=' + mapType \
                  + '@377000000&hl=x-local&src=app&sGa&x=' + str(x) + '&y=' + str(y) + '&z=' + str(zoomLev)

            # 요청 날림
            response = requests.get(url, stream=True)

            # 완료시 파일 생성
            fileName = 'h/' + str(zoomLev) + '/gh_' + str(x) + '_' + str(y) + '_' + str(zoomLev) + '.jpg'

            if response.status_code == 200:
                # 성공시 이미지 저장
                print(fileName + ' success! ' + statusStr)
                with open(fileName, 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
            else:
                # 실패시 로그 기록
                print(response.status_code)
                with open('failed.txt', "a", encoding='utf-8') as outTxt:
                    outTxt.write(fileName + "\n")
                    outTxt.write(str(count) + ": " + url + "\n")

            print("--- %s seconds ---" % (time.time() - start_time))

            # 15분 돌고 5분간 휴식
            if count != 0 and count % 10000 == 0:
                print("sleeping........")
                time.sleep(300)
                print("Awake!")

            del response

        count += 1
