from environment import *

class KnapsackRandomAgent():

    def __init__( self, env: KnapsackEnv ):
        self.env = env

    def act(self):
        """
        Acts according to random policy
        """
        action = self.env.action_space.sample() 
        obs, reward, done, info = self.env.step(action)
        return obs, reward, done, info 

    def play(self, n_episodes, n_max_steps_per_episode, render_callback=None ):
        
        import os

        # Run n_episodes episodes
        for i_episode in range(n_episodes):
            obs = self.env.reset() # random knapsack
            done = False
            for t in range(n_max_steps_per_episode):
                
                obs, reward, done, info = self.act()
                
                if render_callback is not None:
                    render_callback( i_episode, t )
                
                if done:
                    break
                
            self.env.close()
            # if (t % 1000 == 0):
            #     print(f"agent iteration {t}")

    def learn(self, n_episodes, n_max_steps_per_episode):
        pass