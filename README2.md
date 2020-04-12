# P2_Radar_Target_Generation_and_Detection
Udacity_SensorFusion
**Project 2: Radar Target Generation and Detection**

* Refer to `radar_target_generation_and_detection.m`

---
## 1. Implementation steps for the 2D CFAR process
In a noisy environment full of clutter noise with changing noise level, a constant threshold is often useless. Because the noise level may change over time. We need to dynamically filter the noise. CFAR is such a great algorithm to solve this problem. It varies the threshold based on surroundings by using sliding window loop across the complete cell matrix. In 2D CFAR, it is implemented in both dimentions of range doppler block. The block consists of CUT(Cell Under Test) in the center, surrounded by guard cells and training cells. Therefore, we have following **2D CFAR process steps**:
* 1. Determine the number of Training cells and Guard cells in both dimensions.
* 2. Use for-Loop to calculate the average noise level across all the training cells.
* 3. Multiply the offset to the average noise level(add offset in logarithmic form), so that we get the threshold.
* 4. Compare the **CUT signal** against the **threshold**, so that we get a resulted signal map with only 0 and 1.
* 5. Assign 0 to the edge cells, which are not covered by CUT because of surrounded guard cells and training cells.

---
## 2. Selection of Training, Guard cells and offset.
* **Training cells** The cells we use to calculate the average noise level is the training cells. By definition, CFAR hopes to define the threshold by calculating the average noise level of the cells around the target, multiplied by an offset value.    **The number of training cells** should be determined according to the environment. For example, a criterion should be that the range of training cells must not contain other CUT. If there are too many training cells, other CUTs may be contained and the resulted threshold will be very large. In this case, targets may be missed. On the contrary, there will be too many false targets being detected. Here we choose:
```
Tr = 10;    % Number of training cells in range dimension
Td = 8;     % Number of training cells in doppler dimension
```

* **Guard cells** Considering various strength of target reflection, in practice, the target is not possible to be "contained" in only one cell. If we use only one cell to "contain" the target signal, other part of it will "leak" to training cells, which will lead to a false threshold.  So **the number of guard cells** should be determined by the strength of target reflection. Stronger the target reflection, more the leakage out of CUT, more the guard cells should have. Here we choose:
```
Gr = 4;    % Number of guard cells in range dimension
Gd = 4;     % Number of guard cells in doppler dimension
```

* **Offset** Offset is used to scale the average noise level. Because **average** means nearly half of the noise level is higher than it. There will be a surprisingly number of false targets if the average value is directly used as the threshold. So it is necessary to scale the average. It should be noted that, as a factor, if it is given in logarithmic form, simply add it. Here we choose:
```
offset = 1.4;      % Offset value
```

---
## 3.Steps taken to suppress the non-thresholded cells at the edges.
Considering the structure of the sliding window, there will be some non-thresholded cells at the edges due to the training cells occupying them. So we need to suppress these cells. Here we assign them a zero:
```
RDM(union(1:(Tr+Gr),end-(Tr+Gr-1):end),:) = 0;      % Edge cells of top and down
RDM(:,union(1:(Td+Gd),end-(Td+Gd-1):end)) = 0;      % Edge cells of left and right
```

---
## 4. Code structure
* 1. Define Radar Specifications 

* 2. User Defined Range and Velocity of Target
* 3. FMCW Waveform Generation
* 4. Signal generation and Moving Target simulation
* 5. Range Measurement
* 6. Range Doppler Response
* 7. CFAR implementation
