import json
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field, asdict


class JSONSaveLoadMixin:
    def save_to_json(self, json_path: str):
        json_string = json.dumps(asdict(self), indent=2, sort_keys=True) + "\n"
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(json_string)

    @classmethod
    def load_from_json(cls, json_path: str):
        with open(json_path, "r", encoding="utf-8") as f:
            text = f.read()
        return cls(**json.loads(text))


class ReprMixin:
    def update(self, contents: Dict, overwrite=False):
        for key, value in contents.items():
            if key in self.__dict__.keys() and not self.overwrite:
                continue
            setattr(self, key, value)

    def __repr__(self):
        cls_name = self.__class__.__qualname__
        FIELDS = self.__dataclass_fields__
        ADDED = list(set(self.__dict__.keys()).difference(FIELDS))
        ADDED = {k: v for k, v in self.__dict__.items() if k in ADDED}
        contents = "==== FIELDS CONTENTS ====\n" + ", ".join([
            field.name + ": " +  str(field.type).split(".")[-1]
            for field in FIELDS.values()
        ])
        if ADDED:
            contents += "\n==== ADDED CONTENTS ====\n" + ", ".join([
                k + ": " + str(type(v)) for k, v in ADDED.items()
            ])
        N_EPOCHS = len(list(self.__dict__.values())[0])
        return cls_name + f"(N_EPOCHS:{N_EPOCHS}):\n" + contents


@dataclass(repr=False)
class TrainRecord(JSONSaveLoadMixin, ReprMixin):
    loss_discriminator: List[float] = field(default_factory=list)
    loss_generator: List[float] = field(default_factory=list)
    loss_reconstruction: List[float] = field(default_factory=list)
    latent_max_distr: List[float] = field(default_factory=list)
    latent_avg_entropy: List[float] = field(default_factory=list)
    latent_avg: List[float] = field(default_factory=list)
    dirich_avg_entropy: List[float] = field(default_factory=list)
    loss_labeled: List[float] = field(default_factory=list)


@dataclass(repr=False)
class EvalRecord(JSONSaveLoadMixin, ReprMixin):
    npmi: List[float] = field(default_factory=list)
    topic_uniqueness: List[float] = field(default_factory=list)
    top_words: List[float] = field(default_factory=list)
    npmi2: List[float] = field(default_factory=list)
    topic_uniqueness2: List[float] = field(default_factory=list)
    top_words2: List[float] = field(default_factory=list)
    u_loss_train: List[float] = field(default_factory=list)
    l_loss_train: List[float] = field(default_factory=list)
    u_loss_val: List[float] = field(default_factory=list)
    l_loss_val: List[float] = field(default_factory=list)
    u_loss_test: List[float] = field(default_factory=list)
    l_loss_test: List[float] = field(default_factory=list)
    l_acc_train: List[float] = field(default_factory=list)
    l_acc_val: List[float] = field(default_factory=list)
    l_acc_test: List[float] = field(default_factory=list)
