kubectl delete configmap pyfile
kubectl delete configmap outputkey
kubectl delete configmap requirementsfile
kubectl delete deployment serverless-deployment-course

kubectl apply -f pyfile.yaml
kubectl apply -f outputkey.yaml
kubectl apply -f requirementsfile.yaml
kubectl apply -f serverless-deployment-course.yaml