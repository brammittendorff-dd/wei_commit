import oss2

auth = oss2.Auth(access_key_id='LTAIOk8WUKDknyqp', access_key_secret='bKw5pntIa23VNtbT63wrptN5MJBUf5')
# ECS内网
endpoint = 'oss-cn-hangzhou-internal.aliyuncs.com'
bucket_name = 'entertain-kr.oss-cn-hangzhou-internal.aliyuncs.com'

# 外网
endpoint = 'oss-cn-hangzhou.aliyuncs.com'
bucket_name = 'entertain-kr'

bucket = oss2.Bucket(auth, endpoint, bucket_name, connect_timeout=60)


def upload(filestream, filepath):
    try:
        result = bucket.put_object(filepath, filestream)
    except FileNotFoundError as e:
        print('说明本地文件不存在')
        raise Exception(e)
    if result.status == 200:
        base_url = 'https://entertain-kr.oss-cn-hangzhou.aliyuncs.com'
        return '{}/{}'.format(base_url, filepath)