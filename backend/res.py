class result():

    def __init__(self) -> None:
        self.res_empty = "Module is empty"
        self.res_imageinfo = {}

    def clear_res(self, module: str) -> None:
        """
        对指定模块的储存进行清空
        """
        if module in self.res_imageinfo.keys():
            self.res_imageinfo.pop(module)
        else:
            return "Module is empty"

    def add_res(self, module: str, data: str) -> None:
        """
        将结果储存到指定模块
        """
        # 储存扫描结果，module以vol模块格式
        if module not in self.res_imageinfo.keys():
            self.res_imageinfo[module] = data
        else:
            self.res_imageinfo[module] += data

    def get_res(self, module: str) -> str:
        """
        读取特定模块的结果
        """
        # 调用扫描结果，module以vol模块格式
        if module in self.res_imageinfo.keys():
            return self.res_imageinfo[module]
        else:
            return self.res_empty

    def format_res(self, data: str, module: str) -> str:
        """
        针对特定模块的数据进行格式化处理
        """
        data = data.split("\n")
        data = [i for i in data if i != ""]
        if module == "imageinfo":
            res = [i.strip().split(":", maxsplit=1) for i in data]
        elif module == "pslist":
            res = data[2:]
            res = [i.split(" ") for i in res]
            for offset, sub in enumerate(res):
                tmp = [i for i in sub if i != ""]
                res[offset] = tmp[0:8] + [" ".join(tmp[8:])]
        elif module == "cmdline":
            res = [i for i in data if i != "*" * 72]
        else:
            res = [data]
        return res


core_res = result()
