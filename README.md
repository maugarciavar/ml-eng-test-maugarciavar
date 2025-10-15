# Wall Detection API

## Build the Docker Image. The . at the end is to indicate that the dockerfile is in the current directory where running the docker build command
docker build -t wall-detector .

## Run this to run/activate the container and expose port 3000
docker run -p 3000:3000 wall-detector

## Example test, the input image must be .pdf as in the original dataset, avoid spaces in the filename. The output will be generated in image format png.
curl -X POST -F "image=@A0.54-FOURTH-FLOOR-REFERENCE-PLAN-Rev.1.pdf" "http://localhost:3000/run-inference?type=wall" -o output.png

## This project serves as a demonstration of API design, computer vision processing, and Docker containerization skills.The current approach uses traditional OpenCV-based image processing for wall detection. While it performs reasonably on clean blueprints, the results can be significantly improved by training and integrating a deep learning segmentation model (for example, U-Net or SegNEt) to learn wall features and better distinguish text and symbols. This could be achieved by using pytorch or ultralytics. 