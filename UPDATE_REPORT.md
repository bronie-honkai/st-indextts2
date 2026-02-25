# v1.3.0 更新说明（2026-02-25）

更新摘要：
- 版本号：v1.3.0（在 `manifest.json` 中已更新）
- 主要目标：提升离线与无后端场景下的可用性、增强设置迁移稳定性以及改进播放与缓存的健壮性。

关键变更：

1. 离线与回退策略优化
   - 增强了对本地缓存（IndexedDB）与已导入音频的优先使用，能够在 IndexTTS 服务不可用时回退到本地播放，减少用户中断感。
   - 在 IndexedDB 中新增/完善 `configs` store（见 `index.js` 中的打开逻辑），音频持久化与配置更可靠。

2. 设置与预设框架改进
   - 引入并稳定了预设（presets）结构：`getRootSettings`、`switchPreset` 与 `saveSettings` 支持完整迁移与深度补齐默认值（`deepMergeDefaults`）。
   - 改进了向后兼容的迁移逻辑：旧版扁平设置会自动迁移为 `presets` 结构并保留用户自定义值。

3. 更健壮的运行时环境检测与容错
   - 新增更健壮的 `getContext()` 获取方式，兼容多种 SillyTavern 上下文访问形式并捕获错误，避免在特殊环境下直接抛错导致扩展崩溃。
   - 更完善的音频缓存清理（`clearMemoryAudioCache`）与播放状态管理，能更安全地释放 Blob URL 并重置播放状态。

4. 播放器与用户体验改进
   - 迷你播放器、播放列表与控制器结构增强，支持更稳定的 seek/播放控制和会话管理。
   - 行内播放、解析模式（GAL / Audiobook）和自动推理（`autoInference`）的默认行为与配置更加直观。

5. 开发与兼容性改进
   - 代码中加强了对文件名后缀的保障（`ensureWavSuffix`）、样式加载检查（`ensureCssLoaded`）等小修复，提升跨平台兼容性。

迁移与注意事项：
- 升级到 v1.3.0 时，扩展会尝试自动将旧版设置迁移为新的 `presets` 架构；建议在升级前备份原有设置与 IndexedDB（若你保存了自定义音频）。
- 如果你使用自建 IndexTTS 服务：请确认 `manifest.json` / 设置中的 `apiUrl` 与 `cloningUrl` 配置正确。
- 如果出现远程推送或网络调用失败，扩展会优先使用本地缓存音频（若存在）。

已包含的文件（新版本目录）：
- index.js
- manifest.json （version: 1.3.0）
- style.css
- README.md
- test.py / test-japanese.py（测试脚本）

提交与发布建议（Git 操作示例）：
```powershell
cd <your-repo-root>
git checkout -b release/st-indextts2-v1.3.0
git add public/scripts/extensions/third-party/st-indextts2-new/
git commit -m "chore(st-indextts2): release v1.3.0 — 增强离线回退与设置迁移"
git tag -a v1.3.0 -m "st-indextts2 v1.3.0"
git push origin HEAD
git push origin --tags
```

如果你需要，我可以在当前工作区里执行上述提交与推送命令（需要本机已配置 Git 凭据并能访问远程仓库）。

问题反馈与后续计划：
- 建议把升级后的 `manifest.json` 与 `UPDATE_REPORT.md` 一并提交到仓库，并在 Release 中附上升级说明与常见问题（FAQ）。
- 后续可以增加自动化升级检测与一键备份导出功能，便于用户在升级前保存自定义音频与设置。

— kirara
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

