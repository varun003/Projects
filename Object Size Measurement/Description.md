# Object-Size-Measurement

### Workflow
1. Image pre-processing
  
* Reading and resizing image
* converting image to grayscale
* using Gaussian blur to remove unnecessary edges
* Using canny,dilate and erode to get better edges
* Applying thershold value to receive further better edges

2. Object Segmentation

* Finding contours
* Sorting contours from left to right in correct order
* Removing unnecessary contours having area less than 10000

3. Creating reference object and calculate pixels of reference object
4. Draw BB around each object and calculating its height and width
