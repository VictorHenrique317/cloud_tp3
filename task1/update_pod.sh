#!/bin/bash

kubectl delete configmap pyfile
kubectl delete configmap outputkey
kubectl delete configmap requirementsfile

kubectl create configmap pyfile --from-file pyfile=func.py --output yaml > pyfile.yaml
kubectl create configmap outputkey --from-literal REDIS_OUTPUT_KEY=victorribeiro-proj3-output --output yaml > outputkey.yaml
kubectl create configmap requirementsfile --from-file requirementsfile=requirements.txt --output yaml > requirementsfile.yaml

kubectl apply -f pyfile.yaml
kubectl apply -f outputkey.yaml
kubectl apply -f requirementsfile.yaml
kubectl apply -f serverless-deployment-course.yaml

pod_name=$(kubectl get pods -o jsonpath='{.items[0].metadata.name}')
kubectl delete pod $pod_name