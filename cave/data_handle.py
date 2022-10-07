# Python Script Created by MRS
import json, requests, random
import os, re

from nonebot import on_command, get_driver, Config
config = Config.parse_obj(get_driver().config.dict())

from typing import Union

relative_url = "./data/cave/"
abstract_url = "file:///home/ubuntu/NewRio/newRio/data/cave/"

class Handle():
    @staticmethod
    def __check_path():
        if(not os.path.exists(relative_url)):
            os.mkdir("./data/cave")
            with open(relative_url + "cave.json") as f:
                content = {"max": 0}
                json.dump(content, f, indent=4, ensure_ascii=False)
            with open(relative_url + "cave_temp.json") as f:
                content = {"max": 0}
                json.dump(content, f, indent=4, ensure_ascii=False)
            return
        elif(not os.path.exists(relative_url + "cave.json")):
            with open(relative_url + "cave.json") as f:
                content = {"max": 0}
                json.dump(content, f, indent=4, ensure_ascii=False)
        elif (not os.path.exists(relative_url + "cave_temp.json")):
            with open(relative_url + "cave_temp.json") as f:
                content = {"max": 0}
                json.dump(content, f, indent=4, ensure_ascii=False)

    @staticmethod
    def add_image(qq: int, url: str) -> None: #添加图片
        Handle.__check_path()
        try:
            img = requests.get(url, timeout=15).content
        except ConnectionError as e:
            print(e)
            raise ConnectionError

        with open(relative_url + "cave.json", "r", encoding="utf-8") as f2:
            content = json.load(f2)
        content["max"] += 1
        file_name = str(content["max"]) + ".png"
        with open(relative_url + "images/"+ file_name, "wb") as f1:
            f1.write(img)

        data = dict()
        data[content["max"]] = {"user": qq, "type": "image", "url": abstract_url+"images/"+ file_name}
        content.update(data)
        with open(relative_url + "cave.json", "w", encoding="utf-8") as f3:
            json.dump(content, f3, indent=4)

    @staticmethod
    def add_text(qq: int, text: str) -> None: #添加文字
        Handle.__check_path()
        with open(relative_url + "cave.json", "r", encoding="utf-8") as f:
            content = json.load(f)
        content["max"] += 1
        data = dict()
        data[content["max"]] = {"user": qq, "type": "text", "content": text}
        content.update(data)
        with open(relative_url + "cave.json", "w", encoding="utf-8") as f2:
            json.dump(content, f2, indent=4, ensure_ascii=False)

    @staticmethod
    def read_cave(num: int):
        """
        读取特定cave\n
        :return: cave信息列表 [类型, 添加者qq, 内容]
        :exception: json文件格式异常
        """
        Handle.__check_path()
        with open(relative_url + "cave.json", "r", encoding="utf-8") as f:
            content = json.load(f)
        if(content["max"] < num):
            return -1
        else:
            data = content[str(num)] #KeyError
            if (data["type"] == "image"):
                return ["image", data.get("user"), data.get("url")]
            elif (data["type"] == "text"):
                return ["text", data.get("user"), data.get("content")]

    @staticmethod
    def del_cave(num: int) -> Union[int, None]:
        Handle.__check_path()
        with open(relative_url + "cave.json", "r", encoding="utf-8") as f:
            content = json.load(f)

        data = content[str(num)] #KeyError

        if (content["max"] < num):
            return -1
        else:
            if(data["type"] == "image"):
                try:
                    os.remove("/home/ubuntu/NewRio/newRio/data/cave/images/" + str(num) + ".png") #FileNotFoundError
                except FileNotFoundError:
                    pass
            content.pop(str(num))
            with open(relative_url + "cave.json", "w", encoding="utf-8") as f:
                json.dump(content, f, indent=4, ensure_ascii=False)


    @staticmethod
    def choose_cave():
        """
        随机选取一个cave\n
        :return: cave信息列表 [类型, 添加者qq, 内容]
        :exception: json文件格式异常
        """
        Handle.__check_path()
        with open(relative_url + "cave.json", "r", encoding="utf-8") as f:
            content = json.load(f)
        if(content["max"] == 0):
            raise Exception("当前没有存储cave!")
        while(1):
            try:
                num = random.randint(1, content["max"])
                data = content[str(num)]
                break
            except KeyError:
                pass
        if(data["type"] == "image"):
            return ["image", data.get("user"), data.get("url"), num]
        elif (data["type"] == "text"):
            return ["text", data.get("user"), data.get("content"), num]
        else:
            raise Exception("文件格式错误!请检查json文件")

    @staticmethod
    def checkMsg(uid: int, content: str):
        # patt = re.compile(r"\[CQ:(.*?)]")
        # b = re.sub(patt, "", content)
        # if(b.__eq__("")):
        #     return "目前暂不支持图片+文字消息"

        if(str(uid) not in config.superusers):
            res = Handle._add_temp_cave(uid, content)
            if(res == -1):
                return "临时cave存储出错!"
            return res

        if (content.count("CQ") == 0):
            try:
                Handle.add_text(uid, content)
                return "添加成功!"
            except Exception as e:
                print(e)
                return
        elif (content.count("CQ") >= 2):
            Handle.add_text(uid, content)
            return "非本地图片添加成功!"
        elif (content.count("CQ") == 1):
            pattern = re.compile(r"CQ:image(.+?)url=(?P<url>.*?)]")
            match = re.search(pattern, content)
            if (match is None):
                return "不支持的消息类型!应当为图片/纯文字"
            url = match.group("url")
            try:
                Handle.add_image(uid, url)
                return "添加成功!"
            except ConnectionError:
                return "连接超时!无法保存图片..."
            except Exception as e:
                print(e)
                return -1

    @staticmethod
    def validation_file() -> int:
        """
        效验cave正确性

        :return: 被删cave数量
        """
        with open(relative_url + "cave.json", "r", encoding="utf-8") as f:
            content = json.load(f)
        count = 0
        for i in content.keys():
            if(i == "max"):
                continue
            data = content[i]
            if(data["type"] == "text"):
                if(data["content"] == ""):
                    Handle.del_cave(int(i))
                    count += 1
            elif(data["type"] == "image"):
                url = data["url"]
                url = url.replace(abstract_url, "")
                new_url = relative_url + url
                if(not os.path.exists(new_url)):
                    Handle.del_cave(int(i))
                    count += 1
        return count

    """
    临时cave函数
    """
    @staticmethod
    def _progress_all_cave(is_ok: bool):
        with open(relative_url + "cave_temp.json", "r", encoding="utf-8") as f2:
            content = json.load(f2)
        max = content["max"]
        for i in range(1, max + 1):
            try:
                info = content[str(i)]
            except KeyError:
                continue
            Handle._choose_temp_cave(i, is_ok)
        Handle._clear_temp_cave()
        return "已全部处理!"

    @staticmethod
    def __temp_img(qq: int, url: str):
        """
        临时图片

        :param qq: 添加者qq
        :param url: 图片链接
        :return:
        """
        # print("=========1")
        with open(relative_url + "cave_temp.json", "r", encoding="utf-8") as f2:
            content = json.load(f2)
        content["max"] += 1

        data = dict()
        # print("=========2")
        data[content["max"]] = {"user": qq, "type": "image", "url": url}
        content.update(data)
        # print("=========3")
        with open(relative_url + "cave_temp.json", "w", encoding="utf-8") as f3:
            json.dump(content, f3, indent=4)
        # print("=========4")

    @staticmethod
    def __temp_text(qq: int, text: str):
        """
        临时文本

        :param qq: 添加者qq
        :param text: 文本内容
        :return:
        """
        with open(relative_url + "cave_temp.json", "r", encoding="utf-8") as f:
            content = json.load(f)
        content["max"] += 1
        data = dict()
        data[content["max"]] = {"user": qq, "type": "text", "content": text}
        content.update(data)
        with open(relative_url + "cave_temp.json", "w", encoding="utf-8") as f2:
            json.dump(content, f2, indent=4, ensure_ascii=False)

    @staticmethod
    def _add_temp_cave(qq: int, content: str):
        if (content.count("CQ") >= 2):
            return "目前暂不支持同一个消息添加两张以上的图片!"
        elif (content.count("CQ") == 1):
            pattern = re.compile(r"CQ:image(.+?)url=(?P<url>.*?)]")
            match = re.search(pattern, content)
            if (match is None):
                return "不支持的消息类型!应当为图片/纯文字"
            url = match.group("url")
            try:
                Handle.__temp_img(qq, url)
                return "添加成功!"
            except Exception as e:
                print(e)
                return -1
        else:
            try:
                Handle.__temp_text(qq, content)
                return "添加成功!"
            except Exception as e:
                print(e)
            finally:
                return

    @staticmethod
    def _del_temp_cave(num: int):
        with open(relative_url + "cave_temp.json", "r", encoding="utf-8") as f:
            content = json.load(f)

        data = content[str(num)]  # KeyError

        if (content["max"] < num):
            return -1
        else:
            content.pop(str(num))
            with open(relative_url + "cave_temp.json", "w", encoding="utf-8") as f:
                json.dump(content, f, indent=4, ensure_ascii=False)

    @staticmethod
    def _clear_temp_cave():
        """
        清除全部临时cave
        :return:
        """
        with open("./data/cave/cave_temp.json", "w", encoding="utf-8") as f:
            content = {"max": 0}
            json.dump(content, f, indent=4)
        return "清理完成!"

    @staticmethod
    def _show_temp_cave():
        with open(relative_url + "cave_temp.json", "r", encoding="utf-8") as f:
            content = json.load(f)
        lst = []
        for i in content.keys():
            if(i == "max"):
                continue
            data = content[i]
            if (data["type"] == "image"):
                lst.append(["image", data.get("user"), data.get("url"), i])
            elif (data["type"] == "text"):
                lst.append(["text", data.get("user"), data.get("content"), i])
        if(len(lst) == 0):
            return -1
        return lst

    @staticmethod
    def _choose_temp_cave(num: int, is_ok: bool):
        if(not is_ok):
            try:
                Handle._del_temp_cave(num)
            except KeyError:
                return "不存在该临时cave!"
            return "已删除!"
        with open(relative_url + "cave_temp.json", "r", encoding="utf-8") as f:
            content = json.load(f)
        try:
            data = content[str(num)]
            if(data["type"] == "text"):
                Handle.add_text(data["user"], data["content"])
            elif(data["type"] == "image"):
                Handle.add_image(data["user"], data["url"])
            else:
                return "Json文件格式错误!!!"
        except KeyError:
            return "不存在该临时cave!"
        Handle._del_temp_cave(num)
        return "添加成功!"