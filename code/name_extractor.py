# -*- coding: utf-8 -*-

"""This module is for extracing 
user names of those who 
either liked or commentted
on my video

TODO: to actually check the timestamp...it's not done ╮(╯_╰)╭
"""

from html.parser import HTMLParser
import io
import os
import sys


UnqualifiedNames = ["昔年_之殇", "我愛如花", "梦林夕晨", "花京院典明Q", "京剧猫黑糖", "小黒化布哆", "乱斗DJ裂空君", "微热巫女不会受伤","Chips土豆片","不如吃茶克","我是老牛呀","开心T恤","一只暖心桂","CR_门外汉"]

class LikerNameParser(HTMLParser):

    def __init__(self):
        # initialize the base class
        HTMLParser.__init__(self)
        self.isDataOfInterest = False
        self.name_list = []

    def handle_starttag(self, tag, attrs):
        # Detect the likers
        if tag == "a":
            if len(attrs) == 4:
                if attrs[0][0] == "data-v-f798d496":
                    if attrs[1][0] == "href":
                        if attrs[2][0] == "target":
                            if attrs[3][0] == "title":
                                # print("Start tag:", tag)
                                # for attr in attrs:
                                #     print("     attr:", attr)
                                self.isDataOfInterest = True
                                # print("Detected.")

    def handle_data(self, data):
        # print("Data     :", data)
        if self.isDataOfInterest:
            # print("Data of interests: ", data)
            if not data.encode('utf-8') in self.name_list:
                self.name_list.append(data.encode('utf-8'))
            self.isDataOfInterest = False
        pass

    def get_namelist(self):
        return self.name_list
        

# Example Sequences:
# <a data-usercard-mid="323998129" href="https://space.bilibili.com/323998129" 
# target="_blank" class="name ">-ALL-IN-</a>
# <a href="https://www.bilibili.com/blackboard/help.html#%E4%BC%9A%E5%91%98%E7%AD%89%E7%BA%A7%E7%9B%B8%E5%85%B3" 
# target="_blank"><i class="level l4"></i></a></div>
# <p class="text">最喜欢桶子，就算削过大招距离也还是带劲，很不理解那些说达里尔废的人</p>

class CommenterNameParser(HTMLParser):

    def __init__(self):
        # initialize the base class
        HTMLParser.__init__(self)
        # self.isFirstSequenceDetected = False  # Used if detecting the content of the comment
        self.isDataOfInterest = False
        self.name_list = []

    def handle_starttag(self, tag, attrs):
        # Detect the name of the commenter
        if tag == "a":
            if len(attrs) == 4:
                if attrs[0][0] == "data-usercard-mid":
                    if attrs[1][0] == "href":
                        if attrs[2][0] == "target":
                            if attrs[3][0] == "class":
                                # print("Start tag:", tag)
                                # for attr in attrs:
                                #     print("     attr:", attr)
                                self.isDataOfInterest = True
                                # print("Detected.")

        # Detect the content of the comment
        # if tag == "p" :
        #     if len(attrs) == 1:
        #         if attrs[0][0] == "class" and attrs[0][1] == "text":
        #             print("Start tag:", tag)
        #             for attr in attrs:
        #                 print("     attr:", attr)
        #             self.isDataOfInterest = True
        #             self.isFirstSequenceDetected  = False
        #             print("Detected.")

    def handle_data(self, data):
        # print("Data     :", data)
        if self.isDataOfInterest:
            # print("Data of interests: ", data)
            if not data.encode('utf-8') in self.name_list:
                if not data.encode('utf-8') in UnqualifiedNames:
                    self.name_list.append(data.encode('utf-8'))
            self.isDataOfInterest = False
        pass

    def get_namelist(self):
        return self.name_list

def name_extractor(type, deadline):
    if type == "like":
        print("********************************")
        print("****赞了视频的观众有……****")
        page_path = "/Users/yijizhang/20191101-BS-raffle/htmls/like_page.html"
    elif type == "comment":
        print("****评论了视频的观众有……****")
        page_path = "/Users/yijizhang/20191101-BS-raffle/htmls/comment_page.html"
    else:
        print("Type not supprted. Exit.")
        sys.exit(1)


    file = open(page_path, "r")
    data = file.read().decode('utf-8')
    file.close()

    if type == "like":
        parser = LikerNameParser()
    elif type == "comment":
        parser = CommenterNameParser()
    else:
        print("Type not supprted. Exit.")
        sys.exit(1)

    parser.feed(data)
    names = parser.get_namelist()
    for name in names:
        print name.decode('utf-8') # KEEP!!! How to print it out in Chinese...
    print("****总计：" + str(len(names)) + " 位。****\n")
    print("********************************")
    return names


def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

def get_final_names():
    likers = name_extractor("like","ddl")
    commenters = name_extractor("comment","ddl")
    qualifiers = intersection(likers,commenters)
    print("********************************")
    print("****最终符合抽奖资格的观众有……****")
    for name in qualifiers:
        print name.decode('utf-8') # KEEP!!! How to print it out in Chinese...
    print("****总计：" + str(len(qualifiers)) + " 位。****")
    print("********************************")
    return qualifiers

def main():
    # testing
    likers = name_extractor("like","ddl")
    commenters = name_extractor("comment","ddl")
    qualifiers = intersection(likers,commenters)
    print("********************************")
    print("****最终符合抽奖资格的观众有……****")
    for name in qualifiers:
        print name.decode('utf-8') # KEEP!!! How to print it out in Chinese...
    print("****总计：" + str(len(qualifiers)) + " 位。****")
    print("********************************")

if __name__ == "__main__":
    main()

### example html sequence that contains the Timestamp info I need:
# <span data-v-0bc25b4d="" data-v-f798d496="" class="time time-span">2019年10月26日 04:50</span>
