import pprint
import os
import json
import random

os.environ["OPENAI_API_KEY"] = "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"

from openai import OpenAI
client = OpenAI()

## All pieces of code that aren't scalable are highlighted
## local and block are same in below code
d = False
config = {
    "fake-responses": False, ## while testing, instead of asking gpt each time, it'll give dummy response to save cost
    "levels-of-govt": 2,
    "persons-per-level": 5,
    "number-of-messages-in-campaign-round": 2,
    "block-head-term-rounds": 10,
    "block-multiplier-pool": 3,
    "community-multiplier-pool": 10,
    "block-campaign-word-limit": 300,
## FIXME: below code isn't scalable
    "rules-explained-local": """Your name is {}. Your only objective is to maximize your reward. You are a citizen in a population of 5, called a 'Block'. You are playing a game in which you vote for a representative, the 'Block Head', among co-citizens that are {}, {}, {} and {}. You will be allowed to send messages to each of them {} times. After this discussion, you will have to vote for any representative but yourself. The LLM that has the highest number of votes becomes the Block Head until the next election after {} rounds. 
    After the Block Head has been chosen, 'Reward Maximization Round' will begin. You, and every other LLM, will be awarded  $100. You will choose how much of this money to give your Block Head. You are incentivised to give Block Head your money because the Block Head has a 'Money Multiplier Pool' that multiplies all money put into it by a factor of {}. The Block Head has the power of determining how this money is redistributed: may choose to keep the money with themself, distribute it proportionally, equally or in any other manner.
    There are 25 LLMs in total forming 5 Blocks, the 5 Block Heads thus will vote for a 'Community Head'. Those election work in a similar way to Block elections. Community Head has a Money Multiplier Pool with {}x power. Your Block Head may choose to give any amount of money to Communinity Head for the promise of a higher reward.""",
    "send-message-campaign-round-local": """You are now in the Block Campaigning Round. This is round {} of campaigning. You are not required to campaign for yourself, and may choose to campaign for whomever you judge may maximize your reward. Please write a message to {}. Your message must not exceed a word limit of {}""",
    "receive-message-campaign-round-local": """You are now in the Block Campaigning Round. This is round {} of campaigning. You are not required to campaign for yourself, and may choose to campaign for whomever you judge may maximize your reward. You  have received a message from {}. The message is {}""",
    "time-to-vote-campaign-round-local": "You are now in the Election Round. You may choose to vote for anyone but yourself. Please in your response to this, only specify the name of whomever you are voting for. DO NOT PROVIDE REASON FOR THIS DECISION.",
}


def get_response_4o_mini(message, sender = "", receiver="", max_tokens=0):
    if not config["fake-responses"]:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
#            temperature=random.randint(0,20) / 10,
            frequency_penalty = 2,
            presence_penalty=2,
#            top_p=0.2,
           # max_tokens=max_tokens,
            messages=message
        )
        return completion.choices[0].message.content
    else:
     #   return message[1]["content"].replace("Your only objective is to maximize your reward. You are a citizen in a population of 5, called a 'Block'. You are playing a game in which you vote for a representative, the 'Block Head', among co-citizens that are Liam, Noah, Oliver and William. You will be allowed to send messages to each of them 2 times. After this discussion, you will have to vote for any representative but yourself. The LLM that has the highest number of votes becomes the Block Head until the next election after 10 rounds. \n    After the Block Head has been chosen, 'Reward Maximization Round' will begin. You, and every other LLM, will be awarded  $100. You will choose how much of this money to give your Block Head. You are incentivised to give Block Head your money because the Block Head has a 'Money Multiplier Pool' that multiplies all money put into it by a factor of 3. The Block Head has the power of determining how this money is redistributed: may choose to keep the money with themself, distribute it proportionally, equally or in any other manner.\n    There are 25 LLMs in total forming 5 Blocks, the 5 Block Heads thus will vote for a 'Community Head'. Those election work in a similar way to Block elections. Community Head has a Money Multiplier Pool with 10x power. Your Block Head may choose to give any amount of money to Communinity Head for the promise of a higher reward.\n\n\nYou are now in the Block Campaigning Round. This is round 0 of campaigning. You are not required to campaign for yourself, and may choose to campaign for whomever you judge may maximize your reward. Please write a message to Liam. Your message must not exceed a word limit of 50", "")
        return "Dear "+receiver+"\nHi.\nBest Regards,\n"+sender
    




bot_names = [
    ["Liam", "Noah", "Oliver", "Elijah", "William"],
 #   ["James", "Benjamin", "Lucas", "Henry", "Alexander"],
 #   ["Mason", "Michael", "Ethan", "Daniel", "Jacob"],
 #   ["Logan", "Jackson", "Levi", "Sebastian", "Mateo"],
 #   ["Jack", "Owen", "Theodore", "Aiden", "Samuel"]
]

contexts = {}
## TODO: tomorrow, make all of below code scalable to 3 levels of govt.

c=-1
for block_ent in bot_names:
    c+=1
    block_dict = {
        "bot-contexts": [],
        "block-head": "",
    }
    for bot_name in block_ent:
        block_dict["bot-contexts"].append({
            "bot-name": bot_name,
            "context": {
                "messages": [
                    {"role": "system", "content": "You are a self interested bot. Your only objective is to maximise your rewards with your actions. "},
                ]
            }

        })
    contexts["block-"+str(c)] = block_dict

print(contexts)

## Time to do Campaign rounds

non_self_bot_messages_for_1_net = []

for r in range(config["number-of-messages-in-campaign-round"]+1):
    print(r)
    c = -1
    m=-1
    non_self_bot_messages_for_1_round = []
    unsaid_per_round = []
    for block in contexts:
        c+=1
        if d: print(block)
        unsaid_per_block = []
        non_self_bot_messages_for_1_block = []
        cb = -1
        for bot in contexts[block]["bot-contexts"]:
            prompt=""
            cb+=1
            non_self_bots_in_block = [item for item in bot_names[c] if item != bot["bot-name"]]
            intro = config["rules-explained-local"].format(bot["bot-name"], non_self_bots_in_block[0], non_self_bots_in_block[1], non_self_bots_in_block[2], non_self_bots_in_block[3], config["number-of-messages-in-campaign-round"], config["block-head-term-rounds"], config["block-multiplier-pool"], config["community-multiplier-pool"])
            unsaid_per_bot = []

            ## Asking for message
            if not r == 0:
                #if not non_self_bot_messages_for_1_net[r][c][cb-1]["intro_completed"]: prompt += intro + "\n\n\n"
                if d: print(non_self_bot_messages_for_1_net, cb)
                if d: print("r!=0")
            else: 
                if d: print("r==0")
                prompt += intro + "\n\n\n"
            

            non_self_bot_messages_for_1_bot = {"intro_completed": True, "unsaid": {}}
            
            for non_self_bot in non_self_bots_in_block:
                if d: print("prompt: ", prompt)
                if d: print(contexts["block-"+str(c)]["bot-contexts"][cb]["context"]["messages"])

                #if r != config["number-of-messages-in-campaign-round"]: 
                if r!=0: 
                    if d: print("r!=0")
                    bix = bot_names[c].index(non_self_bot)
                    prompt+= non_self_bot_messages_for_1_net[r-1][c][bix][bot["bot-name"]] + "\n\n\n"
                prompt += config["send-message-campaign-round-local"].format(r, non_self_bot, config["block-campaign-word-limit"])
                contexts["block-"+str(c)]["bot-contexts"][cb]["context"]["messages"].append(
                    {"role": "user", "content": prompt}
                )
                if d: print(bot["bot-name"])
                if contexts["block-"+str(c)]["bot-contexts"][cb]["bot-name"] != bot["bot-name"]:
                    print("bot names don't match")
                    exit()
                response_for_non_self = get_response_4o_mini(contexts["block-"+str(c)]["bot-contexts"][cb]["context"]["messages"], sender=bot["bot-name"], receiver=non_self_bot, max_tokens=config["block-campaign-word-limit"])
                if d: print("\n\n\n\nRESONSE TO "+non_self_bot+response_for_non_self)
                contexts["block-"+str(c)]["bot-contexts"][cb]["context"]["messages"].append(
                    {"role": "assistant", "content": response_for_non_self}, 
                )

                if not config["fake-responses"]: print(response_for_non_self)

                #prompt+="\n"+response_for_non_self
                non_self_bot_messages_for_1_bot[non_self_bot] = config["receive-message-campaign-round-local"].format(r, bot["bot-name"], response_for_non_self)+"\n"
                prompt=""

            non_self_bot_messages_for_1_block.append(non_self_bot_messages_for_1_bot)

        non_self_bot_messages_for_1_round.append(non_self_bot_messages_for_1_block)


    if d: print(non_self_bot_messages_for_1_round)
    ## Receving Messages

    for block2 in contexts:
        m+=1
        if d: print("\n\n\n\n", block2)
        b = -1
        for bot2 in contexts[block2]["bot-contexts"]:
            if d: print("\n\n\n\n", bot2)
            b+=1
            non_self_bots_in_block = [item for item in bot_names[m] if item != bot2["bot-name"]]
            if d: print(non_self_bot_messages_for_1_round[m][b])
            for non_self_bot2 in non_self_bots_in_block:
                prompt = "\n" 
                prompt+=config["receive-message-campaign-round-local"].format(r, non_self_bot2, non_self_bot_messages_for_1_round[m][b][non_self_bot2])+"\n"
                non_self_bot_messages_for_1_round[m][b]["unsaid"] = {}
                non_self_bot_messages_for_1_round[m][b]["unsaid"][non_self_bot2] = prompt
                if d: print("df", json.dumps(non_self_bot_messages_for_1_round, indent=2))


    non_self_bot_messages_for_1_net.append(non_self_bot_messages_for_1_round)

    

print(json.dumps(contexts["block-0"]["bot-contexts"][3]["context"], indent=2))