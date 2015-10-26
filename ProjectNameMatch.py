# -*-coding:utf-8-*-
import re


"""
分析文件列表是否为序列文件
测试代码:
str01 = 'XFTL_020_006b_039_CHcolor_lr_c001_CH_Col.1001.iff'
aa = ProjectNameMatch()
aa.fileName = str01
aa.setFileName(str01)
aa.getPorjName()
aa.getResults()
aa.getResults('version_number')
dict1 = {'episode_number': 'a01_', 'session_number': 'a02_', 'project_name': 'a01_', 'scene_describe': 'a04_', 'process_name': 'a05_', 'scene_number': 'a03_', 'version_number': 'a06_'}
aa.setPrefix(custom=dict1)
aa.getProjDirectorys()
aa.getUploadServerPath()
aa.getUploadServerPath(mod='Mov')
"""


class ProjectNameMatch(object):
    """检查文件名称是否符合预设的项目规则"""
    def __init__(self):
        super(ProjectNameMatch, self).__init__()
        self.fileName = ''                                            # 文件名称
        self.projDrive = 'E:/maya/'                             # 项目预设的本地工程文件夹位置
        self._results = {}                                            # 将匹配的结果以字典的形式存放在该变量内
        self._nResults = {}                                        # 纯净版的匹配结果(根据前缀规则去掉前缀内容)
        self._pResults = {}                                        # 在纯净版的基础上加上前缀,(注,路径输出或者其它结果输出都将用此版本,默认为原始匹配结果)
        self._projectName = ''                                   # 项目名称

        #将项目名称分割成项目的基础信息,例如项目名称,集数,场次,镜头号,镜头描述(可选),环节名称,版本号(可选)
        self._keys = [
            ('project_name', 'episode_number', 'session_number', 'scene_number', 'scene_describe', 'process_name', 'version_number')
        ]

        #项目可能出现的环节名称,例如mo(模型),rg(绑定)等等
        links = [
            '|'.join(['mo', 'rg', 'tx', 'ms', 'ly', 'an', 'dy', 'ef', 'lr', 'cp', 'MO', 'RG', 'TX', 'MS', 'LY', 'AN', 'DY', 'EF', 'LR', 'CP'])
        ]
        #正则的匹配规则,必须和key值进行对应,key值只是为了将规则进行归类,方便后面的组合
        #因为项目会不断的增加,以及每个项目的存在多种匹配模式的存在
        rules = {
            'XFTL':
                    [
                        ['XF', '(?!999|000)[0-9]+', '(sq){0,1}[0-9]+[a-zA-Z]{0,2}', '(sc){0,1}[0-9]+[a-zA-Z]{0,2}', '\\w+', links[0], '(c){0,1}[0-9]+'],
                        ['XFTL', '(?!999|000)[0-9]+', '(sq){0,1}[0-9]+[a-zA-Z]{0,2}', '(sc){0,1}[0-9]+[a-zA-Z]{0,2}', '\\w+', links[0], '(c){0,1}[0-9]+'],
                        ['XFTL', '999|000', '[a-zA-Z]+[0-9]{0,2}', '(sc){0,1}[0-9]+[a-zA-Z]{0,2}', '\\w+', links[0], '(c){0,1}[0-9]+']
                    ],
            'SENBA':
                    [
                        ['SB|SENBA', '(?!999|000)[0-9]+', '(sq){0,1}[0-9]+[a-zA-Z]{0,2}', '(sc){0,1}[0-9]+[a-zA-Z]{0,2}', '\\w+', links[0], '(c){0,1}[0-9]+'],
                        ['SB|SENBA', '999|000', '[a-zA-Z]+[0-9]{0,2}', '(sc){0,1}[0-9]+[a-zA-Z]{0,2}', '\\w+', links[0], '(c){0,1}[0-9]+']
                    ]
        }

        #组合模式,将项目的key和对应的正则rules进行对应的组合
        #"_"为分割连接符号,"{0,1}"为该字段为可选
        groups = [
            ''.join(['(?P<%s>%s)', '(?P<%s>%s)', '(_(?P<%s>%s))', '(_(?P<%s>%s))', '(_(?P<%s>%s)){0,1}', '(_(?P<%s>%s))', '(_(?P<%s>%s)){0,1}']),
            ''.join(['(?P<%s>%s)', '(_(?P<%s>%s))', '(_(?P<%s>%s))', '(_(?P<%s>%s))', '(_(?P<%s>%s)){0,1}', '(_(?P<%s>%s))', '(_(?P<%s>%s)){0,1}'])
        ]

        # 将和key的值和对应的正则匹配规则以及对应的组合模式进行组合
        # 注:项目名称的匹配将会以下列字典的Key为主,而非以匹配规则的结果为主,
        # 因为有部分文件名称将会采用简写,例如项目名"XFTL",而文件名可以用"XF"简称开头
        self._matchsDict = {
            'XFTL':
                [
                    groups[0] % self._crossMerger(self._keys[0], rules['XFTL'][0]),
                    groups[1] % self._crossMerger(self._keys[0], rules['XFTL'][1]),
                    groups[1] % self._crossMerger(self._keys[0], rules['XFTL'][2])
                ],
            'SENBA':
                [
                    groups[1] % self._crossMerger(self._keys[0], rules['SENBA'][0]),
                    groups[1] % self._crossMerger(self._keys[0], rules['SENBA'][1])
                ]
        }

        self._prefixDict = {
            'XFTL': {
                self._keys[0][1]: [('ep_{0,1}', 'episode_{0,1}'), ('ep', 'episode_', 'ep_')],
                self._keys[0][2]: [('sq_{0,1}', 'sequence_{0,1}'), ('sq', 'sequence_', 'sq_')],
                self._keys[0][3]: [('sc_{0,1}', 'scene_{0,1}'), ('sc', 'scene_', 'sc_')]
            },
            'SENBA': {
                self._keys[0][1]: [('ep_{0,1}', 'episode_{0,1}'), ('ep', 'episode_', 'ep_')],
                self._keys[0][2]: [('sq_{0,1}', 'sequence_{0,1}'), ('sq', 'sequence_', 'sq_')],
                self._keys[0][3]: [('sc_{0,1}', 'scene_{0,1}'), ('sc', 'scene_', 'sc_')]
            }
        }

        # 这是根据文件名称提取相关信息在本地生成一个maya工程目录
        # 生成的方式完全按照maya创建工程目录的方式进行输出
        # 第一个字符串为工程名称,第二个数组为本地路径的组成元素
        # 注意,本地路径的生成将统一用self.projDrive/self._projectName/self._keys[1]/self._keys[1]这种模式进行连接
        self._localPathDict = {
            'XFTL': [self._keys[0][3], (self._keys[0][1], self._keys[0][2])],
            'SENBA': [self._keys[0][3], (self._keys[0][1], self._keys[0][2])]
        }

        # 服务器路径采用奇偶数分流规则,集数为偶数则放在EVEN文件夹内,奇数则放在ODD文件夹内
        # 考虑到不同项目奇偶分流的关键字段可能不一样,因此将关键字采用字典的key留作扩展
        parityList = [
            {self._keys[0][1]:['EVEN/', 'ODD/']}
        ]

        # 将文件部分关键字的内容作为服务器部分路径
        # 考虑到不同项目会有不同的关键字,因此用列表形式,方便扩展
        localPathList = [
            [self._keys[0][1], self._keys[0][2], self._keys[0][3]]
        ]

        # 服务器路径采用奇偶数分流规则,集数为偶数则放在EVEN文件夹内,奇数则放在ODD文件夹内
        self._serverPathDict = {
            'XFTL': {
                'Images': ['//kaixuan.com/kx/Proj/Priject/xuanfengtuoluo/Production/Render/Images/', parityList[0], localPathList[0]],
                'Mov': ['//kaixuan.com/kx/Proj/Priject/xuanfengtuoluo/Production/Render/Mov/', parityList[0], localPathList[0]]
            },
            'SENBA': {
                'Images': ['//kaixuan.com/kx/Proj/SENBA/Production/Render/Images/', parityList[0], localPathList[0]],
                'Mov': ['//kaixuan.com/kx/Proj/SENBA/Production/Render/Mov/', parityList[0], localPathList[0]]
            }
        }

    def _crossMerger(self, projKeys=(), rules=[]):
        return tuple([x for y in zip(projKeys, rules) for x in y])

    def _matchString(self, rule='', str1=''):
        """判断字符串匹配规则和字符是否完全匹配"""
        matching = 0
        m = re.match(rule, str1)
        if m and m.group(0) == str1:
            matching = 1
        return matching

    def _setNResults(self):
        """根据项目规则匹配的结果,得到纯净版的匹配结果(根据前缀规则去掉前缀内容)"""
        nResults = self._results.copy()
        prefixDict = self._prefixDict[self._projectName]
        for key in prefixDict:
            for rules in prefixDict[key][0]:
                m = re.match(rules, nResults[key])
                if m:
                    nResults[key] = nResults[key].replace(m.group(0), '', 1)
                    break
        self._nResults = nResults

    def _setPresetPrefix(self, mod=0):
        """获取预设的前缀设置,目前只预设了3种,因此数字只能是0-2"""
        nResults = self._nResults.copy()
        prefixDict = self._prefixDict[self._projectName]
        for key in prefixDict:
            nResults[key] = prefixDict[key][1][mod] + nResults[key]
        self._pResults = nResults
        return nResults

    def _getKeysValue(self, keys=[]):
        """根据keys列表返回key的内容"""
        results = self._pResults
        return [results[key] for key in keys]

    def _getServerParity(self, parityDict={}):
        """根据项目的奇偶字典预设,返回服务器上的奇偶分流路径"""
        results = self._pResults
        parity = ''
        for key in parityDict:
            numStr = ''.join(re.findall('[0-9]', results[key]))
            num = int(numStr) % 2
            parity = parityDict[key][num]
        return parity

    def setPrefix(self, mod=1, custom={}):
        """
        设置前缀
        mod = -1, 原始匹配结果
        mod = 0,无前缀
        mod = 1,预设1前缀(默认值)
        mod = 2,预设2前缀
        mod = 3,预设3前缀
        custom为自定义前缀,类型为字典类型(优先级最高,将无视mod的值)
        key的值必须和匹配结果的key值保持一致
        """
        results = self._results.copy()
        nResults = self._nResults.copy()
        pResults = {}
        if custom:
            for key in custom:
                if nResults[key]:
                    nResults[key] = custom[key] + nResults[key]
            self._pResults = nResults
            return nResults
        if mod > 0:
            pResults = self._setPresetPrefix(mod=mod-1)
        else:
            if mod:
                pResults = results
            else:
                pResults = nResults
        self._pResults = pResults
        return pResults

    def setFileName(self, fileName=''):
        """设置当前maya的文件名称"""
        #if not fileName:
            #fileName = cmds.file(query=True, sceneName=True, shortName=True)
        self.fileName = fileName
        matching = self.matchProjName()
        self._pResults = self._results.copy()
        if not matching:
            self.fileName = ''
        return matching

    def setProjDrive(self, projDrive='E:/maya/'):
        """设置要另存的maya工程目录盘符"""
        self.projDrive = projDrive

    def matchProjName(self):
        """检查文件名称是否符合预设的项目规则"""
        matchsDict = self._matchsDict
        fileName = self.fileName
        matching = 0
        for key in matchsDict:
            for rule1 in matchsDict[key]:
                m = re.match(rule1, fileName)
                if m:
                    self._results = m.groupdict().copy()
                    self._projectName = key
                    self._setNResults()
                    matching = 1
                    break
            if matching:
                break
        if not matching:
            print u'文件名称命名不规范!'
        return matching

    def getPorjName(self):
        projName = self._projectName
        if not projName:
            self.matchProjName()
            projName = self._projectName
        return projName

    def getResults(self, key=''):
        results = self._results
        if not results:
            self.matchProjName()
            results = self._results
        if key and key in results:
            return results[key]
        return results

    def getProjDirectorys(self, link='/'):
        """根据项目文件名称自动生成本地的工程名称和工程路径"""
        project = self._projectName
        key = self._localPathDict[project][0]
        keys = self._localPathDict[project][1]
        values = self._getKeysValue(keys)
        projectName = self._pResults[key]
        projectPath = self.projDrive + project + link
        projectPath = projectPath + link.join(values) + link
        return [projectName, projectPath]

    def getUploadServerPath(self, mod='Images', link='/'):
        """
        根据项目文件名称获取上传服务器的路径
        mod = Images为素材上传地址(默认值)
        mod = Mov 为mov视频上传地址
        目前只预设了这2种
        """
        serverPath = ''
        project = self._projectName
        valueList = self._serverPathDict[project][mod]
        parity = self._getServerParity(valueList[1])
        values = self._getKeysValue(valueList[2])
        serverPath = valueList[0] + parity + link.join(values) + link
        return serverPath

if __name__ == "__main__":
    str01 = 'XFTL_020_006b_039_CHcolor_lr_c001_CH_Col.1001.iff'
    aa = ProjectNameMatch()    
    aa.fileName = str01
    aa.setFileName(str01)
    aa.getPorjName()
    aa.getResults()
    aa.getResults('version_number')
    dict1 = {'episode_number': 'a01_', 'session_number': 'a02_', 'project_name': 'a01_', 'scene_describe': 'a04_', 'process_name': 'a05_', 'scene_number': 'a03_', 'version_number': 'a06_'}
    aa.setPrefix(custom=dict1)
    aa.getProjDirectorys()
    aa.getUploadServerPath()
    aa.getUploadServerPath(mod='Mov')
    print aa.getResults()