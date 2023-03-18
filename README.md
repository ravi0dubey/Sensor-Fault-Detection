# Sensor-Fault-Detection

## Problem Statement

The Air Pressure System(APS) is a critical component of a heavy-duty vehicle that uses compressed air to force a piston to provide pressure to the brake pads, slowing down the vehicle.
It is a Binary Classification problem, in which the affirmative class indicates that the failure was caused by a certain component of the APS, while the negative class indicates that the failure was caused by something else.

## Solution Proposed

In this project, the focus is to correctly predict the class of dataset to detemine the fault is due to APS or some other system.
Goal is to reduce the cost due to unnecessary repairs. So it is required to minimize the false predictions

## Training Pipeline
![image](https://user-images.githubusercontent.com/38419795/225762823-2756c612-b41e-4418-9e86-b94c81f10252.png)


## Data Ingestion pipeline
![image](https://user-images.githubusercontent.com/38419795/225761627-e7bb0f6f-724d-4b94-a181-06136365932d.png)

## Folder structure of Artifact which gets created on running Training Pipeline

![image](https://user-images.githubusercontent.com/38419795/226071961-d9678667-cf9e-4410-a9d4-6a4293f4ae1e.png)

## Approach while doing the coding
![image](https://user-images.githubusercontent.com/38419795/226114307-71505cd5-8bb4-44fb-b0e1-1e28a5b045ec.png)
1. Define all constants used which will be used under constants folder
2. In Entity folder we declare configuration and artifact of the component
3. Train Pipeline uses both configuration and artifact of the component
4. Components like data ingestion, data validation etc. will be declared which will be used by pipeline



