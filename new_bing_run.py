# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

from comm.utils import *

if __name__ == '__main__':
    cfg_data = FileUtils.load_json('./conf/conf.json')
    logger = Logger.init_logger(
        logger_path=cfg_data['path']['log'],
        level='INFO'
    )

    FileUtils.exl2json(cfg_data['path']['prompt'],
                       cfg_data['path']['answer'],
                       'Q')
    NewBingCrawler.search_from_prompt_json(prompt_path=cfg_data['path']['answer'])
