import logging
from zcSpider.items import MatchDataItem
from zcSpider.items import OuOddsItem
from zcSpider.items import YaOddsItem
from zcSpider.items import YaOddsDetailItem
from zcSpider.items import SizeOddsItem
from zcSpider.items import SizeOddsDetailItem
from .Sql import Sql

class MatchDataPipeline(object):
    def process_match_item(self, item):
        try:
            #获取主队编号
            mmid = Sql.select_name('b_team', item['mmTeam'])
            if (mmid == 0):
                if Sql.addTeamItem(item['mmTeam'], '', ''):
                    mmid = Sql.select_name('b_team', item['mmTeam'])

            #获取客队球队编号
            mdid = Sql.select_name('b_team', item['mdTeam'])
            if (mdid == 0):
                if Sql.addTeamItem(item['mdTeam'], '', ''):
                    mdid = Sql.select_name('b_team', item['mdTeam'])

            #获取联赛编号
            mlsid = Sql.select_name('b_lmatch', item['mlsName'])
            if (mlsid == 0):
                if Sql.addlmMatchItem(item['mlsName'], '', ''):
                    mlsid = Sql.select_name('b_lmatch', item['mlsName'])

            #判断当前比赛是否已经记录
            mbId = Sql.getMatchId(item['mid'])
            if (mbId == 0):
                item['mmTeamId'] = mmid
                item['mdTeamId'] = mdid
                item['mlsId'] = mlsid
                Sql.addMatchItem(item)

        except Exception as e:
            logging.error('MatchDataPipeline Error: {}'.format(e))



    def process_ouodds_item(self, item):
        try:
            if isinstance(item, OuOddsItem):
                #判断当前比赛是否已经记录
                mbId = Sql.getMatchId(item['mid'])
                if (mbId > 0):
                    # 获取博彩公司编号
                    #item['mlyName'] = 'Interwetten'
                    mlyid = Sql.select_name('b_lottery', item['mlyName'])
                    if (mlyid == 0):
                        if Sql.addLotteryItem(item['mlyName'], '', ''):
                            mlyid = Sql.select_name('b_lottery', item['mlyName'])
                    item['mlyId'] = mlyid
                    ooid = Sql.getOuOddsId(item['mid'], mlyid)
                    if (ooid == 0) and (mlyid > 0):
                        Sql.addOuOddsItem(item)

        except Exception as e:
            logging.error('OuOddsDataPipeline Error: {}'.format(e))

    def process_yaodds_item(self, item):
        try:
            #判断当前比赛是否已经记录
            mbId = Sql.getMatchId(item['mid'])
            if (mbId > 0):
                # 获取博彩公司编号
                mlyid = Sql.select_name('b_lottery', item['mlyName'])
                if (mlyid == 0):
                    if Sql.addLotteryItem(item['mlyName'], '', ''):
                        mlyid = Sql.select_name('b_lottery', item['mlyName'])
                item['mlyId'] = mlyid
                ooid = Sql.getYaOddsId(item['mid'], mlyid)
                if (ooid == 0) and (mlyid > 0):
                    Sql.addYaOddsItem(item)
        except Exception as e:
            logging.error('YaOddsDataPipeline Error: {}'.format(e))

    def process_yaoddsdetail_item(self, item):
        try:
            # 获取博彩公司编号
            mlyid = Sql.select_name('b_lottery', item['mlyName'])
            # 获取亚赔ID
            myoid = Sql.getYaOddsId(item['mid'], mlyid)
            # 判断明细是否已经存在
            mdid = Sql.getYaDetailId(myoid, item['mDisc'])
            if (mdid == 0) and (myoid > 0):
                item['myoid'] = myoid
                Sql.addYaDetailItem(item)
        except Exception as e:
            logging.error('YaOddsDetailDataPipeline Error: {}'.format(e))

    def process_sizeodds_item(self, item):
        try:
            #判断当前比赛是否已经记录
            mbId = Sql.getMatchId(item['mid'])
            if (mbId > 0):
                # 获取博彩公司编号
                mlyid = Sql.select_name('b_lottery', item['mlyName'])
                if (mlyid == 0):
                    if Sql.addLotteryItem(item['mlyName'], '', ''):
                        mlyid = Sql.select_name('b_lottery', item['mlyName'])
                item['mlyId'] = mlyid
                ooid = Sql.getSizeOddsId(item['mid'], mlyid)
                if (ooid == 0) and (mlyid > 0):
                    Sql.addSizeOddsItem(item)
        except Exception as e:
            logging.error('SizeOddsDataPipeline Error: {}'.format(e))

    def process_sizeoddsdetail_item(self, item):
        try:
            # 获取博彩公司编号
            mlyid = Sql.select_name('b_lottery', item['mlyName'])
            # 获取亚赔ID
            myoid = Sql.getSizeOddsId(item['mid'], mlyid)
            # 判断明细是否已经存在
            mdid = Sql.getSizeDetailId(myoid, item['mDisc'])
            if (mdid == 0) and (myoid > 0):
                item['msoid'] = myoid
                Sql.addSizeDetailItem(item)
        except Exception as e:
            logging.error('SizeOddsDetailDataPipeline Error: {}'.format(e))

    def process_item(self, item, spider):
        # print(item)
        if isinstance(item, MatchDataItem):
            self.process_match_item(item)
        elif isinstance(item, OuOddsItem):
            self.process_ouodds_item(item)
        elif isinstance(item, YaOddsItem):
            self.process_yaodds_item(item)
        elif isinstance(item, YaOddsDetailItem):
            self.process_yaoddsdetail_item(item)
        elif isinstance(item, SizeOddsItem):
            self.process_sizeodds_item(item)
        elif isinstance(item, SizeOddsDetailItem):
            self.process_sizeoddsdetail_item(item)
