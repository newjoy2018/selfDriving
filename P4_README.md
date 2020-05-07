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
* We can measure the time to collision by observing relative height change on the image sensor. But bounding boxes is not a good indicator which can stably reflect the true vehicle dimensions and the aspect ratio differs between images, because the bounding boxes change over different images for the same vehical. If we use bounding box height or width to compute time to collision, it would lead to significant errors. Instead of relying on the detection of the vehicle as a whole, better choice is the structure on the specific vehicle. If it were possible to locate uniquely identifiable keypoints that could be tracked from one frame to the next, we could use the distance between all keypoints on the vehicle relative to each other to compute a robust estimate of the height ratio in out TTC equation. The ratio of all relative distances between each other can be used to compute a reliable TTC estimate by replacing the height ratio h1 / h0 with the mean or median of all distance ratios dk / dk'. However, computing the mean distance ratio as in the function we just discussed would presumably lead to a faulty calculation of the TTC. A more robust way of computing the average of a dataset with outliers is to use the median instead.


Compute the time-to-collision in second for all matched 3D objects using only keypoint correspondences from the matched bounding boxes between current and previous frame.
* Code is functional and returns the specified output. Also, the code is able to deal with outlier correspondences in a statistically robust way to avoid severe estimation errors.



## FP.5 Performance Evaluation 1
* Find examples where the TTC estimate of the Lidar sensor does not seem plausible. Describe your observations and provide a sound argumentation why you think this happened.
* Several examples (2-3) have been identified and described in detail. The assertion that the TTC is off has been based on manually estimating the distance to the rear of the preceding vehicle from a top view perspective of the Lidar points.


## FP.6 Performance Evaluation 2
* Run several detector / descriptor combinations and look at the differences in TTC estimation. Find out which methods perform best and also include several examples where camera-based TTC estimation is way off. As with Lidar, describe your observations again and also look into potential reasons.
* All detector / descriptor combinations implemented in previous chapters have been compared with regard to the TTC estimate on a frame-by-frame basis. To facilitate comparison, a spreadsheet and graph should be used to represent the different TTCs.

