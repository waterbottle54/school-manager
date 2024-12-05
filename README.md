# SE School Manager (학습 관리자)

 ## Introduction

 Login                     |  Admin Menus
:-------------------------:|:-------------------------:
![](https://github.com/waterbottle54/school-manager/blob/main/screenshots/login.png) | ![](https://github.com/waterbottle54/school-manager/blob/main/screenshots/menus.png)

 Data Management            |  Student Registration
 :-------------------------:|:-------------------------:
 ![](https://github.com/waterbottle54/school-manager/blob/main/screenshots/data_management.png) | ![](https://github.com/waterbottle54/school-manager/blob/main/screenshots/add_student.png)

  Problem Management        |  Problem Registration
 :-------------------------:|:-------------------------:
 ![](https://github.com/waterbottle54/school-manager/blob/main/screenshots/view_problems.png) | ![](https://github.com/waterbottle54/school-manager/blob/main/screenshots/add_problem.png)
 
 * **SE School Manager**는 **Qt5 / Python** 으로 작성된 **Desktop** 학습 관리 소프트웨어입니다.<br>

   이 프로그램은 저의 파트타임 강사 경험을 기반으로 제작되었으며, 학원, 교습소에 적합한 용도입니다. <br>
   
   SQLite DB 를 통해 제반 데이터 관리, 학생 관리, 문제 관리, 오답 관리 등의 기능을 제공합니다. <br>

   파이썬의 type hint 뿐 아니라 type check 를 적용하여 type safety, null safety 를 구현하였습니다.

 ## Getting Started
> ### Dependencies
> * Windows: **10, 11**
> * python >= **3.0.9**
> 

 ## Project Overview
> ### Language
> Python (3.9.0 interpreter)
> Strict Type check applied.

> ### IDE
> Visual Studio Code (1.95.3) 

> ### Framework
> Qt5 (5.15.11)
 
> ### GUI
> * 다중 스크린 관리 및 전환을 위해, 네비게이션 패턴을 구현하였다.
> * NavController가 스크린 전환, 스크린 간 데이터 전달, 툴바 갱신 등을 수행한다.
> * 각 스크린 클래스는 접미사로 Fragment가 붙어있다. 총 7개의 Fragment와 3개의 Dialog가 있다.
 
> ### Architecture
> * MVVM Pattern 을 사용하였다. 일관성 있는 데이터 제공을 위해 Repository Layer를 구현하였다.
> * 스크린(-Fragment.py)마다 비즈니스 로직 처리를 위한 개별 뷰모델(-ViewModel.py)이 구현되어 있다.
> * UI의 규모가 작지 않고 잦은 갱신이 요구되므로 Observer 패턴을 사용하였다.
> * Observer 패턴의 구현을 위해 data와 callback을 갖는 LiveData 모듈을 작성하였다.
 
> ### Data Persistency
> * SQLite Database : 필드가 2개 이상인 모델이 저장된다. 
> * Json File: 원시형, 배열 타입의 모델이 저장된다.

 ## Author
 * 조성원 (Sung Won Jo)
 
     📧 waterbottle54@naver.com
   
     📚 [Portfolio](https://www.devsungwonjo.pe.kr/)
   
     📹 [YouTube Channel](https://github.com/waterbottle54)
   
 ## Version History
 * **1.0** (2024.10): First release



