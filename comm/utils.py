# !/usr/bin/env python3
# _*_ coding: utf-8 _*_
import json
import time
import asyncio
import pandas as pd
from loguru import logger
from EdgeGPT import Chatbot, ConversationStyle


class NewBingCrawler:
    cookies_path = './conf/cookies.json'

    @classmethod
    def search(cls, question, word_num=2000):
        if len(question) > word_num:
            logger.warning(f'question word num more over than {word_num}！！！')
            return ''

        async def crawl(style='precise'):
            bot = Chatbot(cookie_path=cls.cookies_path)
            if style == 'balanced':
                res_dict = (await bot.ask(prompt=question,
                                          conversation_style=ConversationStyle.balanced))
            else:
                # res_dict = FileUtils.load_json('./data/answer/rsp.json')
                res_dict = (await bot.ask(prompt=question,
                                          conversation_style=ConversationStyle.precise))
            await bot.close()
            logger.info(f'using {style} to search')
            msg = None
            try:
                msg = res_dict['item']['messages']
            except:
                logger.warning('很抱歉，你已达到可在 24 小时内发送到必应的邮件限制。请稍后回来查看!')
                exit(0)
            flag, suggestion_list, searching_list = True, [], []
            if 'text' not in msg[1].keys():
                answer = msg[1]['spokenText']
                flag = False
            else:
                answer = msg[1]['text']
                suggestions = msg[1]['suggestedResponses']
                suggestion_list = list(set(suggestion['text'] for suggestion in suggestions))
                source_attributions = msg[1]['sourceAttributions']
                searching_list = list(set(item['searchQuery'] for item in source_attributions))

            # print(json.dumps(res_dict, ensure_ascii=False, indent=4))
            return flag, answer, suggestion_list, searching_list

        start_time = time.time()
        try:
            _, res, sg, sw = asyncio.run(crawl())
            # 优先精确模式，无结果则选平衡模式
            if not _:
                _, res, sg, sw = asyncio.run(crawl('balanced'))
            end_time = time.time()
            logger.info(f'use time====>: {end_time - start_time}s')
            logger.info(f'Q: {question}')
            logger.info(f'A: {res}\n')
            logger.info(f'Suggestions: {sg}\n')
        except Exception as e:
            logger.error(e)
            return
        return {
            'answer': res,
            'suggestions': sg,
            'searching_words': sw
        }

    @classmethod
    def search_from_prompt_json(cls, prompt_path):
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
                res = NewBingCrawler.search(question)
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
    def write2json(json_path: str, data: dict):
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
