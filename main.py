import requests
import operator
import re
import os

registry_url = os.getenv('REGISTRY_URL', 'http://192.168.64.2:5000')
remain_num_str = os.getenv('REMAIN_TAG_NUM', '5')
remain_num = int(remain_num_str)
regex_pattern = os.getenv('REPO_REGEX_PATTERN', '.*')

# 获取所有的仓库名
def get_repositories():
    url = f'{registry_url}/v2/_catalog'
    response = requests.get(url)
    repositories = response.json().get('repositories')
    return repositories

# 获取指定仓库的所有 tag
def get_tags(repository):
    url = f'{registry_url}/v2/{repository}/tags/list'
    response = requests.get(url)
    tags = response.json().get('tags')
    return tags

# 获取指定 tag 的 Docker-Content-Digest
def get_digest(repository, tag):
    url = f'{registry_url}/v2/{repository}/manifests/{tag}'
    headers = {'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}
    response = requests.get(url, headers=headers)
    digest = response.headers.get('Docker-Content-Digest')
    return digest

# 删除指定仓库的指定 tag
def delete_tag(repository, tag):
    digest = get_digest(repository, tag)
    url = f'{registry_url}/v2/{repository}/manifests/{digest}'
    response = requests.delete(url)
    return response.status_code == 202

# 对 tag 进行排序
def sort_tags(tags):
    sorted_tags = sorted(tags, key=lambda x: tuple(map(int_or_str, re.split('[.-]', x))))
    return sorted_tags[::-1]

# 将字符串转化为数字或字符串
def int_or_str(s):
    try:
        return int(s)
    except ValueError:
        return s

# 获取所有需要处理的仓库名
repositories = [r for r in get_repositories() if re.match(regex_pattern, r)]

# 遍历所有需要处理的仓库
for repository in repositories:
    # 获取所有 tag 并排序
    tags = get_tags(repository)
    sorted_tags = sort_tags(tags)
    # 仅保留最新的两个 tag
    for tag in sorted_tags[remain_num:]:
        # 删除不需要保留的 tag
        if delete_tag(repository, tag):
            print(f'Deleted tag {tag} from repository {repository}')
        else:
            print(f'Failed to delete tag {tag} from repository {repository}')
