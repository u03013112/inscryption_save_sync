# inscryption_save_sync
鉴于inscryption居然没有云同步存档功能（不同操作系统之间），使得我非常不开心，所以简单的写一个存档文件同步功能。

我分别在 win11 和 macos 上进行游戏，但是发现存档文件并不会同步，真的蠢。

我的macos存档路径 '~/Library/Application Support/Steam/steamapps/common/Inscryption/Inscryption.app/SaveFile.gwsave'

win11存档路径 'D:\Steam\steamapps\common\Inscryption\SaveFile.gwsave'

我找了一台linux服务器来做存档管理

## 1. 服务器端

    python 3

    docker封装，使用docker-compose管理，暂时无需任何配置与外部文件挂在，完全放在docker里面，暴露一个端口，暂定为 8888。

    提供功能：
    1、上传存档文件
    2、下载存档文件
    
    在服务端只保留一个存档文件，中间走HTTP协议，存档是纯文本文件，存到容器内的'/app/SaveFile.gwsave'

    暂时无需任何认证，存档文件普遍不大（500KB以内），所以上传和下载完全可以同步，不分片，不验证完整性（暂时）

## 2. 客户端

    python3

    不需要docker封装，直接运行即可
    需要一个简单的小界面，界面上有一个文本框，显示服务器IP+端口，当前的存档文件的路径，以及3个按钮，一个是'同步'，一个是'强制上传'，一个是‘强制下载’

    需要一个配置文件（config.json），存储服务器的地址和端口，以及本地存档文件的路径。
    配置文件内容类似
    {
        "serverIP":"",
        "serverPort":8888,
        "savePath":""
    }

    流程：
    1、程序启动，读取配置文件，没有配置文件在文本框报错
        然后尝试下载服务器上的存档文件
        如果下载失败，那么在界面上提示下载失败，这可能是网络或者服务器的问题，直接报错
    2、将下载文件和本地存档文件进行解析（都是json），通过获取'playTime'字段，判断哪个是最新的存档文件
        如果本地存档文件不是最新的，那么就建议覆盖本地存档文件
        如果本地存档文件是最新的，那么就建议上传最新的存档文件
    3、如果有必要，可以强制上传或者下载存档文件，强制时会给出警告
