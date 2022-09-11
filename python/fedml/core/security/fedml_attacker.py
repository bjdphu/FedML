from .attack.byzantine_attack import ByzantineAttack
from .constants import ATTACK_METHOD_BYZANTINE_ATTACK
import logging
from ..common.ml_engine_backend import MLEngineBackend
from typing import List, Tuple, Dict, Any


class FedMLAttacker:
    _attacker_instance = None

    @staticmethod
    def get_instance():
        if FedMLAttacker._attacker_instance is None:
            FedMLAttacker._attacker_instance = FedMLAttacker()

        return FedMLAttacker._attacker_instance

    def __init__(self):
        self.is_enabled = False
        self.attack_type = None
        self.attacker = None

    def init(self, args):
        if hasattr(args, "enable_attack") and args.enable_attack:
            logging.info("------init attack..." + args.attack_type.strip())
            self.is_enabled = True
            self.attack_type = args.attack_type.strip()
            self.attacker = None
            if self.attack_type == ATTACK_METHOD_BYZANTINE_ATTACK:
                self.attacker = ByzantineAttack(args)
            # elif self.attack_type == ATTACK_METHOD_DLG:
            #     self.attacker = DLGAttack(model=args.model, attack_epoch=args.attack_epoch)
        else:
            self.is_enabled = False

        if self.is_enabled:
            if hasattr(args, MLEngineBackend.ml_engine_args_flag) and args.ml_engine in [
                MLEngineBackend.ml_engine_backend_tf,
                MLEngineBackend.ml_engine_backend_jax,
                MLEngineBackend.ml_engine_backend_mxnet,
            ]:
                logging.info(
                    "FedMLAttacker is not supported for the machine learning engine: %s. "
                    "We will support more engines in the future iteration."
                    % args.ml_engine
                )
                self.is_enabled = False

    def is_attack_enabled(self):
        return self.is_enabled

    def get_attack_types(self):
        return self.attack_type

    def is_model_attack(self):
        if self.is_attack_enabled() and self.attack_type in [
            ATTACK_METHOD_BYZANTINE_ATTACK
        ]:
            return True
        return False

    def is_poison_data_attack(self):
        if self.is_attack_enabled() and self.attack_type in []:
            return True
        return False

    def is_reconstruct_data_attack(self):
        if self.is_attack_enabled() and self.attack_type in []:
            return True
        return False

    def attack_model(self, raw_client_grad_list: List[Tuple[float, Dict]], extra_auxiliary_info: Any = None):
        if self.attacker is None:
            raise Exception("attacker is not initialized!")
        return self.attacker.attack_model(raw_client_grad_list, extra_auxiliary_info)

    def poison_data(self, dataset):
        if self.attacker is None:
            raise Exception("attacker is not initialized!")
        return self.attacker.poison_data(dataset)

    def reconstruct_data(self, a_gradient: dict, extra_auxiliary_info: Any = None):
        if self.attacker is None:
            raise Exception("attacker is not initialized!")
        return self.attacker.reconstruct_data(a_gradient, extra_auxiliary_info=extra_auxiliary_info)
