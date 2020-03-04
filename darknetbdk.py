import cv2
import numpy as np
import matplotlib.pyplot as plt

#reference https://pysource.com/2019/06/27/yolo-object-detection-using-opencv-with-python/
#get image and put text and draw bound box
def dakrnet(img2):
    imgbdk=img2
    net = cv2.dnn.readNet("../yolov3.weights", "../cfg/yolov3.cfg")
    #net = cv2.dnn.readNet("../yolov3-bdg.weights", "../cfg/yolov3-bdg.cfg")
    #직접 학습한 파일 활용 yolo 코드
    classes = []
    #open("/home/dongkeun/darknet/data/bdg.names", "r")드
    #직접 학습하여 stop sign만 들어있는 names 파일 실행 코드
    with open("/home/dongkeun/darknet/data/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Loading image
    img = cv2.imread(imgbdk)
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
            cv2.putText(img, label, (x, y + 30), font, 0.7, color, 1)
    return img,label
