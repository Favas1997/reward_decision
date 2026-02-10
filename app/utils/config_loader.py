"""
Configuration loader.

Loads reward policy from YAML file.
"""

import yaml


def load_policy():
    """
    Load policy configuration.

    :return: Policy dictionary
    """
    with open("app/config/policy.yaml") as f:
        return yaml.safe_load(f)