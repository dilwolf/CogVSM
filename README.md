## CogVSM framework

This project implements a hierarchical edge computing system with a Long Short-Term Memory (LSTM) model for cognitive video surveillance management, as described in the paper titled "Cognitive Video Surveillance Management in Hierarchical Edge Computing System with Long Short-Term Memory Model".

### Overview

The system consists of two edge nodes: the first edge node and the second edge node. The first edge node handles object detection using the YOLOv7-tiny model and communicates with the second edge node for further processing. The second edge node predicts future object occurrences using LSTM, controls threshold values, and performs motion tracking.

### Edge Node Configuration

- **First Edge Node (Client Side)**: Responsible for object detection using YOLOv7-tiny model. Utilizes Jetson Nano with an ARM A56 CPU and NVIDIA Maxwell GPU. Connected to an IP camera via USB.
  
- **Second Edge Node (Server Side)**: Conducts future object occurrence prediction with LSTM, controls threshold values, and implements motion tracking using TF-pose-estimation. 

### Performance

While motion tracking on the Jetson Nano proved too slow for real-time monitoring, our hierarchical edge computing system optimizes performance by offloading motion tracking to the second edge node.

For more details, refer to the [original paper](https://www.mdpi.com/1424-8220/23/5/2869).
