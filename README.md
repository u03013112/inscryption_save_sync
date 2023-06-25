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
    3、查询存档文件，主要针对的是文件中的playTime字段，用于判断哪个是最新的存档文件
    
    暂时无需任何认证，存档文件普遍不大（500KB以内），所以上传和下载完全可以同步，不分片，不验证完整性（暂时）

## 2. 客户端

    python3

    不需要docker封装，直接运行即可
    需要一个配置文件（config.py），存储服务器的地址和端口，以及本地存档文件的路径

    提供功能：
    1、检查本地存档文件，与查询服务器上的存档文件，判断哪个是最新的存档文件
    2、如果本地存档文件不是最新的，那么就建议下载最新的存档文件
    3、如果本地存档文件是最新的，那么就建议上传最新的存档文件
    4、如果有必要，可以强制上传或者下载存档文件，强制时会给出警告
