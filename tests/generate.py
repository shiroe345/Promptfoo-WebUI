import pandas as pd

def basic_eval():
    testcases = []
    df = pd.read_csv("data/digsign_basic.csv")
    # df = df[:3]
    for index, row in df.iterrows():
        testcases.append({
            "vars": {
                "user_prompt": row["使用者輸入"]
            },
            "assert": [
                {
                    "type": "llm-rubric",
                    "value": row["預期 LLM 回應"],
                    "weight": 1,
                    "provider": "openai:gpt-4o-mini"
                }
            ],
            "threshold": 0.7
        })

    return testcases

def tool_eval():
    testcases = []
    df = pd.read_csv("data/digsign_tool.csv")
    # df = df[:3]
    for index, row in df.iterrows():
        testcases.append({
            "vars": {
                "user_prompt": row["使用者輸入"]
            },
            "assert": [
                {
                    "type": "javascript",
                    "value": f"output.includes('{row['tool_calls']}')",
                    "weight": 1
                }
            ],
            "threshold": 0.7
        })

    return testcases




    