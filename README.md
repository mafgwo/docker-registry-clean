# docker-registry-clean
Docker Registry tag清理

# 脚本部署
直接通过一下Docker命令启动就等于部署成功了脚本
```bash
docker run -d \
 -e REGISTRY_URL=http://192.168.90.221:5000 \
 -e REMAIN_TAG_NUM=10 \
 -e REPO_REGEX_PATTERN="^tools.*" \
 --name registry-clean mafgwo/registry-clean:1.0
```

启动之后可以通过以下命令查看脚本执行情况，脚本某人一分钟执行一次，所以执行以下查看日志的命令后等待一会能看到正常的日志输出说明成功了，如果想要看到删除的tag的日志请确保仓库中的tag数量超过了保留的数量。
```bash
docker logs -f registry-clean
```
