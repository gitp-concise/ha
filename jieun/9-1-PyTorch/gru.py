import torch
from torch import nn, Tensor


class GRUCell(nn.Module):
    def __init__(self, input_size: int, hidden_size: int) -> None:
        super().__init__()
        # 구현하세요!
        # Update gate
        self.W_z = nn.Linear(input_size, hidden_size)
        self.U_z = nn.Linear(hidden_size, hidden_size)
        
        # Reset gate
        self.W_r = nn.Linear(input_size, hidden_size)
        self.U_r = nn.Linear(hidden_size, hidden_size)
        
        # Candidate hidden state
        self.W_h = nn.Linear(input_size, hidden_size)
        self.U_h = nn.Linear(hidden_size, hidden_size)

    def forward(self, x: Tensor, h: Tensor) -> Tensor:
        # 구현하세요!
        # Update gate
        z_t = torch.sigmoid(self.W_z(x) + self.U_z(h))
        
        # Reset gate
        r_t = torch.sigmoid(self.W_r(x) + self.U_r(h))
        
        # Candidate hidden state
        h_hat_t = torch.tanh(self.W_h(x) + self.U_h(r_t * h))
        
        # New hidden state
        h_t = (1 - z_t) * h + z_t * h_hat_t
        
        return h_t


class GRU(nn.Module):
    def __init__(self, input_size: int, hidden_size: int) -> None:
        super().__init__()
        self.hidden_size = hidden_size
        self.cell = GRUCell(input_size, hidden_size)
        # 구현하세요!

    def forward(self, inputs: Tensor) -> Tensor:
        # 구현하세요!
        batch_size, sequence_length, d_model = inputs.size()
        h = torch.zeros(batch_size, self.hidden_size, device=inputs.device)
        
        for t in range(sequence_length):
            h = self.cell(inputs[:, t, :], h)
        
        return h