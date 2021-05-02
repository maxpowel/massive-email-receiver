Configure the secret and configmap in `deployment.yml`, then apply it.
For the secret (mongo_uri), use:
```bash
echo -n "mongodb+srv://user:pass@my_replica_set.com/database" | base64
```

The use a load balancer to expose the pod to internet, I use nginx-ingress and this
extremely useful tutorial: https://stackoverflow.com/questions/61430311/exposing-multiple-tcp-udp-services-using-a-single-loadbalancer-on-k8s