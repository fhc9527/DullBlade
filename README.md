# DullBlade
Automated web reconnaissance &amp; vulnerability scanning tool.Simple, stable, powerful. 	
    在进行测试的时候就想着，既然我一步步执行脚本，oneforall跑资产，提子域名，又要对子域名进行批量的存活探测，在使用xray进行被动扫描，测poc，那我可不可以写一个脚本，链接这几个步骤，实现自动化执行呢，天天视频、博客、平台东学一下西学一下，接触也有2年了，在ai发展到今天，实现这个功能简直太简单了，写在这里，是为了以后在加一些其他的东西。
    在调用oneforall的时候注意路径，使用的相对路径，这个oneforall、xray的工具也不是最新的，如果有朋友看到这个脚本，有幸下载，使用自己的工具，无非就是改下路径的问题，直接把自己的工具复制进来即可，使用我这个不知道经历几手的工具也是可以跑的，哈哈。oneforall的路径修改在utils/oneforall_runner.py中，代码好找改下就行，xray的径在modules/scanner.py中，同样好找，自己改改就行，有最新的还是建议使用最新的哈，我这好多手了。
    经过测试是可以，全自动化的，只需要把想跑的资产域名放入1.txt中，配置好相应环境，双击main.py，即可执行，
<img width="1692" height="804" alt="image" src="https://github.com/user-attachments/assets/c54d4b1d-fd96-4a6e-b9d8-314a78d9de68" />
会按照oneforall-提取子域名-存活探测-xray的顺序执行哈。
    最后，这是自己学习写的，存在不足太多，如果涉及其他问题，即使告知即可。
