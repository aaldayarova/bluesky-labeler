#!/usr/bin/env python3
import os
import pandas as pd
import ast
import re

def load_and_parse(path):
    df = pd.read_csv(path)
    df['Labels'] = df['Labels'].apply(parse_cell)
    return df

def parse_cell(x):
    if not isinstance(x, str):
        return x

    # 1) literal_eval raw
    try:
        return ast.literal_eval(x)
    except Exception:
        pass

    # 2) collapse double-quotes into single
    cleaned = re.sub(r'""+', '"', x)
    try:
        return ast.literal_eval(cleaned)
    except Exception:
        pass

    # 3) fallback: capture first quoted substring
    m = re.search(r'"([^"]+)"', cleaned)
    return [m.group(1)] if m else []

def main():
    script_dir   = os.path.dirname(__file__)
    results_csv  = os.path.join(script_dir, 'test-posts-results.csv')
    labels_csv   = os.path.join(script_dir, 'test-posts-labeled.csv')

    results_df = load_and_parse(results_csv)
    labels_df  = load_and_parse(labels_csv)
    
    df = pd.merge(
        results_df,
        labels_df,
        on='URL',
        how='inner',
        suffixes=('_pred', '_true')
    )
    
    df['correct'] = df.apply(
        lambda r: r['Labels_pred'] == r['Labels_true'], axis=1
    )
    
    total, correct = len(df), df['correct'].sum()
    acc = correct / total if total else 0.0

    print(f"Total posts checked: {total}")
    print(f"Correct predictions: {correct}")
    print(f"Accuracy           : {acc:.2%}\n")
    
    bad = df.loc[~df['correct'], ['URL', 'Labels_pred', 'Labels_true']]
    if not bad.empty:
        print("Mismatches:")
        for _, row in bad.iterrows():
            print(f"- {row.URL}")
            print(f"    Predicted: {row.Labels_pred}")
            print(f"      Actual: {row.Labels_true}")

if __name__ == "__main__":
    main()