# coding: utf-8
from sqlalchemy import Column, DateTime, Index, String, Text
from sqlalchemy.dialects.mysql import DATETIME, INTEGER, LONGTEXT, SMALLINT, TINYINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Adminuser(Base):
    __tablename__ = 'adminuser'

    id = Column(INTEGER(11), primary_key=True)
    first_name = Column(VARCHAR(255), nullable=False)
    last_name = Column(VARCHAR(255), nullable=False)
    login = Column(VARCHAR(80), nullable=False, unique=True)
    email = Column(VARCHAR(255), nullable=False, unique=True)
    password = Column(VARCHAR(255), nullable=False)
    active = Column(TINYINT(1), nullable=False)
    confirmed_at = Column(DATETIME(fsp=6), nullable=False)


class Allcomment(Base):
    __tablename__ = 'allcomment'

    id = Column(INTEGER(11), primary_key=True)
    commrnt_content = Column(VARCHAR(128), nullable=False)
    commentator = Column(VARCHAR(32), nullable=False)
    comment_time = Column(VARCHAR(32), nullable=False)
    is_interesting = Column(TINYINT(1), nullable=False)
    comment_label = Column(INTEGER(11), nullable=False)
    event_id = Column(INTEGER(11), nullable=False)


class Article(Base):
    __tablename__ = 'article'

    id = Column(INTEGER(11), primary_key=True)
    label_id = Column(INTEGER(11))
    title = Column(VARCHAR(128))
    create_time = Column(DATETIME(fsp=6), nullable=False)
    release_time = Column(DATETIME(fsp=6), nullable=False)
    release_state = Column(INTEGER(11), nullable=False)
    read_amount = Column(INTEGER(11), nullable=False)
    article_data = Column(LONGTEXT)
    share_image_url = Column(VARCHAR(32))
    source = Column(VARCHAR(128))
    url = Column(VARCHAR(128))
    source_id = Column(VARCHAR(128))


class ArticleManySource(Base):
    __tablename__ = 'article_many_source'

    id = Column(INTEGER(11), primary_key=True)
    source_id = Column(INTEGER(11))
    article_id = Column(INTEGER(11))


class AuthGroup(Base):
    __tablename__ = 'auth_group'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(VARCHAR(80), nullable=False, unique=True)


class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = Column(INTEGER(11), primary_key=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DATETIME(fsp=6))
    is_superuser = Column(TINYINT(1), nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(TINYINT(1), nullable=False)
    is_active = Column(TINYINT(1), nullable=False)
    date_joined = Column(DATETIME(fsp=6), nullable=False)


class Baike(Base):
    __tablename__ = 'baike'

    id = Column(INTEGER(11), primary_key=True)
    yiming = Column(VARCHAR(64))
    zhongwenming = Column(VARCHAR(32))
    waiwenming = Column(VARCHAR(64))
    cengyongming = Column(VARCHAR(64))
    chuohao = Column(VARCHAR(64))
    waihao = Column(VARCHAR(64))
    ribenyiming = Column(VARCHAR(64))
    yuanyiming = Column(VARCHAR(64))
    chenghu = Column(VARCHAR(64))
    yuanming = Column(VARCHAR(64))
    guoji = Column(VARCHAR(64))
    minzu = Column(VARCHAR(64))
    shengri = Column(VARCHAR(64))
    zuji = Column(VARCHAR(64))
    huji = Column(VARCHAR(64))
    jiaxiang = Column(VARCHAR(64))
    chushengde = Column(VARCHAR(64))
    zujiguxiang = Column(VARCHAR(64))
    zhengzhixinyang = Column(VARCHAR(64))
    shuxiang = Column(VARCHAR(64))
    xingzuo = Column(VARCHAR(64))
    xuexing = Column(VARCHAR(64))
    sanweichicun = Column(VARCHAR(64))
    shengao = Column(VARCHAR(128))
    tizhong = Column(VARCHAR(128))
    jiaochicun = Column(VARCHAR(128))
    xiema = Column(VARCHAR(128))
    xiehao = Column(VARCHAR(128))
    xuewei = Column(VARCHAR(128))
    citiao = Column(VARCHAR(256))
    type = Column(INTEGER(11))
    sourcecategory_id = Column(INTEGER(11))
    chushengriqi = Column(VARCHAR(64))


class Baikearound(Base):
    __tablename__ = 'baikearound'

    id = Column(INTEGER(11), primary_key=True)
    baike_id = Column(INTEGER(11))
    zongjiao = Column(VARCHAR(64))
    zongjiaoxinyang = Column(LONGTEXT)
    xinyangzongjiao = Column(LONGTEXT)
    jingtongyuyan = Column(LONGTEXT)
    suohuiyuyan = Column(LONGTEXT)
    shanchangyuyan = Column(LONGTEXT)
    zhangwowaiyu = Column(LONGTEXT)
    shanchangdeyuyan = Column(LONGTEXT)
    yuyannengli = Column(LONGTEXT)
    zhiye = Column(LONGTEXT)
    qianyuegongsi = Column(LONGTEXT)
    jingjigongsi = Column(LONGTEXT)
    changpiangongsi = Column(LONGTEXT)
    gerenchangpiangongsi = Column(LONGTEXT)
    yinyuezhizuogongsi = Column(LONGTEXT)
    ribenchangpiangongsi = Column(LONGTEXT)
    neidijingji = Column(LONGTEXT)
    danwei = Column(LONGTEXT)
    yanchugongsi = Column(LONGTEXT)
    zhongguodailigongsi = Column(LONGTEXT)
    xuanchuangongsi = Column(LONGTEXT)
    yuandanwei = Column(LONGTEXT)
    xiandanwei = Column(LONGTEXT)
    suoshuchangpiangongsi = Column(LONGTEXT)
    yinyuegongsi = Column(LONGTEXT)
    yingshigongsi = Column(LONGTEXT)
    shishanggongsi = Column(LONGTEXT)
    zhongguojingjigongsi = Column(LONGTEXT)
    motegongsi = Column(LONGTEXT)
    chudaogequ = Column(LONGTEXT)
    chudaozuopin = Column(LONGTEXT)
    chenglishijian = Column(LONGTEXT)
    chudaonianfen = Column(LONGTEXT)
    zhiwu = Column(LONGTEXT)
    gongzuolinian = Column(LONGTEXT)
    jiaoyuchengdu = Column(LONGTEXT)
    biyeyuanxiao = Column(LONGTEXT)
    jiuduyuanxiao = Column(LONGTEXT)
    jiuduxuexiao = Column(LONGTEXT)
    jinxiuyuanxiao = Column(LONGTEXT)
    liuxueyuanxiao = Column(LONGTEXT)
    biyeyuanxi = Column(LONGTEXT)
    liuxuexueyuan = Column(LONGTEXT)
    biyeshijian = Column(LONGTEXT)
    yueqi = Column(LONGTEXT)
    shanchangyundong = Column(LONGTEXT)
    yundongzhuanchang = Column(LONGTEXT)
    gerencaiyi = Column(LONGTEXT)
    shanchangyueqi = Column(LONGTEXT)
    yundongtechang = Column(LONGTEXT)
    yanzouyueqi = Column(LONGTEXT)
    zhuanchang = Column(LONGTEXT)
    shanchang = Column(LONGTEXT)
    yishutechang = Column(LONGTEXT)
    zuishanchangdeyueqi = Column(LONGTEXT)
    zuishuxideyueqi = Column(LONGTEXT)
    yueqizhuanchang = Column(LONGTEXT)
    tebiezhuanchang = Column(LONGTEXT)
    renshenggeyan = Column(LONGTEXT)
    shenghuoxinnian = Column(LONGTEXT)
    gerenlixiang = Column(LONGTEXT)
    gerenmingyan = Column(LONGTEXT)
    zuixihuandeyundong = Column(LONGTEXT)
    xiaiyundong = Column(LONGTEXT)
    gerenaihao = Column(LONGTEXT)
    xingqu = Column(LONGTEXT)
    shihao = Column(LONGTEXT)
    richangaihao = Column(LONGTEXT)
    xingqutechang = Column(LONGTEXT)
    renwuguandian = Column(LONGTEXT)
    caifupaiming = Column(LONGTEXT)
    QQhaoma = Column(LONGTEXT)
    weixinpingtai = Column(LONGTEXT)
    xinlangweiboID = Column(LONGTEXT)
    guanwang = Column(LONGTEXT)
    instagram = Column(LONGTEXT)
    FB = Column(LONGTEXT)
    twitter = Column(LONGTEXT)
    douyin = Column(LONGTEXT)
    yuletuanti = Column(LONGTEXT)
    suoshufenzu = Column(LONGTEXT)
    suoshutuandui = Column(LONGTEXT)
    zongyizuhe = Column(LONGTEXT)
    duineizhiwu = Column(LONGTEXT)
    zhuchang = Column(LONGTEXT)
    jitashou = Column(LONGTEXT)
    jianpanshou = Column(LONGTEXT)
    zuhezhuchang = Column(LONGTEXT)
    zuhelingwu = Column(LONGTEXT)
    duineizhiwei = Column(LONGTEXT)
    duizhongzhiwu = Column(LONGTEXT)
    fensiming = Column(LONGTEXT)
    fensimingzi = Column(LONGTEXT)
    fensinicheng = Column(LONGTEXT)
    fensi = Column(LONGTEXT)
    yingyouhui = Column(LONGTEXT)
    Fansnicheng = Column(LONGTEXT)
    guanfangfensiming = Column(LONGTEXT)
    fensimingci = Column(LONGTEXT)
    gemimingcheng = Column(LONGTEXT)
    fensituan = Column(LONGTEXT)
    quanqiufensihui = Column(LONGTEXT)
    fensizicheng = Column(LONGTEXT)
    fensichengwei = Column(LONGTEXT)
    fensituantimingcheng = Column(LONGTEXT)
    fensizuzhi = Column(LONGTEXT)
    fensituanyingyuanse = Column(LONGTEXT)
    gerenyingyuanse = Column(LONGTEXT)
    yingyuandaibiaose = Column(LONGTEXT)
    guanfangyingyuanse = Column(LONGTEXT)
    daibiaose = Column(LONGTEXT)
    duineidaibiaoyanse = Column(LONGTEXT)
    chenghao = Column(LONGTEXT)
    huodederongyu = Column(LONGTEXT)
    gongyijijin = Column(LONGTEXT)
    gongyi = Column(LONGTEXT)
    gerenjijin = Column(LONGTEXT)
    cishanmujuanshiye = Column(LONGTEXT)
    xiwangxiaoxue = Column(LONGTEXT)
    gongyituanti = Column(LONGTEXT)
    yundongxiangmu = Column(LONGTEXT)
    zhuanyetedian = Column(LONGTEXT)
    bisaishuju = Column(LONGTEXT)
    jiaozhang = Column(LONGTEXT)
    liankaochengji = Column(LONGTEXT)
    liankaopaiming = Column(LONGTEXT)
    shijieyulianIDhao = Column(INTEGER(11))
    buduiguanzhi = Column(LONGTEXT)
    daiyanpinpai = Column(LONGTEXT)
    qushishijian = Column(LONGTEXT)
    gerengongzuoshi = Column(LONGTEXT)
    gerengongzuoshi1 = Column(LONGTEXT)
    gerengongzuoshi2 = Column(LONGTEXT)
    zuixihuandeyiren = Column(LONGTEXT)
    zuixihuandeyanyuan = Column(LONGTEXT)
    xihuandegeshou = Column(LONGTEXT)
    zuixihuandegexing = Column(LONGTEXT)
    xihuandeyanyuan = Column(LONGTEXT)
    zuixihuandegeshou = Column(LONGTEXT)
    xihuandenangeshou = Column(LONGTEXT)
    xiaideyuedui = Column(LONGTEXT)
    xihuandenvyanyuan = Column(LONGTEXT)
    xihuandenanyanyuan = Column(LONGTEXT)
    xihuandeyiren = Column(LONGTEXT)
    chongwu = Column(LONGTEXT)
    xihuanyanse = Column(LONGTEXT)
    xihuandedianying = Column(LONGTEXT)
    zuixihuandeshiwu = Column(LONGTEXT)
    xihuandeshuiguo = Column(LONGTEXT)
    xihuandeshipin = Column(LONGTEXT)
    xihuandelingshi = Column(LONGTEXT)
    zuixihuandedifang = Column(LONGTEXT)
    zuixihuandehua = Column(LONGTEXT)
    xihuandeshuji = Column(LONGTEXT)
    zuixihuandejieri = Column(LONGTEXT)
    zuixihuandemanhua = Column(LONGTEXT)
    taoyandeshiwu = Column(LONGTEXT)
    zuitaoyandeshiwu = Column(LONGTEXT)
    zuitaoyandeyule = Column(LONGTEXT)
    fengge = Column(LONGTEXT)
    leixing = Column(LONGTEXT)
    Style = Column(LONGTEXT)
    yinyueleibie = Column(LONGTEXT)
    qufeng = Column(LONGTEXT)
    gequleixing = Column(LONGTEXT)
    xingge = Column(LONGTEXT)
    mudi = Column(LONGTEXT)
    jiuduzhuanye = Column(LONGTEXT)
    jiankuan = Column(LONGTEXT)
    shengxiao = Column(VARCHAR(64))
    fensikouhao = Column(LONGTEXT)
    zichuangchaoliupinpai = Column(LONGTEXT)
    chuanglipinpai = Column(LONGTEXT)
    jingdianyingmuxingxiang = Column(LONGTEXT)
    wenzhijibie = Column(VARCHAR(64))
    huajuzhicheng = Column(VARCHAR(64))
    kouhao = Column(LONGTEXT)
    guojiazhicheng = Column(LONGTEXT)
    baidutieba = Column(LONGTEXT)
    manyizijidedifang = Column(LONGTEXT)
    nonglishengri = Column(VARCHAR(64))
    chunvzuo = Column(VARCHAR(256))
    zhuanjizongxiaoliang = Column(VARCHAR(64))
    hunlian = Column(LONGTEXT)
    zuikaixindeshi = Column(LONGTEXT)
    zhongfangjingjigongsi = Column(VARCHAR(128))
    xuanchuanqihuagongsi = Column(VARCHAR(128))
    cengshutuanti = Column(VARCHAR(128))
    yuanzuhe = Column(VARCHAR(128))
    xiongdizuhe = Column(VARCHAR(128))
    qianrenchengyuan = Column(VARCHAR(128))
    zuhedandang = Column(VARCHAR(128))
    gerenzhuanshugongsi = Column(VARCHAR(128))
    suozaizuhe = Column(VARCHAR(128))
    jiuzhigongsi = Column(VARCHAR(128))
    suoshuxiaofendui = Column(VARCHAR(128))
    huodongqijian = Column(VARCHAR(128))
    zuhexiaofendui = Column(VARCHAR(128))
    chudaori = Column(VARCHAR(128))
    zuhechudaori = Column(VARCHAR(128))
    chudaoshijian = Column(VARCHAR(128))
    chudaodi = Column(VARCHAR(128))
    chudaoriqi = Column(VARCHAR(128))
    solochudaori = Column(VARCHAR(128))
    zhuanyejineng = Column(VARCHAR(128))
    suoshuyundongdui = Column(VARCHAR(128))
    jibenxinxi = Column(LONGTEXT)


class Baikeproduction(Base):
    __tablename__ = 'baikeproduction'

    id = Column(INTEGER(11), primary_key=True)
    baike_id = Column(INTEGER(11))
    daibiaozuopin = Column(LONGTEXT)
    yinyuedaibiaozuo = Column(LONGTEXT)
    yingshidaibiaozuo = Column(LONGTEXT)
    dianyingdaibiaozuo = Column(LONGTEXT)
    dianshijudaibiaozuo = Column(LONGTEXT)
    daibiaozhuanji = Column(LONGTEXT)
    chengmingzuo = Column(LONGTEXT)
    zhuyaoyinyuezuopin = Column(LONGTEXT)
    zhuanji = Column(LONGTEXT)
    danqu = Column(LONGTEXT)
    daibiaogequ = Column(LONGTEXT)
    gerenzhuanji = Column(LONGTEXT)
    gerendanqu = Column(LONGTEXT)
    yuanchuangqumu = Column(LONGTEXT)
    canyandianshiju = Column(LONGTEXT)
    zongyijiemu = Column(LONGTEXT)
    gerenxiezhen = Column(LONGTEXT)
    zuocizuopin = Column(LONGTEXT)
    canyanMV = Column(LONGTEXT)
    zhuchizuopin = Column(LONGTEXT)
    canyanduanpian = Column(LONGTEXT)
    weitarenchuangzuo = Column(LONGTEXT)
    daoyanchunvzuo = Column(LONGTEXT)
    duanjuweidianying = Column(LONGTEXT)
    touzhiyingshi = Column(LONGTEXT)
    cengzhuchijiemu = Column(LONGTEXT)
    zongyizhuchi = Column(LONGTEXT)
    chubanwu = Column(LONGTEXT)
    daibiaoshujizuopin = Column(LONGTEXT)
    canjiachunwan = Column(LONGTEXT)
    xiaopinzuopin = Column(LONGTEXT)
    canyanwangluoju = Column(LONGTEXT)
    peiyindonghuadianying = Column(LONGTEXT)
    shehuihuodong = Column(LONGTEXT)
    renwupingjia = Column(LONGTEXT)
    renwuzhengyi = Column(LONGTEXT)
    chunvzhizuo = Column(LONGTEXT)
    diyibuzuopin = Column(LONGTEXT)
    jingedaibiaozuo = Column(LONGTEXT)
    zhuyaojiangxiang = Column(LONGTEXT)
    yinyueleixing = Column(LONGTEXT)
    remengequ = Column(LONGTEXT)
    canyandianying = Column(LONGTEXT)


class Baikerelationship(Base):
    __tablename__ = 'baikerelationship'

    id = Column(INTEGER(11), primary_key=True)
    zhangfu = Column(LONGTEXT)
    qizi = Column(LONGTEXT)
    peiou = Column(LONGTEXT)
    erzi = Column(LONGTEXT)
    nver = Column(LONGTEXT)
    jiaren = Column(LONGTEXT)
    jiatingchengyuan = Column(LONGTEXT)
    danver = Column(LONGTEXT)
    xiaonver = Column(LONGTEXT)
    daerzi = Column(LONGTEXT)
    xiaoerzi = Column(LONGTEXT)
    jiazhongpaihang = Column(LONGTEXT)
    muqin = Column(LONGTEXT)
    fuqin = Column(LONGTEXT)
    jiejie = Column(LONGTEXT)
    jiatingzhuangkuang = Column(LONGTEXT)
    zinv = Column(LONGTEXT)
    airen = Column(LONGTEXT)
    zhangnv = Column(LONGTEXT)
    cinv = Column(LONGTEXT)
    jiatingqingkuang = Column(LONGTEXT)
    qinshu = Column(LONGTEXT)
    didi = Column(LONGTEXT)
    gege = Column(LONGTEXT)
    yeye = Column(LONGTEXT)
    mama = Column(LONGTEXT)
    baba = Column(LONGTEXT)
    biaoge = Column(LONGTEXT)
    jiashu = Column(LONGTEXT)
    fujun = Column(LONGTEXT)
    tongmumeimei = Column(LONGTEXT)
    fumu = Column(LONGTEXT)
    xianrenqizi = Column(LONGTEXT)
    nainai = Column(LONGTEXT)
    zhuyaojiatingchengyuan = Column(LONGTEXT)
    zufu = Column(LONGTEXT)
    zumu = Column(LONGTEXT)
    xiongzhang = Column(LONGTEXT)
    jiatinggoucheng = Column(LONGTEXT)
    waizengzufu = Column(LONGTEXT)
    waizufu = Column(LONGTEXT)
    xianqi = Column(LONGTEXT)
    diyirenqizi = Column(LONGTEXT)
    diyirenqianqi = Column(LONGTEXT)
    jingjiren = Column(LONGTEXT)
    tongxue = Column(LONGTEXT)
    xiaoyou = Column(LONGTEXT)
    shicheng = Column(LONGTEXT)
    enshi = Column(LONGTEXT)
    zhidaojiaoshi = Column(LONGTEXT)
    gechanglaoshi = Column(LONGTEXT)
    biaoyanlaoshi = Column(LONGTEXT)
    haopengyou = Column(LONGTEXT)
    quanneihaoyou = Column(LONGTEXT)
    yuetanhaoyou = Column(LONGTEXT)
    qianfu = Column(LONGTEXT)
    qiannanyou = Column(LONGTEXT)
    qiannvyou = Column(LONGTEXT)
    qianqi = Column(LONGTEXT)
    xiannvyou = Column(LONGTEXT)
    xiannanyou = Column(LONGTEXT)
    ganqingjingli = Column(LONGTEXT)
    zhizi = Column(LONGTEXT)
    xiangguantuanti = Column(LONGTEXT)
    cengshuzuhe = Column(LONGTEXT)
    guowangchengyuanqianrenchengyuan = Column(LONGTEXT)
    qianzuhe = Column(LONGTEXT)
    feiwen = Column(LONGTEXT)
    pengyou = Column(LONGTEXT)
    nvyou = Column(LONGTEXT)
    diyiweiqizi = Column(LONGTEXT)
    dierweiqizi = Column(LONGTEXT)
    nanyou = Column(LONGTEXT)
    quanzhonghaoyou = Column(LONGTEXT)
    haiwaijingjigongsi = Column(LONGTEXT)
    dadang = Column(LONGTEXT)
    guanfangduishou = Column(LONGTEXT)
    jiating = Column(LONGTEXT)
    nvpengyou = Column(LONGTEXT)
    tonggongsiyiren = Column(LONGTEXT)
    nanpengyou = Column(LONGTEXT)
    sudi = Column(LONGTEXT)
    dixi = Column(VARCHAR(512))
    gonggong = Column(VARCHAR(128))
    haoyou = Column(VARCHAR(128))
    jimu = Column(VARCHAR(128))
    jiuma = Column(VARCHAR(128))
    laoshi = Column(VARCHAR(128))
    meimei = Column(VARCHAR(128))
    waigong = Column(VARCHAR(128))
    waishengnv = Column(VARCHAR(128))
    xuesheng = Column(VARCHAR(128))
    yima = Column(LONGTEXT)
    yinv = Column(VARCHAR(128))
    yizi = Column(VARCHAR(128))
    yuefu = Column(VARCHAR(128))
    biaodi = Column(LONGTEXT)
    biaogufu = Column(LONGTEXT)
    biaojie = Column(LONGTEXT)
    biaomei = Column(LONGTEXT)
    biaoyi = Column(LONGTEXT)
    bobo = Column(LONGTEXT)
    bole = Column(LONGTEXT)
    chengyuan = Column(LONGTEXT)
    chuanbozhe = Column(LONGTEXT)
    dajiuge = Column(LONGTEXT)
    daoshi = Column(LONGTEXT)
    dayeye = Column(LONGTEXT)
    duishou = Column(LONGTEXT)
    duiyuan = Column(LONGTEXT)
    duizhang = Column(LONGTEXT)
    erxi = Column(LONGTEXT)
    fuqi = Column(LONGTEXT)
    gufu = Column(LONGTEXT)
    guma = Column(LONGTEXT)
    hezuoren = Column(LONGTEXT)
    jiefu = Column(LONGTEXT)
    jifu = Column(LONGTEXT)
    jinv = Column(LONGTEXT)
    jiren = Column(LONGTEXT)
    jiujiu = Column(LONGTEXT)
    jizi = Column(LONGTEXT)
    lianjin = Column(LONGTEXT)
    lingdao = Column(LONGTEXT)
    meifu = Column(LONGTEXT)
    nvxu = Column(LONGTEXT)
    ouxiang = Column(LONGTEXT)
    popo = Column(LONGTEXT)
    qianduiyou = Column(LONGTEXT)
    qidi = Column(LONGTEXT)
    qimei = Column(LONGTEXT)
    qingjiagong = Column(LONGTEXT)
    qingjiamu = Column(LONGTEXT)
    saozi = Column(LONGTEXT)
    shidi = Column(LONGTEXT)
    shifu = Column(LONGTEXT)
    shijie = Column(LONGTEXT)
    shimei = Column(LONGTEXT)
    shisheng = Column(LONGTEXT)
    shixiong = Column(LONGTEXT)
    shiye = Column(LONGTEXT)
    shizu = Column(LONGTEXT)
    shushu = Column(LONGTEXT)
    sunnv = Column(LONGTEXT)
    sunzi = Column(LONGTEXT)
    tangdi = Column(LONGTEXT)
    tangge = Column(LONGTEXT)
    tangjie = Column(LONGTEXT)
    tangmei = Column(LONGTEXT)
    tongmen = Column(LONGTEXT)
    tuandui = Column(LONGTEXT)
    tuanti = Column(LONGTEXT)
    waipo = Column(LONGTEXT)
    waisheng = Column(LONGTEXT)
    waisun = Column(LONGTEXT)
    waisunnv = Column(LONGTEXT)
    waisunzi = Column(LONGTEXT)
    weihunfu = Column(LONGTEXT)
    weihunqi = Column(LONGTEXT)
    xianfu = Column(LONGTEXT)
    xiaoguzi = Column(LONGTEXT)
    xiaoyi = Column(LONGTEXT)
    xiashu = Column(LONGTEXT)
    yangfu = Column(LONGTEXT)
    yangzi = Column(LONGTEXT)
    yifu2 = Column(LONGTEXT)
    yifu4 = Column(LONGTEXT)
    yimu = Column(LONGTEXT)
    yuemu = Column(LONGTEXT)
    zengzufu = Column(LONGTEXT)
    zhanyou = Column(LONGTEXT)
    zhinv = Column(LONGTEXT)
    zhouli = Column(LONGTEXT)
    baike_id = Column(INTEGER(11))
    duiyou = Column(LONGTEXT)
    suoshutuanti = Column(LONGTEXT)


class Ballot(Base):
    __tablename__ = 'ballot'

    id = Column(INTEGER(11), primary_key=True)
    create_time = Column(DATETIME(fsp=6), nullable=False)
    over_time = Column(DATETIME(fsp=6), nullable=False)
    title = Column(VARCHAR(512), nullable=False)
    event_id = Column(INTEGER(11))


class BallotAtitude(Base):
    __tablename__ = 'ballot_atitude'

    id = Column(INTEGER(11), primary_key=True)
    ballot_id = Column(INTEGER(11), nullable=False)
    user_id = Column(INTEGER(11), nullable=False)
    create_time = Column(DATETIME(fsp=6), nullable=False)


class BallotOption(Base):
    __tablename__ = 'ballot_option'

    id = Column(INTEGER(11), primary_key=True)
    ballot_id = Column(INTEGER(11), nullable=False)
    option = Column(VARCHAR(256), nullable=False)


class Behaviorkeyword(Base):
    __tablename__ = 'behaviorkeyword'

    id = Column(INTEGER(11), primary_key=True)
    keywordname = Column(VARCHAR(512))


class BehaviorkeywordManyEvent(Base):
    __tablename__ = 'behaviorkeyword_many_event'

    id = Column(INTEGER(11), primary_key=True)
    behaviorkeyword_id = Column(INTEGER(11))
    event_id = Column(INTEGER(11))


class Cookie(Base):
    __tablename__ = 'cookie'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(255))
    password = Column(String(255))
    cookies = Column(Text)
    create_time = Column(DateTime, nullable=False)


class Dataorigin(Base):
    __tablename__ = 'dataorigin'

    id = Column(INTEGER(11), primary_key=True)
    article_id = Column(INTEGER(11))
    dynamic_id = Column(INTEGER(11))
    label_id = Column(INTEGER(11))


class Datatype(Base):
    __tablename__ = 'datatype'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(64))


class DjangoContentType(Base):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        Index('django_content_type_app_label_model_76bd3d3b_uniq', 'app_label', 'model', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    app_label = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)


class DjangoMigration(Base):
    __tablename__ = 'django_migrations'

    id = Column(INTEGER(11), primary_key=True)
    app = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    applied = Column(DATETIME(fsp=6), nullable=False)


class DjangoSession(Base):
    __tablename__ = 'django_session'

    session_key = Column(String(40), primary_key=True)
    session_data = Column(LONGTEXT, nullable=False)
    expire_date = Column(DATETIME(fsp=6), nullable=False, index=True)


class Dynamic(Base):
    __tablename__ = 'dynamic'

    id = Column(INTEGER(11), primary_key=True)
    release_time = Column(DATETIME(fsp=6))
    release_state = Column(INTEGER(11))
    read_amount = Column(INTEGER(11))
    description = Column(String(128))
    correct_state = Column(INTEGER(11))
    data = Column(LONGTEXT)
    share_image_url = Column(String(32))
    create_time = Column(DATETIME(fsp=6))
    label_id = Column(INTEGER(11))
    dynamicsource = Column(String(128), nullable=False)
    dynamicsource_id = Column(INTEGER(11))
    url = Column(String(256))
    updata_data = Column(LONGTEXT)
    source_id = Column(String(128))


class DynamicManySource(Base):
    __tablename__ = 'dynamic_many_source'

    id = Column(INTEGER(11), primary_key=True)
    source_id = Column(INTEGER(11))
    Dynamic_id = Column(INTEGER(11))


class Dynamicsource(Base):
    __tablename__ = 'dynamicsource'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(LONGTEXT)
    weibo_ID = Column(String(100))


class Event(Base):
    __tablename__ = 'event'

    id = Column(INTEGER(11), primary_key=True)
    event_title = Column(String(32))
    event_lable = Column(INTEGER(11))
    event_time = Column(DATETIME(fsp=6))
    event_introduction = Column(LONGTEXT)
    create_time = Column(DATETIME(fsp=6), nullable=False)
    is_updata = Column(TINYINT(1), nullable=False)
    event_picture_url = Column(String(256))
    dataytpe_id = Column(INTEGER(11), nullable=False)
    likeamount = Column(INTEGER(11), nullable=False)
    unlikeamount = Column(INTEGER(11), nullable=False)


class EventGatherManyEvent(Base):
    __tablename__ = 'eventGather_many_event'

    id = Column(INTEGER(11), primary_key=True)
    eventGather_id = Column(INTEGER(11), nullable=False)
    event_id = Column(INTEGER(11), nullable=False)


class EventManySource(Base):
    __tablename__ = 'event_many_source'

    id = Column(INTEGER(11), primary_key=True)
    source_id = Column(INTEGER(11))
    Event_id = Column(INTEGER(11))


class Eventgather(Base):
    __tablename__ = 'eventgather'

    id = Column(INTEGER(11), primary_key=True)
    is_updata = Column(TINYINT(1), nullable=False)
    creat_time = Column(DATETIME(fsp=6))
    label_id = Column(INTEGER(11), nullable=False)
    introduction = Column(LONGTEXT)
    name = Column(String(128))
    picture1 = Column(String(128))
    picture2 = Column(String(128))
    state = Column(INTEGER(11), nullable=False)
    type = Column(INTEGER(11), nullable=False)
    update_time = Column(DATETIME(fsp=6), nullable=False)
    dataytpe_id = Column(INTEGER(11), nullable=False)


class Focu(Base):
    __tablename__ = 'focus'

    id = Column(INTEGER(11), primary_key=True)
    content = Column(String(128), nullable=False)
    title = Column(String(128), nullable=False)
    event_id = Column(INTEGER(11), nullable=False)
    create_time = Column(DATETIME(fsp=6), nullable=False)


class Interestingcomment(Base):
    __tablename__ = 'interestingcomment'

    id = Column(INTEGER(11), primary_key=True)
    is_show = Column(TINYINT(1), nullable=False)
    comment_id = Column(INTEGER(11), nullable=False)
    event_id = Column(INTEGER(11), nullable=False)
    label = Column(INTEGER(11))


class Keyword(Base):
    __tablename__ = 'keyword'

    id = Column(INTEGER(11), primary_key=True)
    keyword_name = Column(String(64), nullable=False)
    create_time = Column(DATETIME(fsp=6), nullable=False)


class Label(Base):
    __tablename__ = 'label'

    id = Column(INTEGER(11), primary_key=True)
    create_time = Column(DATETIME(fsp=6), nullable=False)


class Labelclas(Base):
    __tablename__ = 'labelclass'

    id = Column(INTEGER(11), primary_key=True)
    create_time = Column(DATETIME(fsp=6), nullable=False)


class Media(Base):
    __tablename__ = 'media'

    id = Column(INTEGER(11), primary_key=True)
    is_picture = Column(TINYINT(1), nullable=False)
    url = Column(String(256))
    hash = Column(String(256))


class MediaManyDyanmic(Base):
    __tablename__ = 'media_many_dyanmic'

    id = Column(INTEGER(11), primary_key=True)
    media_id = Column(INTEGER(11))
    dynamic_id = Column(INTEGER(11))


class Module(Base):
    __tablename__ = 'module'

    id = Column(INTEGER(11), primary_key=True)
    module_name = Column(String(256))


class Multimediamesource(Base):
    __tablename__ = 'multimediamesource'

    id = Column(INTEGER(11), primary_key=True)
    picture_id = Column(INTEGER(11))
    video_id = Column(INTEGER(11))
    media_id = Column(INTEGER(11))
    creat_time = Column(String(32), nullable=False)


class Onebox(Base):
    __tablename__ = 'onebox'

    id = Column(INTEGER(11), primary_key=True)
    event_id = Column(INTEGER(11), nullable=False)
    label = Column(INTEGER(11))
    describe = Column(String(256))
    onebox_picture = Column(String(128))
    onebox_time = Column(DATETIME(fsp=6), nullable=False)


class OneboxMamyDataorigin(Base):
    __tablename__ = 'onebox_mamy_dataorigin'

    id = Column(INTEGER(11), primary_key=True)
    onebox_id = Column(INTEGER(11), nullable=False)
    dataprigin_id = Column(INTEGER(11), nullable=False)


class Oneboxblack(Base):
    __tablename__ = 'oneboxblack'

    id = Column(INTEGER(11), primary_key=True)
    content = Column(LONGTEXT)


class Oneboxwhite(Base):
    __tablename__ = 'oneboxwhite'

    id = Column(INTEGER(11), primary_key=True)
    content = Column(LONGTEXT)


class Picture(Base):
    __tablename__ = 'pictures'

    id = Column(INTEGER(11), primary_key=True)
    event_id = Column(INTEGER(11), nullable=False)
    name = Column(String(64))


class Productiondevelopment(Base):
    __tablename__ = 'productiondevelopment'

    id = Column(INTEGER(11), primary_key=True)
    baike_id = Column(INTEGER(11), nullable=False)
    type = Column(String(64), nullable=False)
    url = Column(String(256), nullable=False)
    baikeID = Column(INTEGER(11), nullable=False)
    zhuanjimingcheng = Column(String(128), nullable=False)
    danqugequmingcheng = Column(String(128), nullable=False)
    dianshijumingcheng = Column(String(128), nullable=False)
    dianshijushiyanjiaose = Column(String(128), nullable=False)
    dianyingmingcheng = Column(String(128), nullable=False)
    dianyingshiyanjiaose = Column(String(128), nullable=False)
    yanchanghuimingcheng = Column(String(128), nullable=False)
    yanchanghuijubanshijian = Column(String(128), nullable=False)
    zongyijiemushijian = Column(String(128), nullable=False)
    zongyijiemubochushijian = Column(String(128), nullable=False)
    zazhixiezhen = Column(String(128), nullable=False)
    zuocigequmingcheng = Column(String(128), nullable=False)
    canyanMVgequmingcheng = Column(String(128), nullable=False)
    zhuchijiemumingcheng = Column(String(128), nullable=False)
    canyanduanpianmingcheng = Column(String(128), nullable=False)
    weitarenzuoqumingcheng = Column(String(128), nullable=False)
    daoyanzuopinmingcheng = Column(String(128), nullable=False)
    duanjuweidianyingmingcheng = Column(String(128), nullable=False)
    touzhiyingshimingcheng = Column(String(128), nullable=False)
    zhuchiyiingshimingcheng = Column(String(128), nullable=False)
    chubanshujishuming = Column(String(128), nullable=False)
    canjiachunwanjiemumingcheng = Column(String(128), nullable=False)
    canjiachunwanjiemushijian = Column(String(128), nullable=False)
    canyanwangjumingcheng = Column(String(128), nullable=False)
    peiyindonghuamingcheng = Column(String(128), nullable=False)


class Role(Base):
    __tablename__ = 'role'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(32), nullable=False)
    description = Column(String(32), nullable=False)


class Source(Base):
    __tablename__ = 'source'

    id = Column(INTEGER(11), primary_key=True)
    source_name = Column(LONGTEXT)


class Sourcemodule(Base):
    __tablename__ = 'sourcemodule'

    id = Column(INTEGER(11), primary_key=True)
    dynamiccsource_id = Column(INTEGER(11))
    module_id = Column(INTEGER(11))


class Sourcenickname(Base):
    __tablename__ = 'sourcenickname'

    id = Column(INTEGER(11), primary_key=True)
    nickname = Column(String(256))
    source_id = Column(INTEGER(11))


class Special(Base):
    __tablename__ = 'special'

    id = Column(INTEGER(11), primary_key=True)
    label_id = Column(INTEGER(11), nullable=False)
    index = Column(INTEGER(11), nullable=False)
    name = Column(String(128))
    introduction = Column(LONGTEXT)
    picture1 = Column(String(128))
    picture2 = Column(String(128))
    state = Column(INTEGER(11), nullable=False)
    type = Column(INTEGER(11), nullable=False)
    creat_time = Column(DATETIME(fsp=6))
    update_time = Column(DATETIME(fsp=6), nullable=False)
    dataytpe_id = Column(INTEGER(11), nullable=False)


class SpecialManyEvent(Base):
    __tablename__ = 'special_many_event'

    id = Column(INTEGER(11), primary_key=True)
    special_id = Column(INTEGER(11), nullable=False)
    event_id = Column(INTEGER(11), nullable=False)


class Timeline(Base):
    __tablename__ = 'timeline'

    id = Column(INTEGER(11), primary_key=True)
    title = Column(LONGTEXT)
    preface = Column(LONGTEXT)
    epilogue = Column(LONGTEXT)
    label_id = Column(INTEGER(11))
    event_id = Column(INTEGER(11))
    is_active = Column(TINYINT(1), nullable=False)
    create_time = Column(DATETIME(fsp=6), nullable=False)
    other_keyword = Column(String(128))
    star_keyword = Column(String(128))


class TimelineMamyDataorigin(Base):
    __tablename__ = 'timeline_mamy_dataorigin'

    id = Column(INTEGER(11), primary_key=True)
    timeline_id = Column(INTEGER(11), nullable=False)
    dataorigin_id = Column(INTEGER(11), nullable=False)


class Topic(Base):
    __tablename__ = 'topic'

    id = Column(INTEGER(11), primary_key=True)
    topic_name_cn = Column(String(64), nullable=False)
    topic_name_en = Column(String(64), nullable=False)
    create_time = Column(DATETIME(fsp=6), nullable=False)
    release_state = Column(INTEGER(11), nullable=False)
    avater_url = Column(String(128), nullable=False)
    background_url = Column(String(128), nullable=False)
    topic_explain = Column(String(128), nullable=False)


class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER(11), primary_key=True)
    mobile = Column(INTEGER(11), nullable=False)
    email = Column(String(32), nullable=False)
    nick_name = Column(String(32), nullable=False)
    avatar_url = Column(String(256), nullable=False)
    open_id = Column(String(256), nullable=False)
    gender = Column(INTEGER(11), nullable=False)
    country = Column(String(32), nullable=False)
    province = Column(String(32), nullable=False)
    city = Column(String(32), nullable=False)
    create_time = Column(DATETIME(fsp=6), nullable=False)


class Userfloweevent(Base):
    __tablename__ = 'userfloweevent'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False)
    is_push = Column(TINYINT(1))
    event_id = Column(INTEGER(11), nullable=False)
    followe_time = Column(String(32), nullable=False)
    last_time = Column(String(32), nullable=False)


class Userflowespecial(Base):
    __tablename__ = 'userflowespecial'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False)
    is_push = Column(TINYINT(1))
    special_id = Column(INTEGER(11), nullable=False)
    followe_time = Column(String(32), nullable=False)
    last_time = Column(String(32), nullable=False)


class Userflowestar(Base):
    __tablename__ = 'userflowestar'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False)
    is_push = Column(TINYINT(1))
    followe_time = Column(String(32), nullable=False)
    last_time = Column(String(32), nullable=False)
    source_id = Column(INTEGER(11))


class Video(Base):
    __tablename__ = 'videos'

    id = Column(INTEGER(11), primary_key=True)
    event_id = Column(INTEGER(11), nullable=False)


class Viewpoint(Base):
    __tablename__ = 'viewpoint'

    id = Column(INTEGER(11), primary_key=True)
    stand_point = Column(String(128), nullable=False)
    focus_id = Column(INTEGER(11), nullable=False)


class ViewpointManyDataorigin(Base):
    __tablename__ = 'viewpoint_many_dataorigin'

    id = Column(INTEGER(11), primary_key=True)
    dataorigin_id = Column(INTEGER(11), nullable=False)
    viewpoint = Column(INTEGER(11), nullable=False)


class AuthPermission(Base):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        Index('auth_permission_content_type_id_codename_01ab375a_uniq', 'content_type_id', 'codename', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    content_type_id = Column(INTEGER(11), nullable=False)
    codename = Column(String(100), nullable=False)


class AuthUserGroup(Base):
    __tablename__ = 'auth_user_groups'
    __table_args__ = (
        Index('auth_user_groups_user_id_group_id_94350c0c_uniq', 'user_id', 'group_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False)
    group_id = Column(INTEGER(11), nullable=False, index=True)


class DjangoAdminLog(Base):
    __tablename__ = 'django_admin_log'

    id = Column(INTEGER(11), primary_key=True)
    action_time = Column(DATETIME(fsp=6), nullable=False)
    object_id = Column(LONGTEXT)
    object_repr = Column(String(200), nullable=False)
    action_flag = Column(SMALLINT(5), nullable=False)
    change_message = Column(LONGTEXT, nullable=False)
    content_type_id = Column(INTEGER(11), index=True)
    user_id = Column(INTEGER(11), nullable=False, index=True)


class AuthGroupPermission(Base):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        Index('auth_group_permissions_group_id_permission_id_0cd325b0_uniq', 'group_id', 'permission_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    group_id = Column(INTEGER(11), nullable=False)
    permission_id = Column(INTEGER(11), nullable=False, index=True)


class AuthUserUserPermission(Base):
    __tablename__ = 'auth_user_user_permissions'
    __table_args__ = (
        Index('auth_user_user_permissions_user_id_permission_id_14a6b632_uniq', 'user_id', 'permission_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11), nullable=False)
    permission_id = Column(INTEGER(11), nullable=False, index=True)
