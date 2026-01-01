import torch
import torch.nn as nn
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor


class TemporalTransformerExtractor(BaseFeaturesExtractor):
    """
    Transformer-based temporal feature extractor for UAM.
    Input: (B, T, obs_dim)
    Output: (B, features_dim)
    """

    def __init__(
        self,
        observation_space,
        features_dim=128,
        n_layers=2,
        n_heads=4,
        ff_dim=256,
    ):
        super().__init__(observation_space, features_dim)

        # observation_space.shape = (T, obs_dim)
        T, obs_dim = observation_space.shape

        self.input_proj = nn.Linear(obs_dim, features_dim)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=features_dim,
            nhead=n_heads,
            dim_feedforward=ff_dim,
            batch_first=True,
        )

        self.transformer_encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=n_layers,
        )

        self.cls_token = nn.Parameter(torch.zeros(1, 1, features_dim))

        self.output_proj = nn.Linear(features_dim, features_dim)

    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        """
        obs shape: (B, T, obs_dim)
        """

        B, T, _ = obs.shape

        x = self.input_proj(obs)  # (B, T, D)

        cls = self.cls_token.expand(B, 1, -1)
        x = torch.cat([cls, x], dim=1)

        h = self.transformer_encoder(x)

        # use CLS token
        out = h[:, 0]

        return self.output_proj(out)
