# Data Platform: K8s Task

## Prerequisites

- Download minikube [here](https://minikube.sigs.k8s.io/docs/start/?arch=%2Fmacos%2Farm64%2Fstable%2Fbinary+download). Please select the correct option for your local machine.

- Ensure docker is running locally.

- Run `minikube start`. You should be able to run `kubectl get pods -A` and get an output similar to this:
```
NAMESPACE     NAME                               READY   STATUS    RESTARTS      AGE
kube-system   coredns-7db6d8ff4d-t72sm           1/1     Running   0             59s
kube-system   etcd-minikube                      1/1     Running   0             73s
kube-system   kube-apiserver-minikube            1/1     Running   0             74s
kube-system   kube-controller-manager-minikube   1/1     Running   0             73s
kube-system   kube-proxy-6rc96                   1/1     Running   0             59s
kube-system   kube-scheduler-minikube            1/1     Running   0             73s
kube-system   storage-provisioner                1/1     Running   1 (46s ago)   72s
```

## The task

1. Create a namespace for your resources to be deployed into

2. Inspect the files should you wish and then run the following, ensuring they are deployed into your new namespace: 
`kubectl apply -f 100-environment && kubectl apply -f 200-resources`

3. You'll notice an error. Please fix the issue with the deployment and re-apply.

4. The aim now is to be able to view the deployment in your browser by running a `port-forward` Kubernetes command. To begin, attempt to view the pods in your namespace. Diagnose and resolve any issues that you're able to notice until we have some running pods.

5. Now that our pods are in a healthy state, we’ll need a service to be able to view the web server in your browser. Create the service with type `NodePort` and ensure we’re using the correct ports for the deployment.