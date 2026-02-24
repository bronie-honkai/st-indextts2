```markdown
# st-indextts2 更新报告

## v1.2.0 更新（2026-02-24）

简述：
本次 1.2.0 更新的核心目标是提升插件在没有外部 IndexTTS 后端服务可用时的可用性：

- 支持在不启动 IndexTTS 服务的情况下继续播放（优先使用本地缓存、已导入音频或 IndexedDB 回退），并在设置中增加 `allowFetch` / `autoInfer` 控制以精细化是否向远端发起请求。
- 改进设置读取与保存的鲁棒性（更健壮的 `getContext()`、深度合并默认项），减少环境差异导致的配置丢失。
- 优化音频缓存与导入机制，增强 IndexedDB 回退策略与本地目录导入能力，使得用户可以将已有音频资源作为播放来源。

影响与迁移建议（简要）：

- 若你依赖远端 IndexTTS 服务生成音频，建议在升级后在设置里检查 `TTS 服务地址` 与 `autoInference`/`allowFetch` 行为（是否允许插件在无服务时回退到本地音频）。
- 本次加强了本地音频与缓存的使用场景：若希望完全离线使用，请将想要的音频文件导入插件缓存或本地音频目录。

更多细节与历史改动请见下面的 2026-02-14 报告（已保留）。

---

更新时间：2026-02-14

概述：
本次更新为 `index.js` 的大幅重构与功能增强，保留原有 TTS 播放与缓存逻辑的同时，新增预设与本地目录集成、提示词注入、IndexedDB 配置存储等特性，并改进了设置管理与 UI。以下为主要变更要点、兼容性/迁移说明与建议操作。

主要变更：
- 设置管理改造
  - 新增预设（presets）架构：`getSettings()` 现在支持从 `window.SillyTavern.getContext().extensionSettings`（Context 优先）读取配置并进行迁移。
  - 新增函数 `getRootSettings()` 与 `switchPreset(name)`，支持预设切换、保存与删除。
  - 对默认设置做深度合并与字段补齐（保证向后兼容）。
- 提示词（Prompt Injection）功能
  - `defaultSettings` 中新增 `promptInjection` 配置（enabled/depth/role/content）。
  - 在设置面板中新增“提示词管理”模块，允许用户编辑注入内容与深度。
  - 通过事件 `CHAT_COMPLETION_PROMPT_READY` 注入提示词（若启用），插入位置基于 depth。该功能对聊天生成流程有直接影响，请谨慎使用。
- 本地目录与文件系统集成
  - 增加 `LocalRepo` 模块，使用 File System Access API（`showDirectoryPicker`）记录目录句柄并请求读写权限。
  - 设置面板增加本地目录选择、授权、扫描导入与导出功能，支持将本地音频文件导入 IndexedDB，或把缓存导出到指定文件夹。
- IndexedDB schema 与配置存储
  - IndexedDB 打开版本由 `1` -> `2`，新增 `configs` 对象仓库，用于保存 `localDirHandle` 等持久句柄。
  - 增加 `AudioStorage.saveConfig(key, value)` 与 `AudioStorage.getConfig(key)` 用于存储额外配置。
- 自动推理控制与容错
  - `ensureAudioRecord()` 新增 `allowFetch` 参数（用于控制是否允许发起 TTS API 请求，用于自动推理策略）。
  - `playSingleLine()` 支持 `autoInfer` / `allowFetch` 控制，避免在某些自动场景下触发网络请求。
- UI/UX 改进
  - 配音弹窗（showConfigPopup）加入预设管理条（保存/删除/切换预设）。
  - 设置面板改为更丰富的模块：预设管理、提示词管理、播放自动化、本地缓存控制等。
  - 行内注入逻辑与播放控制（miniplayer）增强，支持全局播放进度（playlist）与拖动 seek。
- 其他实用改进
  - 增强日志输出与错误处理（更多 console.warn / console.error）。
  - `convertToWav`、`audioBufferToWav` 等音频处理保持兼容并增加调试信息。

影响与迁移说明：
- 设置迁移：旧版的单一配置会自动迁移到新版的预设结构（`presets`），但建议在更新后检查设置面板确保 `selected_preset` 与 `promptInjection` 等字段符合期望。
- IndexedDB：数据库版本升级（1 -> 2）会触发 `onupgradeneeded`，新增 `configs` object store；首次打开可能需要短时间完成升级。
- 本地目录授权：新增的本地导入/导出依赖浏览器支持 File System Access API（在桌面 Chrome/Edge 支持良好）。若授权失败，导入/导出功能将不可用。
- 提示词注入：若启用，可能改

