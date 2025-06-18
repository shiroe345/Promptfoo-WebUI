# LLM 數位證書客服評估框架

本專案使用 promptfoo 建立統一的 LLM 評估框架，用於測試數位證書客服機器人的回應品質及拒絕非相關問題的能力。專案支援基本問答和工具調用(function/tool calling)兩種評估模式。

## 專案結構
```
/Promptfoo-WebUI
│
├── promptfooconfig.yaml     # 主要配置檔，定義模型、測試和評估方式
├── README.md                # 專案說明文件
├── promptfoo-errors.log     # 錯誤日誌檔案
│
├── data/                    # 測試數據目錄
│   ├── digsign_basic.csv    # 基本問答測試數據
│   └── digsign_tool.csv     # 工具調用測試數據
│
├── prompts/                 # 提示詞模板目錄
│   ├── prompt_basic.yaml    # 基本問答系統提示
│   └── prompt_tool.yaml     # 工具調用系統提示
│
├── providers/               # 模型提供者配置目錄
│   ├── llama2.yaml          # Llama 2 模型配置
│   ├── llama3_1.yaml        # Llama 3.1 模型配置
│   ├── breeze.yaml          # Breeze 繁體中文模型配置
│   ├── breeze2.yaml         # Breeze 2 繁體中文模型配置
│   ├── Llama-3.2-3B-F1.yaml # Llama 3.2 3B F1 模型配置
│   ├── gemma3.yaml          # Gemma 3 模型配置
│   └── gpt-4o-mini.yaml     # OpenAI GPT-4o Mini 模型配置
│
└── tests/                   # 測試案例目錄
    ├── generate.py          # 測試案例生成器，包含 basic_eval 和 tool_eval 方法
    └── __pycache__/         # Python 快取目錄
```

## 使用方法

### 環境準備

1. **Node.js 環境**
   確保已安裝 Node.js (建議 v14 或更高版本)
   ```bash
   node --version
   ```

2. **安裝 promptfoo**
   ```bash
   npm install -g promptfoo
   ```

3. **Python 環境**
   確保已安裝 Python 3.8+ 並安裝了 pandas 套件
   ```bash
   pip install pandas
   ```

4. **設定 Ollama (如使用本地模型)**
   確保 Ollama 服務已啟動並載入所需模型
   ```bash
   ollama list
   # 如需載入模型，例如
   ollama pull llama2
   ollama pull ycchen/breeze-7b-instruct-v1_0
   ```

5. **設定 OpenAI API**
   - 如果有使用預設的 provider (gpt-4.1)，需要設置環境變數

   設定環境變數
   ```bash
   # Windows
   set OPENAI_API_KEY=your_api_key

   # Linux/Mac
   export OPENAI_API_KEY=your_api_key
   ```

### 執行評估流程

#### 配置評估
在 `promptfooconfig.yaml` 中調整需評估的模型和測試類型：
```yaml
prompts:
  - file://./prompts/prompt_basic.yaml   # 基本問答評估
  # - file://./prompts/prompt_tool.yaml  # 工具調用評估 (取消註解使用)

providers:
  - file://./providers/breeze.yaml       # 使用 Breeze 模型
  # - file://./providers/llama2.yaml     # 取消註解使用其他模型
  # - file://./providers/Llama-3.2-3B-F1.yaml
  # - file://./providers/gpt-4o-mini.yaml

tests: 
  - file://./tests/generate.py:basic_eval  # 基本問答測試
  # - file://./tests/generate.py:tool_eval # 工具調用測試 (取消註解使用)
```

#### 執行評估
執行所有測試與模型的評估：
```bash
promptfoo eval
```

#### 保存評估結果
將評估結果保存為 JSON 檔案：
```bash
promptfoo eval --output results.json
```

#### 除錯
顯示詳細的評估過程與錯誤訊息：
```bash
promptfoo eval --verbose
```

### 視覺化與分析結果

啟動 Web 介面查看最新評估結果：
```bash
promptfoo view
```

Web 介面功能：
- 查看每個模型在不同測試案例的表現
- 比較不同模型的回應內容
- 分析評估分數與錯誤原因
- 匯出評估報告

### 常見問題排解

1. **找不到模型**
   -> 確認模型名稱是否正確，本地模型是否已下載
   ```bash
   # 檢查本地模型
   ollama list
   ```

2. **評估過程錯誤**
   -> 查看 promptfoo-errors.log 檔案找出錯誤原因
   ```bash
   # Windows
   type promptfoo-errors.log | Select-Object -Last 50
   
   # Linux/Mac
   tail -n 50 promptfoo-errors.log
   ```

3. **未獲得評估結果**
   -> 檢查 providers 目錄中的模型配置是否正確

4. **API 金鑰問題**
   -> 確認環境變數是否正確設定
   ```bash
   # Windows
   echo %OPENAI_API_KEY%
   
   # Linux/Mac
   echo $OPENAI_API_KEY
   ```

## 評估標準

本專案使用多種斷言方式評估模型表現：

1. **基本問答評估 (basic_eval)**：
   - 使用 LLM-rubric 評估模型回應與預期回應的相似度
   - 預設閾值：0.7（70% 相似度）
   - 使用 GPT-4o-mini 作為評估器

2. **工具調用評估 (tool_eval)**：
   - 使用 JavaScript 檢查模型是否正確識別並調用工具
   - 驗證回應中是否包含預期的工具調用格式
   - 檢查是否正確提取必要參數

## 擴充方式

1. **添加新模型**
   - 在 `providers/` 目錄中建立新的 YAML 檔案
   - 設定模型 ID、標籤和配置參數
   - 在 `promptfooconfig.yaml` 中引用此檔案

2. **添加新測試數據**
   - 在 `data/` 目錄中更新或添加新的 CSV 檔案
   - 確保 CSV 格式一致，避免欄位數不一致問題

3. **修改評估方法**
   - 在 `tests/generate.py` 中更新或添加新的評估函數
   - 實現不同的斷言邏輯和評估標準

4. **調整評估標準**
   - 修改測試案例中的斷言類型、權重和閾值
   - 可用斷言類型：llm-rubric、javascript、contains 等
   - 調整閾值以控制評估嚴格程度

5. **自動化測試流程**
   - 結合 CI/CD 工具如 GitHub Actions
   - 設置定期評估以監控模型性能變化
