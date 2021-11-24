# hw2_digitsdetection
code for the  Digits detection Challenge. <br>

## Hardware
● Windows <br>
● Intel(R) CORE i7 7th Gen @ 4.00GHz <br>
● NVIDIA GeForce GTX 1050 Ti <br>

## Introduction and details
There is the outlines in this compitions <br>
1. [Installation](#Installation) <br>
2. [Getting_labels](#Getting_labels) <br>
3. [Implement](#Implement) <br>
4. [Testing](#Testing) <br>
5. [Organising Materials](#testing) <br>
6. [Results](#Results)<br>
7. [Make-Submission](#Make-Submission)<br>

## Installation
Using Anaconda and pytorch to implement this method.

    conda create -n Classification python=3.6
    conda install pytorch -c pytorch
    conda install torchvision -c pytorch

## Getting_labels
Change the path which is in the `buildlabel.py`.

    f = h5py.File('./train/digitStruct.mat','r')
    Image.open('./train/'+IMG_NAME)
In order to get the ground truth. <br>
For example： <br>
![image](https://github.com/ryanwu1717/hw2_digitsdetection/blob/main/image/labels.png)

## Implement
The code is programing on 

    Ubuntu 20.04
    python 3.6
    Nvidia GeForce 1050Ti 
    CUDA 10.2
    cuDNN v8.0.2.
 


*Step 1.* Git clone the darknet form https://github.com/AlexeyAB/darknet. <br>
 
*Step 2.* Open the file Makefile, and modify the values of some parameters, the first few lines of the makefile: turn on GPU acceleration, turn on opencv, and turn on the cuDNN. Change the value from 0 to 1. <br>

    GPU=1
    CUDNN=1
    OPENCV=1
    
*Step 3.* Recompile the darknet <br>
Requires:

- MSVC: https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community
- CMake GUI: `Windows win64-x64 Installer`https://cmake.org/download/
- Download Darknet zip-archive with the latest commit and uncompress it: [master.zip](https://github.com/AlexeyAB/darknet/archive/master.zip)

In Windows:

- Start (button) -> All programs -> CMake -> CMake (gui) ->

- [look at image](https://habrastorage.org/webt/pz/s1/uu/pzs1uu4heb7vflfcjqn-lxy-aqu.jpeg) In CMake: Enter input path to the darknet Source, and output path to the Binaries -> Configure (button) -> Optional platform for generator: `x64`  -> Finish -> Generate -> Open Project ->
![image](https://github.com/ryanwu1717/hw2_digitsdetection/blob/main/image/cmake.png)

- in MS Visual Studio: Select: x64 and Release -> Build -> Build solution

- find the executable file `darknet.exe` in the output path to the binaries you specified

![x64 and Release](https://habrastorage.org/webt/ay/ty/f-/aytyf-8bufe7q-16yoecommlwys.jpeg)
    

    
*Step 4.* Preparing the data : training data, ground truth label, and some data that the yolov4’s method needs. You can get it by `buildtext.py`.  
For example: each image's path, .data and .names <br>
![image](https://github.com/ryanwu1717/hw2_digitsdetection/blob/main/image/train.png)![image](https://github.com/ryanwu1717/hw2_digitsdetection/blob/main/image/test.png)
![image](https://github.com/ryanwu1717/hw2_digitsdetection/blob/main/image/IOCname.png)![image](https://github.com/ryanwu1717/hw2_digitsdetection/blob/main/image/IOCdata.png)

*Step 5.* After preparing all of the data, we need to Create file `yolo-obj.cfg` with the same content as in `yolov4-custom.cfg` and start to train the model with pretrain the yolo  [yolov4.conv.137](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137) model. OR tiny-yolo [yolov4.conv.137](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137)  <br>

- change line batch to [`batch=64`](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L3)
- change line subdivisions to [`subdivisions=16`](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L4)
- change line max_batches to (`classes*2000`, but not less than number of training images and not less than `6000`), f.e. [`max_batches=6000`](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L20) if you train for 3 classes
- change line steps to 80% and 90% of max_batches, f.e. [`steps=4800,5400`](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L22)
- changed the filter value such as filters=(classes + 5)x3) and the class value.** <br>
![image](https://github.com/ryanwu1717/hw2_digitsdetection/blob/main/image/modal.png)


CD to the darknet.exe folder and use this command line for training<br>
    `darknet.exe detector data/IOC.data cfg/yolov4_tiny_custom.cfg yolov4-tiny.conv.29 `

## Testing
Use this command line for testing. <br>
   ` darknet.exe detector test data/IOC.data  cfg/yolov4_tiny_custom.cfg backup/yolov4_tiny_custom_best.weights -ext_output -dont_show -out  result.json < data/test.txt`

    
    Loading weights from backup/yolov4_tiny_custom_best.weights...
    seen 64, trained: 31968 K-images (499 Kilo-batches_64)
    Done! Loaded 38 layers from weights-file
    Enter Image Path: data/IOC/test/117.jpg
    Detection layer: 30 - type = 28
    Detection layer: 37 - type = 28
    data/IOC/test/117.jpg: Predicted in 15.932000 milli-seconds.
    3: 91%
    8: 88%
And it bring out a result.json of all result it predicted


## Organising Materials
Input command to get the result form the test data by yolov4 model, the value of the bounding box is x_center, y_center, width and height. <br>
So, I load the test image size to calculate the (y1, x1, bbox_width, bbox_height) as (top , left, width ,height) in order to get the coco result. <br>
![image](https://github.com/ryanwu1717/hw2_digitsdetection/blob/main/image/answer.png)

## Results
### Prediction 
![image](https://github.com/ryanwu1717/hw2_digitsdetection/blob/main/image/predict.png)  <br> 
### speed benchmark from google Colab
![image](https://github.com/ryanwu1717/hw2_digitsdetection/blob/main/image/banchmark.png) <br> 

## Make-Submission
Use the `create_josn.py` to get the final file. <br>
Submit the file `StudentID.json`, to  get the mPA scroe from TA. <br>
