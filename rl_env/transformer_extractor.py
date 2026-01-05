import torch
import torch.nn as nn
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor


class TemporalTransformerExtractor(BaseFeaturesExtractor):
    """
    Modular temporal feature extractor for ablation study.

    Modules:
      - Frame Encoder
      - Temporal Model (Transformer / Identity)
      - Temporal Aggregation (CLS / mean / last)
    """

    def __init__(
        self,
        observation_space,
        features_dim=128,

        # ===== encoder =====
        use_encoder=True,

        # ===== temporal =====
        temporal_type="transformer",  # "transformer" | "none"
        n_layers=2,
        n_heads=4,
        ff_dim=256,

        # ===== aggregation =====
        aggregation="cls",  # "cls" | "mean" | "last"
    ):
        super().__init__(observation_space, features_dim)

        T, obs_dim = observation_space.shape
        self.T = T
        self.features_dim = features_dim

        self.use_encoder = use_encoder
        self.temporal_type = temporal_type
        self.aggregation = aggregation

        # =====================
        # 1. Frame Encoder
        # =====================
        if use_encoder:
            self.frame_encoder = nn.Linear(obs_dim, features_dim)
        else:
            # no encoder, project later
            self.frame_encoder = nn.Identity()
            self.input_proj = nn.Linear(obs_dim, features_dim)

        # =====================
        # 2. Temporal Model
        # =====================
        if temporal_type == "transformer":
            encoder_layer = nn.TransformerEncoderLayer(
                d_model=features_dim,
                nhead=n_heads,
                dim_feedforward=ff_dim,
                batch_first=True,
            )
            self.temporal_model = nn.TransformerEncoder(
                encoder_layer,
                num_layers=n_layers,
            )

            if aggregation == "cls":
                self.cls_token = nn.Parameter(
                    torch.zeros(1, 1, features_dim)
                )

        elif temporal_type == "none":
            self.temporal_model = nn.Identity()

        else:
            raise ValueError(f"Unknown temporal_type: {temporal_type}")

        # =====================
        # 3. Output head
        # =====================
        self.output_proj = nn.Linear(features_dim, features_dim)

    # =====================
    # Forward
    # =====================
    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        """
        obs: (B, T, obs_dim)
        """
        B, T, _ = obs.shape

        # ----- Frame encoding -----
        if self.use_encoder:
            x = self.frame_encoder(obs)  # (B, T, D)
        else:
            x = self.input_proj(obs)     # (B, T, D)

        # ----- Temporal modeling -----
        if self.temporal_type == "transformer":
            if self.aggregation == "cls":
                cls = self.cls_token.expand(B, 1, -1)
                x = torch.cat([cls, x], dim=1)

            x = self.temporal_model(x)

        # ----- Aggregation -----
        if self.aggregation == "cls":
            h = x[:, 0]
        elif self.aggregation == "mean":
            h = x.mean(dim=1)
        elif self.aggregation == "last":
            h = x[:, -1]
        else:
            raise ValueError(f"Unknown aggregation: {self.aggregation}")

        return self.output_proj(h)


# TemporalTransformerExtractor(
#     observation_space,
#     use_encoder=True,
#     temporal_type="transformer",
#     aggregation="cls"
# )
