import logging


#设置日志的输出样式：
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
               )

logger = logging.getLogger(__name__)


if __name__ == '__main__':
	logging.debug("this is a debug log")
	logging.debug("this is a debug log1")