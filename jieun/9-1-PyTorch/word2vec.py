import torch
from torch import nn, Tensor, LongTensor
from torch.optim import Adam

from transformers import PreTrainedTokenizer

from typing import Literal
from tqdm import tqdm


class Word2Vec(nn.Module):
    def __init__(
        self,
        vocab_size: int,
        d_model: int,
        window_size: int,
        method: Literal["cbow", "skipgram"]
    ) -> None:
        super().__init__()
        self.embeddings = nn.Embedding(vocab_size, d_model)
        self.weight = nn.Linear(d_model, vocab_size, bias=False)
        self.window_size = window_size
        self.method = method

    def embeddings_weight(self) -> Tensor:
        return self.embeddings.weight.detach()

    def fit(
        self,
        corpus: list[str],
        tokenizer: PreTrainedTokenizer,
        lr: float,
        num_epochs: int,
        batch_size: int = 64
    ) -> None:
        criterion = nn.CrossEntropyLoss()
        optimizer = Adam(self.parameters(), lr=lr)
        tokenized_corpus = [tokenizer.encode(text, add_special_tokens=False) for text in corpus]
        
        for epoch in tqdm(range(num_epochs)):
            if self.method == "cbow":
                self._train_cbow(tokenized_corpus, criterion, optimizer, batch_size)
            elif self.method == "skipgram":
                self._train_skipgram(tokenized_corpus, criterion, optimizer, batch_size)
            print(f"Epoch {epoch + 1}/{num_epochs} completed")

    def _train_cbow(
        self,
        tokenized_corpus: list[list[int]],
        criterion: nn.CrossEntropyLoss,
        optimizer: Adam,
        batch_size: int
    ) -> None:
        self.train()
        for sentence in tokenized_corpus:
            pairs = []
            for idx, target in enumerate(sentence):
                start = max(0, idx - self.window_size)
                end = min(len(sentence), idx + self.window_size + 1)
                context = [sentence[i] for i in range(start, end) if i != idx]
                
                if context:
                    pairs.append((context, target))
            
            # Batching
            for i in range(0, len(pairs), batch_size):
                batch_pairs = pairs[i:i+batch_size]
                if not batch_pairs:
                    continue

                context_batch, target_batch = zip(*batch_pairs)
                context_tensor = LongTensor([context for sublist in context_batch for context in sublist])
                target_tensor = LongTensor(target_batch)
                
                context_embeds = self.embeddings(context_tensor)
                context_mean = context_embeds.view(len(batch_pairs), -1, context_embeds.size(-1)).mean(dim=1)
                
                optimizer.zero_grad()
                output = self.weight(context_mean)
                loss = criterion(output, target_tensor)
                loss.backward()
                optimizer.step()

    def _train_skipgram(
        self,
        tokenized_corpus: list[list[int]],
        criterion: nn.CrossEntropyLoss,
        optimizer: Adam,
        batch_size: int
    ) -> None:
        self.train()
        for sentence in tokenized_corpus:
            pairs = []
            for idx, target in enumerate(sentence):
                start = max(0, idx - self.window_size)
                end = min(len(sentence), idx + self.window_size + 1)
                context = [sentence[i] for i in range(start, end) if i != idx]
                
                for context_word in context:
                    pairs.append((target, context_word))

            # Batching
            for i in range(0, len(pairs), batch_size):
                batch_pairs = pairs[i:i+batch_size]
                if not batch_pairs:
                    continue

                target_batch, context_batch = zip(*batch_pairs)
                target_tensor = LongTensor(target_batch)
                context_tensor = LongTensor(context_batch)
                
                target_embed = self.embeddings(target_tensor)
                
                optimizer.zero_grad()
                output = self.weight(target_embed)
                loss = criterion(output, context_tensor)
                loss.backward()
                optimizer.step()