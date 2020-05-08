# SFND 3D Object Tracking

Welcome to the final project of the camera course. By completing all the lessons, you now have a solid understanding of keypoint detectors, descriptors, and methods to match them between successive images. Also, you know how to detect objects in an image using the YOLO deep-learning framework. And finally, you know how to associate regions in a camera image with Lidar points in 3D space. Let's take a look at our program schematic to see what we already have accomplished and what's still missing.

<img src="images/course_code_structure.png" width="779" height="414" />

In this final project, you will implement the missing parts in the schematic. To do this, you will complete four major tasks: 
1. First, you will develop a way to match 3D objects over time by using keypoint correspondences. 
2. Second, you will compute the TTC based on Lidar measurements. 
3. You will then proceed to do the same using the camera, which requires to first associate keypoint matches to regions of interest and then to compute the TTC based on those matches. 
4. And lastly, you will conduct various tests with the framework. Your goal is to identify the most suitable detector/descriptor combination for TTC estimation and also to search for problems that can lead to faulty measurements by the camera or Lidar sensor. In the last course of this Nanodegree, you will learn about the Kalman filter, which is a great way to combine the two independent TTC measurements into an improved version which is much more reliable than a single sensor alone can be. But before we think about such things, let us focus on your final project in the camera course. 

## Dependencies for Running Locally
* cmake >= 2.8
  * All OSes: [click here for installation instructions](https://cmake.org/install/)
* make >= 4.1 (Linux, Mac), 3.81 (Windows)
  * Linux: make is installed by default on most Linux distros
  * Mac: [install Xcode command line tools to get make](https://developer.apple.com/xcode/features/)
  * Windows: [Click here for installation instructions](http://gnuwin32.sourceforge.net/packages/make.htm)
* Git LFS
  * Weight files are handled using [LFS](https://git-lfs.github.com/)
* OpenCV >= 4.1
  * This must be compiled from source using the `-D OPENCV_ENABLE_NONFREE=ON` cmake flag for testing the SIFT and SURF detectors.
  * The OpenCV 4.1.0 source code can be found [here](https://github.com/opencv/opencv/tree/4.1.0)
* gcc/g++ >= 5.4
  * Linux: gcc / g++ is installed by default on most Linux distros
  * Mac: same deal as make - [install Xcode command line tools](https://developer.apple.com/xcode/features/)
  * Windows: recommend using [MinGW](http://www.mingw.org/)

## Basic Build Instructions

1. Clone this repo.
2. Make a build directory in the top level project directory: `mkdir build && cd build`
3. Compile: `cmake .. && make`
4. Run it: `./3D_object_tracking`.


## FP.1 Match 3D Objects
* Here we iterate all of the matches between previous and current data frame, in order to extract corresponding key points. So, we check if the previous bounding box contains previous key points and current bounding box contains current key points. If so, the number of total matches between previous bounding box ID and current bounding box ID will be accumulated. In the end, we choose the match with the max count number as the final match between previous and current bounding box ID. Use for loop to Keep iterating like that untill we find all the matches.

## FP.2 Compute Lidar-based TTC
* Here we choose the points inside the ego lane `(abs(it->y) <= laneWidth / 2.0)` and compute the mean value of x coordinates. Then compute LiDAR based TTC with the following equation:
* TTC = minXCurr * dT / (minXPrev - minXCurr)

## FP.3 Associate Keypoint Correspondences with Bounding Boxes
* In `clusterKptMatchesWithROI()` function, we associate a given bounding box with the keypoints it contains. And iterate all of the key-point matches. If the key-point can be found in the region of interest of our current bounding box, then save current match to corresponding bounding box structure for calculating the camera based TTC. Also, we use the threshold of duclidean distance to filter  outlier matches.

## FP.4 Compute Camera-based TTC
* According to the previous lesson, we can measure the time to collision by observing relative height change on the image sensor. But bounding box is not a good indicator which can stably reflect the true vehicle dimensions because bounding boxes change over different images for the same vehical. If we use bounding box height or width to compute time to collision, it would lead to significant errors. Instead of relying on the detection of the vehicle as a whole, better choice is the structure on the specific vehicle. If it were possible to locate uniquely identifiable keypoints that could be tracked from one frame to the next, we could use the distance between all keypoints on the vehicle relative to each other to compute a robust estimate of the height ratio in TTC equation. The ratio of all relative distances between each other can be used to compute a reliable TTC estimate by replacing the height ratio with the mean or median of all distance ratio. However, computing the mean distance ratio as in the function we just discussed may lead to a faulty calculation of the TTC. The median would be a much more robust way of computing the average of a dataset with outliers instead.


## FP.5 Performance Evaluation 1
* Most TTC estimates from Lidar and camera match very well, there are only small errors between them, like in the following chart(TTC from Lidar is in blue, TTC from camera is in yellow):
<img src="images/TTC_fromLidar&Camera.png" width="587" height="341" />

* But there are also huge errors in some estimates, like TTC estimate by the detector-descriptor combination of SHITOMASI-FREAK in the following:
<img src="images/TTC_SHITOMASI&FREAK.png" width="587" height="342" />

* The errors may come from:
  * The LiDAR and camera are not completely synchronized with each other
  * The LiDAR itself is not calibrated very well
  * Vibration may occur during driving which causes huge errors
* So maybe we can use Kalman filter to reduce errors by minimizing covariance in the future.

## FP.6 Performance Evaluation 2
* According to the mid-term project, we get the result that FAST-ORB, FAST-BRIEF, ORB-BRIEF are the Top3 combinations with the fastest processing time.
* TTC of FAST-ORB
|   Img	 |    Lidar  	|   Camear   |
| :----: | :--------: | :--------: |
|    1   |	12.2891   	|  	13.2736 	|
|    2   |	13.3547   	|  	16.9247	 |
|    3   |	16.3845   	| 		12.8019	 |
|    4   |	14.0764   	| 		10.8876 	|
|    5   |	12.7299   	|	 	11.8197	 |
|    6   |	13.7511	   |  	12.075	  |
|    7   |	13.7314   	|	 	12.1365 	|
|    8   |	13.7901   	| 		11.3714	 |
|    9   |	12.059    	| 	 12.828  	|
|    10  |	11.8642   	| 		13.5979 	|
|    11  |	11.9682    | 		13.1292 	|
|    12  |	9.88711   	| 		12.6578	 |
|    13  |	9.42504   	| 		12.2661	 |
|    14  |	9.30215   	| 		11.811  	|
|    15  |	8.3212	   	| 	 8.75591 	|
|    16  |	8.89867   	| 		11.6437 	|
|    17  |	11.0301   	| 		10.7754 	|
|    18  |	8.53557   	| 	 12.0257	 |
<img src="images/TTC_fast-orb.png" width="588" height="341" />

* TTC of FAST-BRIEF
|  Img 	|  Lidar	 |  Camear |
| :---: | :-----: | :-----: |
|   1   | 12.2891 | 7.81346 |
|   2   | 13.3547 | 13.3196 |
|   3   | 16.3845 | 13.2034 |
|   4   | 14.0764 | 11.5213 |
|   5   | 12.7299 | 13.0781 |
|   6   | 13.7511 | 13.2370 |
|   7   | 13.7314 | 12.1527 |
|   8   | 13.7901 | 12.8288 |
|   9   | 12.0590 | 12.9165 |
|   10  | 11.8642 | 11.2720 |
|   11  | 11.9682 | 11.6361 |
|   12  | 9.88711 | 12.3677 |
|   13  | 9.42504 | 10.9117 |
|   14  | 9.30215 | 10.4153 |
|   15  | 8.32120 | 9.90402 |
|   16  | 8.89867 | 9.22703 |
|   17  | 11.0301 | 11.0143 |
|   18  | 8.53557 | 8.7287  |
<img src="images/TTC_fast_brief.png" width="589" height="346" />

* TTC of ORB-BRIEF
|  Img 	|  Lidar 	|  Camear |
| :---: | :-----: | :-----: |
|   1   | 12.2891 | 9.46493 |
|   2   | 13.3547 | 9.65069 |
|   3   | 16.3845 | 9.9927  |
|   4   | 14.0764 | 20.2057 |
|   5   | 12.7299 | 13.9588 |
|   6   | 13.7511 | 11.8182 |
|   7   | 13.7314 | 9.67764 |
|   8   | 13.7901 | 12.3274 |
|   9   | 12.059  | 169.207 |
|   10  | 11.8642 | 9.82612 |
|   11  | 11.9682 | 21.3918 |
|   12  | 9.88711 | 13.4376 |
|   13  | 9.42504 | 10.0892 |
|   14  | 9.30215 | 6.79522 |
|   15  | 8.3212  | 14.1892 |
|   16  | 8.89867 | 11.0830 |
|   17  | 11.0301 | 11.5144 |
|   18  | 8.53557 | 9.3379  |
<img src="images/TTC_orb_brief.png" width="586" height="348" />

* As we can see from above, it seems that there may always be errors bewteen Lidar- and camera- based TTC estimation, especially in ORB-BRIEF combination. The reasons for these inaccurate camera-based TTC estimation may be:
- Key-points mismatching
- lighting condition changes, which may influence the key point detection and tracking.
* If we fuse with other sensors and use Kalman filter, the result may be improved.
