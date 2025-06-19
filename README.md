# 基于 Wallpaper Engine 的动态风流桌面壁纸

本项目旨在通过 Wallpaper Engine 实现动态风流桌面壁纸，利用 HTML5 或网页技术制作可交互、可动画的风流可视化效果，适合 Windows 用户。

## 项目简介

本项目不再依赖 PyQt5 或 Python 程序，而是采用 Wallpaper Engine 这一强大的动态壁纸平台。Wallpaper Engine 支持视频、GIF、网页、HTML5 以及用户自定义内容，能够让用户轻松将网页动画作为桌面壁纸。
我们将使用 HTML5/JavaScript 技术开发风流可视化网页，并通过 Wallpaper Engine 加载，实现实时、动态的风流展示。

- [cambecc/earth](https://github.com/cambecc/earth)：全球气象可视化项目，提供了风场数据可视化和粒子动画的核心实现。
- [NoisyWinds/Wallpaper](https://github.com/NoisyWinds/Wallpaper)：基于 HTML5/C++ 的桌面动态壁纸项目，提供了 HTML5 动态壁纸的实现范例。

本项目的目标已经明确： 
    制作一个HTML5 动态地图 天气风流场 的网页 ，  导入 到Wallpaper Engine 编辑器 即可实现
        或者 /Wallpaper 项目提供的 桌面启动器 也可加载：（ 2018年的项目， 有显示错误 需要修改）

动态网页的实现，核心在于：
获取和解析气象流场数据
用 WebGL/Canvas 实现高性能粒子动画
结合地图投影和丰富交互，提升可视化体验


## 主要特性

- **Wallpaper Engine 支持**：充分利用 Wallpaper Engine 对网页、HTML5 动态内容的支持
- **动态风流展示**：通过 HTML5/Canvas/WebGL 实现流畅的风流动画
- **可交互性**：可根据需要添加交互功能（如切换风层、显示风速等）
- **高兼容性**：适用于 Windows 10/11，完美集成于桌面环境
- **易于扩展**：可自定义风流数据源、动画样式等

## 技术实现

- **Wallpaper Engine**：动态壁纸平台，支持网页/HTML5内容
- **HTML5 + JavaScript**：实现风流动画与交互逻辑
- **CSS3**：美化界面与动画效果
- **（可选）第三方可视化库**：如 D3.js、three.js 等增强动画表现

## 制作与导入动态壁纸

### 1. 创建 HTML 文件

- 使用 HTML5、CSS 和 JavaScript 编写一个动态网页（如风流动画、粒子特效等）。
- 推荐文件结构如下：

```
wind_flow_wallpaper/
├── index.html           # 主网页文件
├── assets/              # 图片、图标等资源
├── scripts/             # JavaScript 动画与交互脚本
└── styles/              # CSS 样式文件
```

- 在 index.html 中引入相关 JS 和 CSS，实现动画、交互等效果。

### 2. 导入 Wallpaper Engine

- 打开 Wallpaper Engine，选择"网页"类型。
- 导入包含 index.html 及相关资源的文件夹。
- 软件会将网页渲染为动态壁纸，并支持交互效果（如鼠标移动触发动画、点击切换风层等）。

### 3. 交互与扩展

- 可在 JavaScript 中监听鼠标、键盘等事件，实现更多交互。
- 支持自定义数据源、动画参数，打造个性化动态壁纸。

### 4. 示例

- 很多用户通过 HTML5 制作了极具视觉冲击力的动态壁纸，例如"极乐净土"舞蹈动画、粒子流动、3D 场景等，效果非常炫酷。
- 你也可以将风流可视化、天气动画等创意内容作为桌面壁纸。

## 使用方法

1. 安装并启动 Wallpaper Engine（需在 Steam 平台购买）
2. 在 Wallpaper Engine 中选择"从网页/HTML 文件导入"
3. 选择本项目提供的 HTML5 风流动画文件，或输入在线网页地址
4. 应用为桌面壁纸，享受动态风流效果

## 系统要求

- Windows 10/11
- 已安装 Wallpaper Engine
- 支持 HTML5 的现代浏览器内核（Wallpaper Engine 内置）

## 文件结构（示例）

- `wind_flow_wallpaper/index.html`：主网页文件，包含风流动画逻辑
- `wind_flow_wallpaper/assets/`：动画所需图片、图标等资源
- `wind_flow_wallpaper/scripts/`：JavaScript 动画与交互脚本
- `wind_flow_wallpaper/styles/`：CSS 样式文件

## 注意事项

- 需购买并安装 Wallpaper Engine
- 动态壁纸效果取决于 HTML5 动画实现质量
- 如需自定义数据源或动画，请修改 HTML/JS 文件

## 许可证

本项目采用 MIT 许可证。

## 参考与致谢

本项目参考或借鉴了以下开源项目的实现思路和技术：

- [cambecc/earth](https://github.com/cambecc/earth)：全球气象可视化项目，提供了风场数据可视化和粒子动画的核心实现。
- [NoisyWinds/Wallpaper](https://github.com/NoisyWinds/Wallpaper)：基于 HTML5/C++ 的桌面动态壁纸项目，提供了 HTML5 动态壁纸的实现范例。
