# -*-coding:utf-8-*-
import difflib
import re


"""
分析文件列表是否为序列文件
测试代码:
filesList = ['aaa.1001.png', 'aaa.1002.png', 'aaa.1003.png', 'aaa.1004.png', 'aaa.1005.png', 'aaa.1006.png', 'aaa.1007.png', 'aaa.1008.png', 'aaa.1009.png']
fileSequence = SequenceFileDetection()
fileSequence.setSequenceFiles(filesList)
fileSequence.getSequenceInfo()
"""


class SequenceFileDetection(object):
    """
    分析文件列表是否为序列文件
    """
    def __init__(self):
        super(SequenceFileDetection, self).__init__()
        # mode=0返回完整的数字序列
        # 适合渲染图片进行查询匹配使用
        self.sequenceDict1 = {}
        # mode=1返回不同部分的数字序列
        # 适合部分将序列贴图转换成视频格式插件使用
        self.sequenceDict2 = {}

        self.separateFiles = []               # 非序列的文件列表
        self.startFrame = -1                      # 设置起始帧
        self.endFrame = 0                       # 设置结束帧

    def _getFrontNumStr(self, str1=''):
        """获取字符串前端属于数字的字符"""
        numStr = ''
        current = 0
        while(str1):
            if str1[current].isdigit():
                numStr += str1[current]
                str1 = str1[1:]
            else:
                break
        return numStr

    def _getEndNumStr(self, str1=''):
        """获取字符串末尾属于数字的字符"""
        numStr = ''
        current = -1
        while(str1):
            if str1[current].isdigit():
                numStr = str1[current] + numStr
                str1 = str1[:-1]
            else:
                break
        return numStr

    def _sequenceSortKey(self, str1='', length=255):
        """
        序列文件列表排序的Key模块
        length为字符长度,一般windows文件名最长为255
        """
        strNum = ''.join(re.findall(r'\d', str1))
        str1 = ''.join(re.findall(r'\D', str1)) + strNum.zfill(length)
        return str1

    def _filesCompare(self, file1='', file2=''):
        """分析两个文件是否形成序列文件"""
        filesDict = []
        a = file1
        b = file2
        seq = difflib.SequenceMatcher(lambda x: x.isdigit(), a, b)
        k = 1
        switch = 0
        i3 = 0
        i4 = 0
        j3 = 0
        j4 = 0
        for tag, i1, i2, j1, j2 in seq.get_opcodes():
            if tag == 'replace':
                if 0 == k or 0 == i1 or 0 == j1 or not (a[i1:i2].isdigit() and b[j1:j2].isdigit()):
                    switch = 0
                    break
                switch = 1
                k -= 1
                i3 = i1
                i4 = i2
                j3 = j1
                j4 = j2

            if tag == 'delete':
                if 0 == k or i1 < 2 or not (a[i1:i2].isdigit() and a[i1-1:i1].isdigit()):
                    switch = 0
                    break
                switch = 1
                k -= 1
                i3 = i1-1
                i4 = i2
                j3 = j1-1
                j4 = j2

            if tag == 'insert':
                if 0 == k or j1 < 2 or not (b[j1:j2].isdigit() and b[j1-1:j1].isdigit()):
                    switch = 0
                    break
                switch = 1
                k -= 1
                i3 = i1-1
                i4 = i2
                j3 = j1-1
                j4 = j2

        if switch:
            i1 = i3
            i2 = i4
            j1 = j3
            j2 = j4
            temp = self._getEndNumStr(a[0:i1])
            i3 = i1 - len(temp)
            temp = self._getFrontNumStr(a[i2:])
            i4 = i2 + len(temp)

            temp = self._getEndNumStr(b[0:j1])
            j3 = j1 - len(temp)
            temp = self._getFrontNumStr(b[j2:])
            j4 = j2 + len(temp)

            if i3:
                filesDict = [
                        [a[0:i3]+'#'+a[i4:], a[i3:i4], b[j3:j4]],
                        [b[0:i1]+'%'+str(j4-j1)+'d'+b[j4:], a[i1:i4], b[j1:j4]]
                                ]
            else:
                filesDict = [
                        [a[0:i1]+'#'+a[i4:], a[i1:i4], b[j1:j4]],
                        [b[0:i1]+'%'+str(j4-j1)+'d'+b[j4:], a[i1:i4], b[j1:j4]]
                                ]
        else:
            filesDict = []
        return filesDict

    def _getMissList(self, frame1=0, frame2=0):
        """
        根据预设的起始帧和结束帧获取丢失帧列表
        """
        missList = []
        missList.extend(list(xrange(frame1, frame2)))
        return missList

    def _setResults(self, files1='', files2='', missList=[], files=[]):
        """将序列结果存入到预设的字典中"""
        results = self._filesCompare(files1, files2)
        if self.startFrame > -1:
            missList.extend(self._getMissList(self.startFrame, int(results[0][1])))
        if self.endFrame > 0:
            missList.extend(self._getMissList(int(results[0][2])+1, self.endFrame+1))
        missList.sort()
        self.sequenceDict1[results[0][0]] = [results[0][1], results[0][2], missList, files]
        self.sequenceDict2[results[1][0]] = [results[1][1], results[1][2], missList, files]

    def _filesAnalysis(self, files=[]):
        """递归分析多个文件列表是否形成序列文件"""
        if files:
            fileNum = len(files)
            if fileNum != 1:
                missList = []
                switch = 1
                temp = ''
                for i in xrange(1, fileNum):
                    results = self._filesCompare(files[i-1], files[i])
                    if results:
                        if temp:
                            if temp != results[0][0]:
                                switch = 0
                                i -= 1
                                break
                        else:
                            temp = results[0][0]
                        missList.extend(list(xrange(int(results[0][1])+1, int(results[0][2]))))
                    else:
                        switch = 0
                        break
                if switch:
                    self._setResults(files1=files[0], files2=files[i], missList=missList, files=files)
                    #results = self._filesCompare(files[0], files[i])
                    #self.sequenceDict1[results[0][0]] = [results[0][1], results[0][2], missList]
                    #self.sequenceDict2[results[1][0]] = [results[1][1], results[1][2], missList]
                else:
                    if i == 1:
                        self.separateFiles.append(files[0])
                    else:
                        self._setResults(files1=files[0], files2=files[i-1], missList=missList, files=files[:i])
                        #results = self._filesCompare(files[0], files[i-1])
                        #self.sequenceDict1[results[0][0]] = [results[0][1], results[0][2], missList]
                        #self.sequenceDict2[results[1][0]] = [results[1][1], results[1][2], missList]
                    self._filesAnalysis(files[i:])
            else:
                self.separateFiles.append(files[0])

    def setSequenceFiles(self, files=[], startFrame=-1, endFrame=0):
        """
        设置需要分析的文件列表
        files 为文件列表
        startFrame 为预设的起始帧
        endFrame 为预设的结束帧
        """
        if startFrame > -1:
            self.startFrame = int(startFrame)
        if endFrame > 0:
            self.endFrame = int(endFrame)
        files = sorted(files, key=lambda str: self._sequenceSortKey(str))
        self._filesAnalysis(files)



    def getSequenceInfo(self, mode=0):
        """
        返回文件列表的分析结果
        输入(默认mode=0):
            mode=0返回完整的数字序列(适合查询)
            mode=1返回不同部分的数字序列(适合ffmpeg插件)
        输出(字典类型):
            keys=序列文件的文件名
            keys.values[0], 起始帧
            keys.values[1], 结束帧
            keys.values[2], 缺失的序列列表
            keys.values[3], 当前序列规则的全部内容(方便进一步查询序列其他信息,例如文件大小)
            key='separateFiles',values=非序列文件列表
        """
        sequenceDict = {}
        if not mode:
            sequenceDict.update(self.sequenceDict1)
        else:
            sequenceDict.update(self.sequenceDict2)
        sequenceDict['separateFiles'] = self.separateFiles
        return sequenceDict

if __name__ == "__main__":
    filesList = ['aaa.1001.png', 'aaa.1002.png', 'aaa.1003.png', 'aaa.1004.png', 'aaa.1005.png', 'aaa.1006.png', 'aaa.1007.png', 'aaa.1008.png', 'aaa.1009.png']
    fileSequence = SequenceFileDetection()
    fileSequence.setSequenceFiles(filesList)
    fileSequence.getSequenceInfo()
    print fileSequence.getSequenceInfo()