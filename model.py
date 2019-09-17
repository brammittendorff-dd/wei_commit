from sqlalchemy import CHAR, Column, DateTime, ForeignKey, Index, String, TIMESTAMP, Table, Text, text
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER, LONGTEXT, SMALLINT, TINYINT, TEXT, BOOLEAN
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db import engine
import datetime

Base = declarative_base()
metadata = Base.metadata


class AuthGroup(Base):
    __tablename__ = 'auth_group'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(80), nullable=False, unique=True)


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


t_blendinfo_star_temp = Table(
    'blendinfo_star_temp', metadata,
    Column('blendinfo_id', INTEGER(11)),
    Column('star_id', Text)
)


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


class InformationsBlendinfo(Base):
    __tablename__ = 'informations_blendinfo'

    id = Column(INTEGER(11), primary_key=True)
    channel = Column(String(255))
    content = Column(LONGTEXT, nullable=False)
    ori_date = Column(DATETIME(fsp=6), nullable=False)
    url = Column(LONGTEXT)
    pub_date = Column(DATETIME(fsp=6))
    title = Column(String(255))
    display_status = Column(TINYINT(1), nullable=False)
    tag = Column(String(255))
    star_tag = Column(String(255))
    create_time = Column(DATETIME(fsp=6), nullable=False, default=datetime.datetime.now())
    source = Column(String(255))
    publisher = Column(String(255))
    status = Column(INTEGER(11), nullable=False)


class InformationsStar(Base):
    __tablename__ = 'informations_star'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(255))
    weibo_id = Column(String(255))
    twitter_id = Column(String(255))
    tiktok_id = Column(String(255))
    facebook_id = Column(String(255))
    xiaohongshu_id = Column(String(255))
    ins_id = Column(String(255))
    last_mblog_timestamp = Column(String(255))
    last_ins_timestamp = Column(INTEGER(11), nullable=False)
    last_twitter_timestamp = Column(INTEGER(11), nullable=False)
    container_id = Column(String(255))
    create_time = Column(DATETIME(fsp=6), nullable=False, default=datetime.datetime.now())


class InformationsWbuser(Base):
    __tablename__ = 'informations_wbuser'

    id = Column(INTEGER(11), primary_key=True)
    weibo_id = Column(String(255))
    screen_name = Column(String(255))
    profile_img_url = Column(String(255))
    v_flag = Column(TINYINT(1), nullable=False)
    description = Column(LONGTEXT)
    create_time = Column(DATETIME(fsp=6), nullable=False, default=datetime.datetime.now())


class InformationsWeiboinfo(Base):
    __tablename__ = 'informations_weiboinfo'

    id = Column(INTEGER(11), primary_key=True)
    channel = Column(String(20), nullable=False)
    mid = Column(BIGINT(20), nullable=False)
    ori_date = Column(DATETIME(fsp=6), nullable=False)
    device = Column(String(255), nullable=False)
    repost_count = Column(INTEGER(11))
    comment_count = Column(INTEGER(11))
    thumb_count = Column(INTEGER(11))
    interact_count = Column(INTEGER(11))
    content = Column(LONGTEXT, nullable=False)
    uid = Column(BIGINT(20), nullable=False)
    username = Column(String(255), nullable=False)
    follower_count = Column(INTEGER(11))
    statuses_count = Column(INTEGER(11))
    following_count = Column(INTEGER(11))
    sex = Column(String(255))
    location = Column(String(255))
    authentication = Column(TINYINT(1), nullable=False)
    auth_type = Column(String(255))
    description = Column(LONGTEXT)
    url = Column(LONGTEXT)
    is_repost = Column(TINYINT(1), nullable=False)
    ori_author = Column(String(255))
    ori_content = Column(LONGTEXT)
    ori_repost_count = Column(INTEGER(11))
    ori_comment_count = Column(INTEGER(11))
    pub_date = Column(DATETIME(fsp=6))
    title = Column(String(255))
    display_status = Column(TINYINT(1), nullable=False)
    tag = Column(String(255))
    star_tag = Column(String(255))
    create_time = Column(DATETIME(fsp=6), nullable=False, default=datetime.datetime.now())
    source = Column(String(255))
    publisher = Column(String(255))
    status = Column(INTEGER(11), nullable=False)


class OnlineMedia(Base):
    __tablename__ = 'online_media'

    id = Column(INTEGER(11), primary_key=True)
    title = Column(Text(collation='utf8mb4_unicode_ci'), nullable=False)
    channel = Column(String(255, 'utf8mb4_unicode_ci'))
    date = Column(DateTime)
    content = Column(LONGTEXT)
    url = Column(Text(collation='utf8mb4_unicode_ci'), nullable=False)
    source = Column(INTEGER(11), nullable=False)
    create_time = Column(DATETIME(fsp=6), nullable=False, default=datetime.datetime.now())


class PublicFigure(Base):
    __tablename__ = 'public_figure'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    weibo_id = Column(String(255, 'utf8mb4_unicode_ci'))
    twitter_id = Column(String(255, 'utf8mb4_unicode_ci'))
    tiktok_id = Column(String(255, 'utf8mb4_unicode_ci'))
    facebook_id = Column(String(255, 'utf8mb4_unicode_ci'))
    xiaohongshu_id = Column(String(255, 'utf8mb4_unicode_ci'))
    ins_id = Column(String(255, 'utf8mb4_unicode_ci'))


class SocialMedia(Base):
    __tablename__ = 'social_media'

    id = Column(INTEGER(11), primary_key=True)
    created_at = Column(INTEGER(11), nullable=False)
    figure_id = Column(INTEGER(11), nullable=False)
    text = Column(Text)
    media_url = Column(Text)
    platform = Column(INTEGER(2), nullable=False)
    created_time = Column(DateTime)


t_stardynamics = Table(
    'stardynamics', metadata,
    Column('id', String(11)),
    Column('desc', String(255)),
    Column('text', LONGTEXT),
    Column('media_url', LONGTEXT),
    Column('platform', LONGTEXT),
    Column('star_id', INTEGER(11)),
    Column('mid', String(20)),
    Column('source_id', String(11)),
    Column('is_video', String(4)),
    Column('wbuser_id', String(11)),
    Column('type', String(11)),
    Column('pics_url', String(20)),
    Column('created_at', LONGTEXT),
    Column('source_info', CHAR(0)),
    Column('comment_source_info', CHAR(0)),
    Column('create_time', DATETIME(fsp=6), server_default=text("'0000-00-00 00:00:00.000000'"))
)


t_starinfos = Table(
    'starinfos', metadata,
    Column('id', INTEGER(11), server_default=text("'0'")),
    Column('channel', String(255)),
    Column('content', LONGTEXT),
    Column('ori_date', DATETIME(fsp=6), server_default=text("'0000-00-00 00:00:00.000000'")),
    Column('url', LONGTEXT),
    Column('pub_date', DATETIME(fsp=6)),
    Column('title', String(255)),
    Column('display_status', TINYINT(4), server_default=text("'0'")),
    Column('tag', String(255)),
    Column('star_tag', String(255)),
    Column('create_time', DATETIME(fsp=6), server_default=text("'0000-00-00 00:00:00.000000'")),
    Column('source', String(255)),
    Column('publisher', String(255)),
    Column('status', INTEGER(11), server_default=text("'0'")),
    Column('star_id', Text)
)


class Weibo(Base):
    __tablename__ = 'weibo'

    id = Column(INTEGER(11), primary_key=True)
    mid = Column(BIGINT(20), nullable=False)
    date = Column(DateTime, nullable=False)
    device = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    repost_count = Column(INTEGER(11))
    comment_count = Column(INTEGER(11))
    thumb_count = Column(INTEGER(11))
    interact_count = Column(INTEGER(11))
    content = Column(Text(collation='utf8mb4_unicode_ci'), nullable=False)
    uid = Column(BIGINT(20), nullable=False)
    username = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    follower_count = Column(INTEGER(11))
    statuses_count = Column(INTEGER(11))
    following_count = Column(INTEGER(11))
    sex = Column(String(255, 'utf8mb4_unicode_ci'))
    location = Column(String(255, 'utf8mb4_unicode_ci'))
    authentication = Column(TINYINT(1))
    auth_type = Column(String(255, 'utf8mb4_unicode_ci'))
    description = Column(Text(collation='utf8mb4_unicode_ci'))
    url = Column(Text(collation='utf8mb4_unicode_ci'))
    is_repost = Column(TINYINT(1), nullable=False)
    ori_author = Column(String(255, 'utf8mb4_unicode_ci'))
    ori_content = Column(Text(collation='utf8mb4_unicode_ci'))
    star = Column(INTEGER(11), nullable=False)


class WeiboStatu(Base):
    __tablename__ = 'weibo_status'

    id = Column(INTEGER(11), primary_key=True)
    desc = Column(String(255))
    status = Column(LONGTEXT)
    mid = Column(String(255), nullable=False)
    figure_id = Column(INTEGER(11))
    source_id = Column(String(255))
    text = Column(Text)
    user_id = Column(INTEGER(11))
    type = Column(INTEGER(2))
    media = Column(Text)
    is_video = Column(TINYINT(1))
    create_time = Column(DATETIME(fsp=6), nullable=False, default=datetime.datetime.now())
    created_at = Column(INTEGER(11), nullable=False)


class WeiboUser(Base):
    __tablename__ = 'weibo_user'

    id = Column(INTEGER(11), primary_key=True)
    weibo_id = Column(BIGINT(20), nullable=False)
    screen_name = Column(String(255), nullable=False)
    profile_img_url = Column(Text)
    verified = Column(TINYINT(1))
    description = Column(Text)
    create_time = Column(DATETIME(fsp=6), nullable=False, default=datetime.datetime.now())


t_weiboinfo_star_temp = Table(
    'weiboinfo_star_temp', metadata,
    Column('weiboinfo_id', INTEGER(11)),
    Column('star_id', Text)
)


class AuthPermission(Base):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        Index('auth_permission_content_type_id_codename_01ab375a_uniq', 'content_type_id', 'codename', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    content_type_id = Column(ForeignKey('django_content_type.id'), nullable=False)
    codename = Column(String(100), nullable=False)

    content_type = relationship('DjangoContentType')


class AuthUserGroup(Base):
    __tablename__ = 'auth_user_groups'
    __table_args__ = (
        Index('auth_user_groups_user_id_group_id_94350c0c_uniq', 'user_id', 'group_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False)
    group_id = Column(ForeignKey('auth_group.id'), nullable=False, index=True)

    group = relationship('AuthGroup')
    user = relationship('AuthUser')


class AuthtokenToken(Base):
    __tablename__ = 'authtoken_token'

    key = Column(String(40), primary_key=True)
    created = Column(DATETIME(fsp=6), nullable=False)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False, unique=True)

    user = relationship('AuthUser')


class DjangoAdminLog(Base):
    __tablename__ = 'django_admin_log'

    id = Column(INTEGER(11), primary_key=True)
    action_time = Column(DATETIME(fsp=6), nullable=False)
    object_id = Column(LONGTEXT)
    object_repr = Column(String(200), nullable=False)
    action_flag = Column(SMALLINT(5), nullable=False)
    change_message = Column(LONGTEXT, nullable=False)
    content_type_id = Column(ForeignKey('django_content_type.id'), index=True)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False, index=True)

    content_type = relationship('DjangoContentType')
    user = relationship('AuthUser')
class Cookies(Base):
    __tablename__ = 'cookie'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(200), nullable=False)
    password = Column(String(200), nullable=False)
    cookies = Column(LONGTEXT, nullable=False)
    create_time = Column(DATETIME(fsp=6), nullable=False, default=datetime.datetime.now())


class InformationsBlendinfoStar(Base):
    __tablename__ = 'informations_blendinfo_stars'
    __table_args__ = (
        Index('informations_blendinfo_stars_blendinfo_id_star_id_ad04a3d1_uniq', 'blendinfo_id', 'star_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    blendinfo_id = Column(ForeignKey('informations_blendinfo.id'), nullable=False)
    star_id = Column(ForeignKey('informations_star.id'), nullable=False, index=True)

    blendinfo = relationship('InformationsBlendinfo')
    star = relationship('InformationsStar')


class InformationsSdynamicsblend(Base):
    __tablename__ = 'informations_sdynamicsblend'

    id = Column(INTEGER(11), primary_key=True)
    text = Column(LONGTEXT)
    media_url = Column(LONGTEXT)
    pics_url = Column(LONGTEXT)
    platform = Column(LONGTEXT)
    created_at = Column(BIGINT(20))
    create_time = Column(DATETIME(fsp=6), nullable=False, default=datetime.datetime.now())
    star_id = Column(ForeignKey('informations_star.id'), index=True)

    star = relationship('InformationsStar')


class InformationsSdynamicswb(Base):
    __tablename__ = 'informations_sdynamicswb'

    id = Column(INTEGER(11), primary_key=True)
    desc = Column(String(255))
    text = Column(LONGTEXT)
    mid = Column(BIGINT(20))
    media_url = Column(LONGTEXT)
    is_video = Column(TINYINT(1), nullable=False)
    type = Column(INTEGER(11))
    created_at = Column(BIGINT(20))
    create_time = Column(DATETIME(fsp=6), nullable=False, default=datetime.datetime.now())
    source_id = Column(ForeignKey('informations_sdynamicswb.id'), index=True)
    star_id = Column(ForeignKey('informations_star.id'), index=True)
    wbuser_id = Column(ForeignKey('informations_wbuser.id'), index=True)

    source = relationship('InformationsSdynamicswb', remote_side=[id])
    star = relationship('InformationsStar')
    wbuser = relationship('InformationsWbuser')


class InformationsWeiboinfoStar(Base):
    __tablename__ = 'informations_weiboinfo_stars'
    __table_args__ = (
        Index('informations_weiboinfo_stars_weiboinfo_id_star_id_38108b65_uniq', 'weiboinfo_id', 'star_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    weiboinfo_id = Column(ForeignKey('informations_weiboinfo.id'), nullable=False)
    star_id = Column(ForeignKey('informations_star.id'), nullable=False, index=True)

    star = relationship('InformationsStar')
    weiboinfo = relationship('InformationsWeiboinfo')


class AuthGroupPermission(Base):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        Index('auth_group_permissions_group_id_permission_id_0cd325b0_uniq', 'group_id', 'permission_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    group_id = Column(ForeignKey('auth_group.id'), nullable=False)
    permission_id = Column(ForeignKey('auth_permission.id'), nullable=False, index=True)

    group = relationship('AuthGroup')
    permission = relationship('AuthPermission')


class AuthUserUserPermission(Base):
    __tablename__ = 'auth_user_user_permissions'
    __table_args__ = (
        Index('auth_user_user_permissions_user_id_permission_id_14a6b632_uniq', 'user_id', 'permission_id', unique=True),
    )

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False)
    permission_id = Column(ForeignKey('auth_permission.id'), nullable=False, index=True)

    permission = relationship('AuthPermission')
    user = relationship('AuthUser')


class DynamicImage(Base):
    __tablename__ = 'dynamic_image'

    id = Column(INTEGER(11), primary_key=True)
    mid = Column(BIGINT(20))
    thumbnail_height = Column(INTEGER(11))
    thumbnail_width = Column(INTEGER(11))
    large_height = Column(INTEGER(11))
    large_width = Column(INTEGER(11))
    thumbnail_url = Column(Text)
    large_url = Column(Text)
    create_time = Column(DATETIME(fsp=6), nullable=False, default=datetime.datetime.now())


def init_db():
    print('initialize database, drops and creates tables')
    Base.metadata.create_all(engine)


# if not engine.dialect.has_table(engine, 'weibo_status'):
#init_db()
