import random
import sys
import traceback

import structlog


def main(argv):
    logger = structlog.get_logger()
    for i in range(1,20):
        msg = {}  # note - structured data, not a string concatenated on the fly

        # generate some fake data
        session_id = random.randint(0,99)

        msg['session_id'] = session_id
        msg['loop_iteration'] = i

        if i % 15 == 0:
            try:
                raise Exception('Bad runtime example')
            except Exception as e:
                msg['user_experience'] = "\uD83E\uDD2C"
                logger.error("Wake me up at night\n{}".format(traceback.format_exc()))
        elif i % 5 == 0:
            logger.warn("Investigate tomorrow")
        elif i % 3 == 0:
            logger.info("Collect in production")
        else:
            logger.debug("Collect in development")


if __name__ == '__main__':
    main(sys.argv)
