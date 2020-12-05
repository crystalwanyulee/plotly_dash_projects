

## Kartemap Web Application



![image-20201125122321321](images\image-20201125122321321.png)

<div style="page-break-after: always; break-after: page;"></div>

## Installation

```python
plotly 4.12.0
dash 1.17.0
dash-bootstrap-components 1.13.0
dash-html-components 1.1.1
```



## Get Started

Running the app locally

```cmd
python app.py
```



## Example

![demo](images/demo.gif)



## Introduction

#### The top-right controller  

* In addition to select the start city and destination city, users can also add several intermediary cities between them. 

* Moreover, I create a function called fixed for users to find the best route more flexibly. The default is `Order`, that is, the algorithm will find the best route without changing the order `Boston->Dallas->Seattle->Los Angeles`. If users want to find out the shortest route regardless of the order, they have the following options. 

* - **Fix the start city:**  The model will try all kinds of combination to calculate distances, for example, `Boston->Seattle->Los Angeles->Dallas`, `Boston->Dallas->Los Angeles->Seattle`, `Boston-> Los Angeles->Dallas->Seattle`... and so on.  However, the start city will not change in these combinations. 
  - **Fix the destination city:** similar to the option that fix the start city, the model explores the shortest route without changing the end city. 
  - **Fix the start city and the destination city at the same time**
  - **None to fix:** suppose users choose `None` to fix. The application will automatically find out the shortest path, including these cities. The order probably will not be the same as the order they define before.

<img src="C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20201125121700444.png" alt="image-20201125121700444" style="zoom:50%;" />

<img src="C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20201125121657364.png" alt="image-20201125121657364" style="zoom:50%;" />



#### Map

* Before choosing any start city or destination city, the default map looks like the following. It shows all available city options. 

<img src="C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20201125120354385.png" alt="image-20201125120354385" style="zoom:50%;" />

* The map will automatically show the route based on users' choice.



<img src="C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20201125122353770.png" alt="image-20201125122353770" style="zoom:50%;" />

* top-left panel

  * Distance: show the total distance of the route
  * The number of cities: show how many cities the user will pass through
  * Available airlines (drop down menu)

  

  

  <img src="C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20201125122027378.png" style="zoom: 67%;" >

  

  <img src="C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20201125121828701.png" style="zoom: 67%;" >

  

#### Bottom City Information

* Show information of all cities in the route. Information includes images, city names, population, descriptions and `Learn More` links to Tripadvisor 

![image-20201125122422445](C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20201125122422445.png)

* The example link to the trip advisor page

<img src="C:\Users\admin\AppData\Roaming\Typora\typora-user-images\image-20201125122844874.png" alt="image-20201125122844874" style="zoom: 33%;" />



