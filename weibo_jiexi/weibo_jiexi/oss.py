import oss2

auth = oss2.Auth(access_key_id='LTAI4FrGET9fbdXbxfDttvaV', access_key_secret='Z8J3jY5jmJzznudgeg2LnNtND9Y89U')
# ECS内网
# endpoint = 'oss-cn-hangzhou-internal.aliyuncs.com'
# bucket_name = 'entertain-kr.oss-cn-hangzhou-internal.aliyuncs.com'

# 外网
endpoint = ' oss-cn-beijing.aliyuncs.com'
bucket_name = ' entertainment-weibo'

bucket = oss2.Bucket(auth, endpoint, bucket_name, connect_timeout=60)


def upload(filestream, filepath):
    try:
        result = bucket.put_object(filepath, filestream)
    except FileNotFoundError as e:
        print('说明本地文件不存在')
        raise Exception(e)
    if result.status == 200:
        base_url = 'https://entertainment-weibo.oss-cn-beijing.aliyuncs.com'
        return '{}/{}'.format(base_url, filepath)