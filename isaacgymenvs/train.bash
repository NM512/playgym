# Execute just 1 policy training
python train.py task=ShadowHand num_envs=1 train.params.config.minibatch_size=8

# (horizon_length * num_actors(num_envs) * num_agents(defaut 1)) % minibatch_size == 0 is necessary