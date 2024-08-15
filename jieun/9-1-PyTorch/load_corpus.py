# 구현하세요!
from datasets import load_dataset

def load_corpus() -> list[str]:
    corpus: list[str] = []
    # 구현하세요!
    dataset = load_dataset('wikitext', 'wikitext-2-v1')

    for split in ['validation', 'test']:
        for item in dataset[split]:
            corpus.append(item['text'])
            

    return corpus