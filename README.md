# nonbot-plugin-leetcode-everyday
刚接触聊天机器人，做个玩玩。可以定时发送lc每日一题，也可以在qq里发送 <code>/每日一题</code> 获取
## 依赖
本插件使用onebot适配器，并且依赖官方插件 <code>nonebot-plugin-apscheduler</code>
## 如何使用
本插件暂未发布，如需使用，可以clone本仓库到本地使用。<br>另外由于本插件使用了无头浏览器进行渲染，内存消耗较大，请自行斟酌如何使用
### 配置
您可以在 <code>.env</code> 文件中配置如下参数:
>lce_hour : int -> 订阅发送时间，以北京时间表示，默认为北京时间八点<br><br>
>lce_admin : dict[str , list] -> 管理员，可以识别<code>users</code>和<code>groups</code>键，分别为管理员用户和管理员群，值为qq号/群号数组。例：lce_admin={"users":[123456789]}<br><br>
>lce_subscriber : dict[str , list] -> 同上，但一般无需配置<br><br>
>lce_size : dict[str , int] -> 默认值为{"width":500,"height":300}，表示无头浏览器视口大小，影响最终图片大小
<br><br>
### 在qq中使用
任一用户/群均可通过私聊/at发送 <code>/每日一题</code> 或 <code>/lce</code> 获得当天的题目，或在订阅后等待机器人发送
#### 管理员指令
本插件只能由管理员代为订阅/退订(主要是作者摆了)<br>
向机器人发送 <code>/管理</code> 或 <code>/lcem</code> 开启管理任务，然后可以发送以下指令:
><code>更新</code> 或 <code>update</code> : 立刻更新一次每日一题缓存<br><br>
><code>结束</code> 或 <code>finish</code> : 结束管理任务<br><br>
><code>状态</code> 或 <code>status</code> : 查看插件运行状态，管理员和订阅情况等<br><br>
><code>大小</code> 或 <code>size</code> : 调整浏览器视口大小，间接影响图片大小，接受两个整型参数，第一个参数为宽，第二个参数为高，例:<code>size 500 300</code><br><br>
><code>加订</code> 或 <code>add</code> : 增加订阅用户，后接以空格分隔的参数列，接受的第一个参数为<code>user</code> 或 <code>group</code> 指明后续参数是qq号还是群号，后续可以跟任意长的参数，例:<code>add user 123456789 987654321</code><br><br>
><code>退订</code> 或 <code>remove</code> : 移除订阅用户，参数同上，例:<code>remove user 123456789 987654321</code><br><br>
此外各指令还有一些别名，具体可以直接参考源码
## 感谢
感谢以下项目，在本插件制作过程中从其中吸收了许多经验<br>
[Nranphy/nonebot_plugin_leetcode](https://github.com/Nranphy/nonebot_plugin_leetcode)<br>
[zxz0415/leetcode](https://github.com/zxz0415/leetcode)<br>
[kexue-z/nonebot-plugin-htmlrender](https://github.com/kexue-z/nonebot-plugin-htmlrender)
