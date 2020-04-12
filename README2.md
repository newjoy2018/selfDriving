# P2_Radar_Target_Generation_and_Detection
Udacity_SensorFusion
Project 2: Radar Target Generation and Detection

* Refer to `radar_target_generation_and_detection.m`

---
## 1. Implementation steps for the 2D CFAR process
In a noisy environment full of clutter noise with changing noise level, a constant threshold is often useless. Because the noise level may change over time. We need to dynamically filter the noise. CFAR is such a great algorithm to solve this problem. Because CFAR varies the threshold based on surroundings by using sliding window, so that it offers a constant false alarm rate. In 2D CFAR, it is implemented in both dimentions of range doppler block. The block consists of CUT(Cell Under Test) in the center, surrounded by guard cells and training cells. Therefore, we have following **2D CFAR process steps**:
* 1. Determine the number of Training cells and Guard cells in both dimensions.
* 2. Use for-Loop to calculate the average noise level across all the training cells.
* 3. Multiply the offset to the average noise level, so that we get the threshold.
* 4. Compare the **CUT signal** with the **threshold**, so that we get a resulted signal map with only 0 and 1.
* 5. Assign 0 to the edge cells, which are not covered by CUT because of surrounded guard cells and training cells.

---
## 2. Selection of Training, Guard cells and offset.
* **Training cells** The cells we use to calculate the average noise level is the training cells. By definition, CFAR hopes to define the threshold by calculating the average noise level of the cells around the target, multiplied by an offset value. So the training cells should surround the CUT.       **The number of training cells** should be determined according to the environment. For example, a criterion should be that the range of training cells must not contain other CUT. If there are too many training cells, other CUTs may be contained and the resulted threshold will be very large. In this case, targets may be missed. On the contrary, there will be too many false targets being detected. Here we choose:
```
Tr = 10;    % Number of training cells in range dimension
Td = 8;     % Number of training cells in doppler dimension
```

* **Guard cells** Considering various strength of target reflection, in practice, the target is not possible to be "contained" in only one cell. If we only use one cell to "contain" the target signal, other part of it will "leak" to training cells, which will lead to a false threshold.  So **the number of guard cells** should be determined by the strength of target reflection. Stronger the target reflection, more the leakage out of CUT, more the guard cells should have. Here we choose:
```
Gr = 10;    % Number of guard cells in range dimension
Gd = 8;     % Number of guard cells in doppler dimension
```

* **Offset** Offset is used to scale the average noise level. Because **average** means half of the noise level is higher than it. If we use the average value directly as the threshold, there will be a surprisingly number of false targets been detected. So scaling it is necessary. It should be noted that, as a factor, if it is given as logarithmic form, simply add it.

---
## 3.Steps taken to suppress the non-thresholded cells at the edges.




---
## 1. Define Radar Specifications 
* Frequency of operation = 77GHz
* Range Resolution = 1 m
* Max Range = 200m
* Max Velocity = 100 m/s
```
max_range_of_radar = 200;
range_resolution_of_radar = 1;
max_velocity_of_radar = 100;
speed of light = 3e8;
```

---
## 2. User Defined Range and Velocity of Target

* Define the target's initial position and velocity. 
* Note : Velocity remains constant
```
initial_range = 20;
target_velocity  = 30;
```

---
## 3. FMCW Waveform Generation
* Design the FMCW waveform by giving the specs of each of its parameters.
* Calculate the Bandwidth (B), Chirp Time (Tchirp) and Slope (slope) of 
* the FMCW chirp using the requirements above.

* Operating carrier frequency of Radar 
```
fc= 77e9;             %carrier freq
sweep_time_factor = 5.5;

B = speed_of_light / (2 * range_resolution_of_radar);
Tchirp = (sweep_time_factor*2*max_range_of_radar)/speed_of_light;
slope = B/Tchirp;
```                                                          
* The number of chirps in one sequence. 
* Its ideal to have `2^value` for the ease of running the FFT for
* Doppler Estimation. 
```
Nd=128;                   % # of doppler cells OR # of sent periods % number of chirps
```
* The number of samples on each chirp. 
```
Nr=1024;                  % for length of time OR # of range cells
```
* Timestamp for running the displacement scenario for every sample on each chirp
```
t=linspace(0,Nd*Tchirp,Nr*Nd); %total time for samples
```
* Creating the vectors for Tx, Rx and Mix based on the total samples input.
```
Tx=zeros(1,length(t)); %transmitted signal
Rx=zeros(1,length(t)); %received signal
Mix = zeros(1,length(t)); %beat signal
```
* Similar vectors for range_covered and time delay.
```
r_t=zeros(1,length(t)); % range_covered
td=zeros(1,length(t)); % time delay
```

---
## 4. Signal generation and Moving Target simulation
Running the radar scenario over the time.
```
for i=1:length(t)         
    % For each time stamp update the Range of the Target for constant velocity. 
    r_t(i) = initial_range + (target_velocity*t(i));
    td(i) = (2*r_t(i)) / speed_of_light;

    % For each time sample we need update the transmitted and received signal. 
    Tx(i) =  cos( 2*pi*( fc*(t(i) ) + ( 0.5 * slope * t(i)^2) ) );
    Rx (i)  = cos( 2*pi*( fc*(t(i)-td(i) ) + ( 0.5 * slope * (t(i)-td(i))^2) ) );

    % Now by mixing the Transmit and Receive generate the beat signal
    % This is done by element wise matrix multiplication of Transmit and Receiver Signal
    Mix(i) =  Tx(i) .* Rx(i); 
end
```

---
## 5. Range Measurement

* Reshape the vector into Nr*Nd array. 
* Nr and Nd here would also define the size of Range and Doppler FFT respectively.
```
Mix = reshape(Mix,[Nr,Nd]);
```
* run the FFT on the beat signal along the range bins dimension (Nr) and normalize.
```
sig_fft1 = fft(Mix,Nr) ./ Nr;
```
* Take the absolute value of FFT output
```
sig_fft1 = abs(sig_fft1);  
```
* Output of FFT is double sided signal, but we are interested in only one side of the spectrum.
* Hence we throw out half of the samples.
```
single_side_sig_fft1 = sig_fft1(1:Nr/2);
```
* Plotting the range, plot FFT output 
```
figure ('Name','Range from First FFT')
subplot(2,1,1)
plot(single_side_sig_fft1); 
axis ([0 200 0 1]);
```

---
## 6. Range Doppler Response
* The 2D FFT implementation is already provided here. 
* This will run a 2DFFT on the mixed signal (beat signal) output and generate a range doppler map.
* You will implement CFAR on the generated RDM Range Doppler Map Generation.
* The output of the 2D FFT is an image that has reponse in the range and doppler FFT bins. 
* So, it is important to convert the axis from bin sizes to range and doppler based on their Max values.
```
Mix = reshape(Mix,[Nr,Nd]);
```
* 2D FFT using the FFT size for both dimensions.
```
sig_fft2 = fft2(Mix,Nr,Nd);
```
* Taking just one side of signal from Range dimension.
```
sig_fft2 = sig_fft2(1:Nr/2,1:Nd);
sig_fft2 = fftshift (sig_fft2);
RDM = abs(sig_fft2);
RDM = 10*log10(RDM) ;
```
* Use the surf function to plot the output of 2DFFT and to show axis in both dimensions
```
doppler_axis = linspace(-100,100,Nd);
range_axis = linspace(-200,200,Nr/2)*((Nr/2)/400);
figure ('Name','Range and Speed From FFT2')
surf(doppler_axis,range_axis,RDM);
```

---
## 7. CFAR implementation
* Slide Window through the complete Range Doppler Map
* Select the number of Training Cells in both the dimensions.
```
Tr = 10;
Td = 8;
```
* Select the number of Guard Cells in both dimensions around the Cell under test (CUT) for accurate estimation
```
Gr = 4;
Gd = 4;
```
* Offset the threshold by SNR value in dB
```
offset = 1.4;
```
* Create a vector to store noise_level for each iteration on training cells
```
noise_level = zeros(1,1);
```

* Create a vector to store noise_level for each iteration on training cells
* Design a loop such that it slides the CUT across range doppler map.
* Make sure the CUT has margin for Training and Guard cells from the edges.
* For every iteration sum the signal level within all the training cells.
* To sum convert the value from logarithmic to linear using `db2pow` function.
* Average the summed values for all of the training cells used.
* After averaging convert it back to logarithmic using pow2db.
* Further add the offset to it to determine the threshold.
* Next, compare the signal under CUT against this threshold.
* If the CUT level > threshold assign it a value of `1`, else equate it to `0`.
* Use `RDM[x,y]` as the matrix from the output of 2D FFT for implementing CFAR.

```   
RDM = RDM/max(max(RDM));

for i = Tr+Gr+1:(Nr/2)-(Gr+Tr)
    for j = Td+Gd+1:Nd-(Gd+Td)
        
       %Create a vector to store noise_level for each iteration on training cells
        noise_level = zeros(1,1);
        
        % Calculate noise SUM in the area around CUT
        for p = i-(Tr+Gr) : i+(Tr+Gr)
            for q = j-(Td+Gd) : j+(Td+Gd)
                if (abs(i-p) > Gr || abs(j-q) > Gd)
                    noise_level = noise_level + db2pow(RDM(p,q));
                end
            end
        end
        
        % Calculate threshould from noise average then add the offset
        threshold = pow2db(noise_level/(2*(Td+Gd+1)*2*(Tr+Gr+1)-(Gr*Gd)-1));
        threshold = threshold + offset;
        CUT = RDM(i,j);
        
        if (CUT < threshold)
            RDM(i,j) = 0;
        else
            RDM(i,j) = 1;
        end
    end
end
```
* The process above will generate a thresholded block, which is smaller than the Range Doppler Map as the CUT cannot be located at the edges of matrix. Hence,few cells will not be thresholded. To keep the map size same set those values to 0. 
```
RDM(union(1:(Tr+Gr),end-(Tr+Gr-1):end),:) = 0;
RDM(:,union(1:(Td+Gd),end-(Td+Gd-1):end)) = 0;
```
* Display the CFAR output using the Surf function like we did for Range Doppler Response output.
```
figure,surf(doppler_axis,range_axis,RDM);
colorbar;
```

