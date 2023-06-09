# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import json
import time
import pandas as pd
from loguru import logger
from comm.nb import Query


class NewBingCrawler:
    ThrottledFlag = 'ThrottledCodeExpt'
    throttled_words = ['Throttled: Request is throttled.']

    @classmethod
    def search(cls, question, style: str = 'precise', word_num=4000):
        # 或者balanced| precise| creative
        if len(question) > word_num:
            logger.warning(f'question word num more over than {word_num}！！！')
            return {
                'answer': f'question word num more over than {word_num}！！！',
                'suggestions': [],
                'searching_words': [],
            }

        start_time = time.time()
        try:
            answer = Query(
                prompt=question,
                style=style,
                cookie_file=0
            )
            suggest = []
            logger.info(f'using style: {style}')
            logger.info(f'A: {answer.output}')
            logger.info(f'use time: {time.time() - start_time} s')
            logger.info(f'search_words: {answer.sources_dict}')

            try:
                suggest = answer.suggestions
            except Exception as e:
                logger.error(f'no suggest response :{e}')
            logger.info(f'suggestions: {suggest}')

        except Exception as e:
            logger.error(e)
            tmp_ans = cls.ThrottledFlag if str(e) in cls.throttled_words else ''
            return {
                'answer': tmp_ans,
                'suggestions': [],
                'searching_words': [],
            }

        return {
            'answer': answer.output,
            'suggestions': suggest,
            'searching_words': list(set([sw['searchQuery'] for sw in answer.sources])),
        }

    @classmethod
    def search_from_prompt_json(cls, prompt_path, style='precise'):
        is_finished, item_bp = BreakpointHandler.load()
        if is_finished:
            logger.success('finished getting all answer!')
            return
        prompt_data = FileUtils.load_json(prompt_path)
        for idx, item in enumerate(prompt_data):
            if idx < item_bp or item['A']: continue
            question = item['Q']

            try:
                logger.debug(f'====={idx}=====')
                logger.debug(f'querying in : {question}')
                res = NewBingCrawler.search(question=question, style=style)
                if res['answer'] == cls.ThrottledFlag:
                    logger.warning('Account usage limit exceeded!/账号次数超限！')
                    BreakpointHandler.save_breakpoint(idx, question)
                    exit(0)
                prompt_data[idx]['A'] = res['answer']
                prompt_data[idx]['suggestions'] = res['suggestions']
                prompt_data[idx]['searching_words'] = res['searching_words']

                FileUtils.write2json(prompt_path, prompt_data)
            except Exception as e:
                logger.error(e)
                BreakpointHandler.save_breakpoint(idx, question)
                return
            except:
                BreakpointHandler.save_breakpoint(idx, question)
                return
        BreakpointHandler.finish()


class FileUtils:
    @staticmethod
    def write2json(json_path: str, data):
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))
        logger.info(f'write json to: {json_path}')

    @staticmethod
    def load_json(json_path: str):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
        return data

    @staticmethod
    def exl2json(exl_path, json_path, col_name=''):
        # json_data = FileUtils.load_json(json_path)
        # if json_data:
        #     return
        json_data = []
        prompt = pd.read_excel(exl_path, engine='openpyxl')
        question = prompt[col_name] if col_name else prompt.iloc[:, 0]
        for q in question:
            json_data.append({
                'Q': q,
                'A': ''
            })
        FileUtils.write2json(json_path, json_data)

    @staticmethod
    def json2exl(json_path: str, exl_path: str):
        df_json = pd.read_json(json_path)
        df_json.to_excel(exl_path, sheet_name="response",
                         columns=["A", "suggestions", "searching_words"],
                         index=False)


class Logger:
    @staticmethod
    def init_logger(logger_path, filter_word='', level='WARNING'):
        logger.add(logger_path, rotation='10 MB',
                   level=level, filter=lambda x: filter_word in x['message'],
                   encoding="utf-8", enqueue=True, retention="30 days")
        logger.info(f'logger file load in: {logger_path}')
        return logger


class BreakpointHandler:
    conf_path = './conf/conf.json'
    cfg = FileUtils.load_json(conf_path)

    @classmethod
    def save_breakpoint(cls, item_idx, question):
        logger.warning(f'breakpoint in idx {item_idx}')
        cls.cfg = FileUtils.load_json(cls.conf_path)
        cls.cfg['breakpoint']['item_bp'] = item_idx
        cls.cfg['breakpoint']['question'] = question
        FileUtils.write2json(cls.conf_path, cls.cfg)

    @classmethod
    def finish(cls):
        cls.cfg['breakpoint']['is_finished'] = True
        FileUtils.write2json(cls.conf_path, cls.cfg)

    @classmethod
    def load(cls):
        is_finished = cls.cfg['breakpoint']['is_finished']
        item_bp = cls.cfg['breakpoint']['item_bp']
        return is_finished, item_bp
