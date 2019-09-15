# 자동차 번호판 내 숫자인식기 （2018.09.03~2018.12.12）
* * *
#### Co-op Project (2018) / 산학협력 프로젝트 with GIT(Goodmorning Information Technology Co. Ltd.)

### Numberplate Digt Recognizer
#### 역할
1） 번호판 영역 추출 （OpenCV）  
2） 백엔드 서버 구성（AWS EC2, Apache）  
3） 프론트엔드 제작 （HTML5, PHP, JS）  

- 사용자가 업로드한 자동차 이미지 번호판 숫자 인식  
- 이미지 처리(OpenCV) + 숫자 인식(Machine Learning)   

### System Architecture
![](https://cmg7111.github.io/numberplate_architecture.png)

* * *
### 기능
#### Image Segmentation(OpenCV)
1) 이미지 전처리(Canny, Gaussian Blur)
2) 이미지 내 사각형 영역 표시(번호판 영역 사각형의 특징 이용 - 가로세로 비율, 면적) 
3) 번호판 추출(연속적인 사각형 영역 추출)
4) 번호판 영역에서 1,2,3번 과정실행(각 숫자 이미지 추출)
![](https://cmg7111.github.io/segmentation.JPG)


#### 숫자인식(Tensorflow CNN)
1) 인쇄체 숫자 데이터셋을 학습 (128 x 128)
2) CNN(Convolution Neural Net)기법으로 모델 구성
3) 번호판 내 숫자 이미지를 Input으로 숫자 인식
![](https://cmg7111.github.io/numberplate_web.png)


