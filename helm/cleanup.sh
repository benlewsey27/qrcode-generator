#!/bin/bash

persistentVolumeClaims=$(kubectl get pvc --no-headers | awk '{print $1}' )
for pvc in $persistentVolumeClaims; do
  echo "> Deleting $pvc..."
  kubectl delete pvc $pvc
done

echo "Done."
