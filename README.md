# Sensor-Fault-Detection

## Problem Statement

The Air Pressure System(APS) is a critical component of a heavy-duty vehicle that uses compressed air to force a piston to provide pressure to the brake pads, slowing down the vehicle.
It is a Binary Classification problem, in which the affirmative class indicates that the failure was caused by a certain component of the APS, while the negative class indicates that the failure was caused by something else.

## Solution Proposed

In this project, the focus is to correctly predict the class of dataset to detemine the fault is due to APS or some other system.
Goal is to reduce the cost due to unnecessary repairs. So it is required to minimize the false predictions

## Approach while doing the coding
![image](https://user-images.githubusercontent.com/38419795/226114307-71505cd5-8bb4-44fb-b0e1-1e28a5b045ec.png)
1. Define all constants used which will be used under constants folder
2. In Entity folder we declare configuration and artifact of the component
3. Train Pipeline uses both configuration and artifact of the component
4. Components like data ingestion, data validation etc. will be declared which will be used by pipeline


## Training Pipeline
![image](https://user-images.githubusercontent.com/38419795/225762823-2756c612-b41e-4418-9e86-b94c81f10252.png)

## Data Ingestion pipeline
![image](https://user-images.githubusercontent.com/38419795/225761627-e7bb0f6f-724d-4b94-a181-06136365932d.png)

## Folder structure of Artifact which gets created on running Training Pipeline
#### Data Ingestion
![image](https://user-images.githubusercontent.com/38419795/226071961-d9678667-cf9e-4410-a9d4-6a4293f4ae1e.png)\n
#### Data Validation 
![image](https://user-images.githubusercontent.com/38419795/226494010-ac475551-5159-46ce-84c2-a3e2904e249b.png)

## Data Validation pipeline
![image](https://user-images.githubusercontent.com/38419795/226127381-6ddfd989-76e2-4087-86e8-c1cd0daa846b.png)

![image](https://user-images.githubusercontent.com/38419795/226118592-44360d9b-fcaa-40e3-b4b5-936f7dcd760d.png)

#### Data Transformation
![image](https://user-images.githubusercontent.com/38419795/227364255-1657eb48-628a-4c22-a073-1d21fa3c37c9.png)

#### Model Evaluation
Models will be stored in timestamp folder \n
![image](https://user-images.githubusercontent.com/38419795/227789015-c9e7434a-5a76-4977-b53a-9929721f8231.png)


## Data Drift Detection
![image](https://user-images.githubusercontent.com/38419795/226199171-c98ae16f-5007-484e-b5f9-5b3d3e73cc92.png)

## Concept Drift Detection
![image](https://user-images.githubusercontent.com/38419795/226199601-27d1bf75-0556-4275-9c53-21bef8891f66.png)

## Target Drift Detection
![image](https://user-images.githubusercontent.com/38419795/226200126-e31f41e5-c791-43f7-8a57-4df7700a3cce.png)





