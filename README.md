# image_blending-and-Histogram-Equalization
파이썬을 이용한 이미지 블랜딩과 Histogram Equalization 구현입니다.

# 블랜딩 : 손 이미지 위에 눈 이미지를 자연스럽게 배치하는 것이 목표입니다.

![image](https://user-images.githubusercontent.com/63800086/146646091-c68029de-30aa-4bb5-b66f-bfccf85a3c45.png)

블랜딩 과정:

1. 각 이미지에 대한 가우시안 피라미드 생성

![image](https://user-images.githubusercontent.com/63800086/146646137-5024918e-acef-40ec-b54c-9155aac1fb74.png)


 

2. 가우시안 피라미드를 이용하여 라플라시안 피라미드 생성


-해당 레벨에 있는 가우시안 피라미드 이미지를 업스케링하고, 다음 레벨의 가우시안 피라미드 이미지와의 차이 도출. 오리지널 이미지에서 스무딩된 이미지를 빼면 디테일한 부분만 남는 원리를 이용해 디테일한 부분만 도출.

![image](https://user-images.githubusercontent.com/63800086/146646218-25fc4cc5-93c5-4f8e-95cd-ac1034f2f5cb.png)

3. stitch (눈 이미지를 손 이미지 가운데로 올리는 과정)

![image](https://user-images.githubusercontent.com/63800086/146646252-e0ff01cf-f55e-4358-ad8a-d71541af3795.png)



4. stitch 이미지 합치기

가장 마지막 레벨의 가우시안 stitch 이미지를 업스케일링 하고 해당 크기와 같은 라플라시안 stitch 이미지와 더해준다. 오리지널 이미지에 디테일한 영상을 더하면 sharp한 이미지가 도출되는 원리. 해당 과정을 원래 이미지 크기(가장 낮은 레벨)에 도달할 때까지 반복

![image](https://user-images.githubusercontent.com/63800086/146646309-70761235-58aa-4e38-99bf-afd02bbabbe6.png)

-레벨5 단계부터 시작하여 업스케일링 하고 라플라시안 이미지를 더해 나가면서 점점 자연스럽고 선명한 이미지가 도출.

<br/>
<br/>
<br/>
<br/>
<br/>

# Color Histogram Equalization : 일반적으로 Histogram Equalization은 1-channel일 경우에 동작하지만 rgb 채널을 입힌 영상으로 출력하는 것이 목표입니다.

(Histogram Equalization은 좁은 contrast 영역을 가지는 영상을 넓은 contrast 이미지 영역을 가지는 영상으로 바꾸는 기술)

1. 이미지 분리 : 이미지를 각각 gray이미지, rgb이미지, hsv 컬러 스페이스를 사용하는 이미지로 바꾸어 저장

2. 이미지를 rgb로 표현하기 위해 밝기 정보를 가지는 컬러 스페이스인 HSV로 변환한 이미지의 채널을 분리한다. 밝기 정보를 나타내는 채널인 v채널에 Histogram Equalization을 적용하고 다시 나머지 채널인 h,s 합친 후 결과를 그림.

3. 위 과정을 Adaptive Histogram Equalization과 Contrast Limited AHE에도 똑같이 적용 하여 그림. (3가지 Histogram Equalization을 비교.)  


결과:

![image](https://user-images.githubusercontent.com/63800086/146646636-61d31b64-f5f8-497c-90ab-deb2418de696.png)



첫 번째 줄에는 오리지널 그레이 이지미와 rgb 이미지가 각각 왼쪽과 오른쪽에 위치하고 가운데에는 히스토그램과 누적분포 함수가 그려진다. 낮은 contrast 영역을 가지는 이미지이기 때문에 히스토그램의 분포가 작은 것을 볼 수 있다.

두 번째 줄에는 global Histogram Equalization을 적용한 결과이다. 누적분포함수가 선형적으로 펼쳐질 수 있게 전 영역을 펼쳐서 사용하고 있다. 이미지의 결과를 보면 선명해진 부분도 존재하지만 정보가 손실된 부분도 존재하고, 특히 물체는 알아볼 수 없게 되었다.

세 번째 줄에는 Adaptive Histogram Equalization을 적용한 결과이다. 따라서 부분적으로 Histogram Equalization을 진행한다. global Histogram Equalization을 적용한 결과보다 정보의 손실은 줄었으나 노이즈가 나타난 것 같은 이미지 결과가 도출됐다.

네 번째 줄에는 과 Contrast Limited AHE를 적용한 결과이다. 누적분포 함수를 살펴보면 global Histogram Equalization의 누적분포 함수와 비교했을 때 높이는 줄어들었고, 밑부분의 두께는 두터워졌음을 볼 수 있다. 이미지 결과 또한 정보의 손실이 많지 않고 선명해졌으며 Adaptive Histogram Equalization에 비해 노이즈도 보이지 않는 것을 확인할 수 있다. 



