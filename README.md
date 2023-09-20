# PRX - Platform for Remote Experiemnts 🌊




# 🌊

1. Remote server execution

```sh
prx run experiment_001.yaml --server myserver.yaml --config default.conf.yaml 
```
or

```sh
prx set server myserver.yaml
prx set config default.conf.yaml

prx run experiment_001.yaml
# or overwrite configurations
prx run experiment_001.yaml --gpus A100-80GB -n 8 -c 10 --exp_name testrun
```


2. YAML script managements


```
```