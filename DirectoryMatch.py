#coding:utf-8
'''
Created on 2015年10月12日 下午2:53:44

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''
import os
import time
import glob
import re
import collections

import SequenceFileDetection as sfd
import ProjectNameMatch as pnm
    
class DirFactory(object):
    
    def __init__(self, dir):
        self.__dir = dir
        self.__filesDic = dict()
        self.__versionDic = dict()
        self.__outDic = dict()
        
        
    # def getFiles(dir, filesDic = {}, tree = True):
    #     for child in glob.glob(dir + os.sep + '*'):
    #         if tree :
    #             if os.path.isdir(child):
    #                 getFiles(child)
    #             else :
    #                 filesDic.setdefault(dir, list()).append(os.path.basename(child))
    #         else :
    #             filesDic.setdefault(dir, list()).append(os.path.basename(child))
    #     return filesDic
    
    def getFiles(self):
        pm = pnm.ProjectNameMatch()
        for root, dirnames, filenames in os.walk(self.__dir):
            for filename in filenames:
                pm.setFileName(filename)
                if pm.matchProjName() :
                    self.__filesDic.setdefault(root, list()).append(os.path.basename(filename))
                else :
                    pass
        return self.__filesDic
                
                
    def versionMatch(self):
        pathLst = self.__filesDic.keys()
        pm = pnm.ProjectNameMatch()
        for d in pathLst:
            pm.setFileName(self.__filesDic[d][0])
            res = pm.getResults()
            if res['scene_describe'] :
                lst = [res['project_name'], res['episode_number'], res['session_number'], res['scene_number'], res['scene_describe'], res['process_name']]
            else:
                lst = [res['project_name'], res['episode_number'], res['session_number'], res['scene_number'], res['process_name']]
            name = '_'.join(lst)
            ver = re.search("\Ac\d+", os.path.basename(d))
            if ver:
                version = ver.group()
            else :
                version = 'c001'
            self.__versionDic.setdefault(name, dict()).setdefault(version, d)
        return self.__versionDic
        
    def output(self):
        pm = pnm.ProjectNameMatch()
        for key, value in self.__versionDic.items():
            pm.setFileName(key)
            res = pm.getResults()
            key_lst = [res['project_name'], res['episode_number'], res['session_number'], res['scene_number'], res['process_name']]
            name_key = '_'.join(key_lst)    #定义名称key变量
            if res['scene_describe']:
                layer_key = res['scene_describe']
            else :
                layer_key = 'convert'       #定义分层key变量
            outname_value = name_key        #定义输出名称变量
            version_value = value.keys()    #定义版本号变量
            outpath_value = []              #定义输出路径变量
            startf_value = []               #定义起始帧变量
            endf_value = []                 #定义结束帧变量
            ctime_value = []                #定义创建时间变量
            for v in version_value:
                f = self.__filesDic[value[v]]
                outpath_value.append(pm.getUploadServerPath())
                frameRange = self.getFrameRange(f)
                for key in frameRange.keys():
                    if key != "separateFiles" :
                        startf_value.append(frameRange[key][0])
                        endf_value.append(frameRange[key][1])
                        ctime_value.append(time.ctime(self.getCtime(value[v])))
        
            self.__outDic.setdefault(name_key, dict()).setdefault(layer_key, [outname_value, startf_value, endf_value, outpath_value, version_value, ctime_value])
        return self.__outDic
    
#     def getOutPath(self, source):
#         pm = pnm.ProjectNameMatch()
#         pm.getUploadServerPath()
#         return source
    
    def getFrameRange(self, source):
        fileSequence = sfd.SequenceFileDetection()
        fileSequence.setSequenceFiles(source)
        return fileSequence.getSequenceInfo()     
    
    def getCtime(self, source):
        return os.path.getctime(source)
    
if __name__ == "__main__":
    #dm = "E:\\maya\\SENBA\\037\\sc003"
    #dm = "Z:\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep019\\sq004a\\sc020"\
    dm = "Z:\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep019"
    start1 = time.time()
    print "start", time.ctime(start1)
    df = DirFactory(dm)
    files = df.getFiles()
    mid1 = time.time()
    print "mid1", time.ctime(mid1)
    print mid1 - start1
    print files
    versionDic = df.versionMatch()
    mid2 = time.time()
    print "mid2", time.ctime(mid2)
    print mid2 - mid1 
    print versionDic
    outDic = df.output()
    mid3 = time.time()
    print "mid3", time.ctime(mid3)
    print mid3 - mid2
    print outDic