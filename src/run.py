#!/usr/bin/env python3

import logging
import os
from angryduck.client import AngryDuckClient


def get_logger():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger


if __name__ == '__main__':
    logger = get_logger()
    token = os.getenv('DISCORD_TOKEN')

    client = AngryDuckClient(logger)
    client.run(token)
